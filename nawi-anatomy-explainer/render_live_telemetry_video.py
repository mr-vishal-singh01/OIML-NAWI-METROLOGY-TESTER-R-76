import os
import math
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_PATH = "/home/zeno/Desktop/SIH_NAWI_Login_Background.png"
OUTPUT_VIDEO_PATH = "/home/zeno/Desktop/SIH_NAWI_Background_Loop.mp4"
FONT_PATH = "/home/zeno/.local/share/fonts/JetBrainsMonoNerdFontMono-ExtraBold.ttf"

TOTAL_FRAMES = 240  # 8.0 seconds at 30 fps (seamless high-fps loop)
FPS = 30
WIDTH = 1920
HEIGHT = 1080

def get_bezier_point(p0, p1, p2, p3, t):
    """Cubic bezier point at parameter t in [0, 1]"""
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)

def build_cable_points(num_points=1200):
    """Precompute points along the continuous serial cable path"""
    # Segment 1: from smart dongle (680, 190) down to floor
    p0 = (680, 190)
    p1 = (820, 200)
    p2 = (840, 860)
    p3 = (1160, 860)
    
    # Segment 2: from floor (1160, 860) up into PrecisionX terminal (1400, 560)
    p4 = (1160, 860)
    p5 = (1280, 860)
    p6 = (1320, 680)
    p7 = (1400, 560)
    
    pts = []
    half = num_points // 2
    for i in range(half):
        t = i / float(half)
        pts.append(get_bezier_point(p0, p1, p2, p3, t))
    for i in range(half):
        t = i / float(half)
        pts.append(get_bezier_point(p4, p5, p6, p7, t))
    return pts

