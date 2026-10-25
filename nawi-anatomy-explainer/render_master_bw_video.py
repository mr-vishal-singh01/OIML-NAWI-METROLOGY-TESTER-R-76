import os
import math
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# Load the rendered black-and-white plate
card_img_path = os.path.expanduser("~/Desktop/SIH_NAWI_Anatomy_BW.png")
if not os.path.exists(card_img_path):
    print("Base screenshot not found!")
    exit(1)

base = Image.open(card_img_path).convert("RGB")
W, H = 1920, 1080

# Create 1920x1080 paper-white canvas (#f2f2ef)
canvas = Image.new("RGB", (W, H), (242, 242, 239))

# Center the card
scale_factor = min((W - 80) / base.width, (H - 80) / base.height)
new_w = int(base.width * scale_factor)
new_h = int(base.height * scale_factor)
resized_card = base.resize((new_w, new_h), Image.Resampling.LANCZOS)

offset_x = (W - new_w) // 2
offset_y = (H - new_h) // 2
canvas.paste(resized_card, (offset_x, offset_y))

# Add title banner at top
draw = ImageDraw.Draw(canvas)
font_path = os.path.expanduser("~/.local/share/fonts/JetBrainsMonoNerdFontMono-ExtraBold.ttf")
if not os.path.exists(font_path):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

try:
    font_title = ImageFont.truetype(font_path, 22)
    font_sub = ImageFont.truetype(font_path, 14)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

draw.text((offset_x, offset_y - 34), "PRECISIONX (SIH26035) · NON-AUTOMATIC WEIGHING INSTRUMENT (NAWI) OIML R-76 ARCHITECTURE", fill=(38, 38, 42), font=font_title)
draw.text((offset_x, offset_y + new_h + 12), "Direct RS-232 Intercept ▸ Zero Operator Wait/Tampering ▸ On-Chip Ed25519 Cryptographic Proof ▸ Offline QR Token", fill=(138, 138, 143), font=font_sub)

# Prepare frames for video loop (180 frames = 6 seconds at 30 fps)
TOTAL_FRAMES = 180
FPS = 30
OUT_MP4_1 = os.path.expanduser("~/Desktop/SIH_NAWI_BW_Loop.mp4")
OUT_MP4_2 = os.path.expanduser("~/Desktop/SIH_NAWI_Background_Loop.mp4")

# Use ffmpeg pipe for ultra-fast high-quality encoding
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "bgr24",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    OUT_MP4_1
]

proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

np_canvas = np.array(canvas)[:, :, ::-1].copy() # BGR

for f in range(TOTAL_FRAMES):
    frame = np_canvas.copy()
    
    # Pulse effect on dongle indicator and flow line
    phase = (f / 30.0) * math.pi * 2
    glow = int(128 + 120 * math.sin(phase))
    
    # Send frame
    proc.stdin.write(frame.tobytes())

proc.stdin.close()
proc.wait()

print(f"Generated {OUT_MP4_1}")
# Copy to background loop as well
import shutil
shutil.copyfile(OUT_MP4_1, OUT_MP4_2)
print(f"Updated {OUT_MP4_2}")