def main():
    print(f"Loading base image from: {BASE_IMAGE_PATH}")
    base_pil = Image.open(BASE_IMAGE_PATH).convert("RGBA")
    base_np = np.array(base_pil)  # RGBA uint8
    
    font_led = ImageFont.truetype(FONT_PATH, 32)
    font_unit = ImageFont.truetype(FONT_PATH, 13)
    font_status = ImageFont.truetype(FONT_PATH, 8)
    font_hash = ImageFont.truetype(FONT_PATH, 9)
    
    cable_pts = build_cable_points(1200)
    num_pts = len(cable_pts)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "16",
        OUTPUT_VIDEO_PATH
    ]
    
    print(f"Starting FFMPEG pipe to generate {TOTAL_FRAMES} frames ({TOTAL_FRAMES/FPS:.1f}s at {FPS}fps)...")
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    num_packets = 14
    packet_spacing = num_pts / float(num_packets)
    
    for frame_idx in range(TOTAL_FRAMES):
        if frame_idx % 60 == 0:
            print(f"Rendering frame {frame_idx}/{TOTAL_FRAMES} ({frame_idx/TOTAL_FRAMES*100:.1f}%)...")
            
        frame = base_np.copy()
        overlay = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
        
        # 1. Moving Telemetry Photon Packets along Cable
        for k in range(num_packets):
            cur_pos = (frame_idx * 5.5 + k * packet_spacing) % num_pts
            pt = cable_pts[int(cur_pos)]
            px, py = int(pt[0]), int(pt[1])
            
            # Outer cyan bloom
            cv2.circle(overlay, (px, py), 14, (2, 132, 199, 100), -1)
            # Mid bright cyan
            cv2.circle(overlay, (px, py), 7, (56, 189, 248, 200), -1)
            # Pure white photon core
            cv2.circle(overlay, (px, py), 3, (255, 255, 255, 255), -1)
            
            # Motion blur trail
            for trail_i in range(1, 5):
                prev_pos = (cur_pos - trail_i * 6) % num_pts
                t_pt = cable_pts[int(prev_pos)]
                alpha = int(150 / (trail_i + 1))
                cv2.circle(overlay, (int(t_pt[0]), int(t_pt[1])), max(1, 4 - trail_i), (56, 189, 248, alpha), -1)

        # 2. Dynamic Waveform in PrecisionX Engine (x: 1380, y: 226, w: 450, h: 64)
        cv2.rectangle(frame, (1380, 226), (1830, 290), (2, 7, 20, 255), -1)
        for gx in range(1380, 1830, 45):
            cv2.line(frame, (gx, 226), (gx, 290), (30, 41, 59, 130), 1)
        cv2.line(frame, (1380, 258), (1830, 258), (30, 41, 59, 180), 1)
        
        wave_pts = []
        phase = frame_idx * 0.16
        for x_rel in range(0, 440, 3):
            x_abs = 1385 + x_rel
            damp = math.exp(-x_rel / 80.0)
            noise = math.sin(phase * 2.2 + x_rel * 0.12) * 2.2 * damp
            osc = math.sin(phase + x_rel * 0.08) * 19.0 * damp + noise
            y_abs = int(258 + osc)
            wave_pts.append((x_abs, y_abs))
            
        for i in range(len(wave_pts) - 1):
            cv2.line(frame, wave_pts[i], wave_pts[i+1], (56, 189, 248, 255), 2)
            
        cv2.circle(frame, (1825, 258), 5, (16, 185, 129, 255), -1)
        cv2.circle(overlay, (1825, 258), 12, (16, 185, 129, 110), -1)

        # 3. Dynamic Rotating XML Ring at (1388, 453)
        center_seal = (1388, 453)
        radius = 16
        angle_start = (frame_idx * 4) % 360
        cv2.ellipse(overlay, center_seal, (radius, radius), 0, angle_start, angle_start + 80, (192, 132, 252, 240), 2)
        cv2.ellipse(overlay, center_seal, (radius, radius), 0, angle_start + 120, angle_start + 200, (192, 132, 252, 240), 2)
        cv2.ellipse(overlay, center_seal, (radius, radius), 0, angle_start + 240, angle_start + 320, (192, 132, 252, 240), 2)

        # 4. Blend overlay
        mask = overlay[:, :, 3] > 0
        frame[mask] = overlay[mask]

        # 5. Convert to PIL for LED digits
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)

        # LED Display Window: (380, 185, w: 200, h: 42)
        draw.rounded_rectangle([380, 185, 580, 227], radius=4, fill=(24, 4, 8, 255), outline=(239, 68, 68, 255), width=1)
        
        # Settling simulation in first 40 frames
        if frame_idx < 10:
            display_val = " 0.00"
            stable = False
        elif frame_idx < 22:
            display_val = "18.45"
            stable = False
        elif frame_idx < 34:
            display_val = "36.80"
            stable = False
        elif frame_idx < 44:
            display_val = "49.95"
            stable = False
        else:
            display_val = "50.00"
            stable = True

        # Draw Glowing Red Digits
        draw.text((398, 189), display_val, font=font_led, fill=(153, 27, 27, 180))
        draw.text((398, 189), display_val, font=font_led, fill=(239, 68, 68, 255))
        draw.text((538, 198), "kg", font=font_unit, fill=(239, 68, 68, 255))

        # Stable LED Lamp (394, 239)
        if stable:
            draw.ellipse([391, 236, 397, 242], fill=(16, 185, 129, 255))
            draw.text((402, 234), "STABLE", font=font_status, fill=(52, 211, 153, 255))
        else:
            draw.ellipse([391, 236, 397, 242], fill=(60, 60, 60, 255))
            draw.text((402, 234), "SETTLING...", font=font_status, fill=(251, 191, 36, 255))

        # Dynamic Hash Ticker
        hash_chunk = hex((0x3c8e41a0 + frame_idx * 19) & 0xffffffff)[2:].zfill(8)
        draw.text((1416, 472), f"SHA-256 Anti-Rollback Hash: {hash_chunk}...d910 (Tamper-Proof)", font=font_hash, fill=(168, 85, 247, 255))

        pipe.stdin.write(img_pil.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print(f"SUCCESS! Rendered crystal-clear master animated loop to: {OUTPUT_VIDEO_PATH}")

if __name__ == "__main__":
    main()
