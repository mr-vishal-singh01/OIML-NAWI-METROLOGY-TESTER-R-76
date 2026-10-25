"""
QR Code Reed-Solomon Degradation & Optical Resilience Benchmark
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Tests optical scannability under controlled physical damage (Level H, 30% error recovery).
Demonstrates Reed-Solomon error correction boundaries and finder pattern isolation.
"""

import io
import json
from pathlib import Path
from typing import Optional, Tuple

import qrcode
from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode


def test_qr_resilience(
    payload_data: str,
    damage_percentage: float = 0.20,
    output_path: Optional[str] = "damaged_qr_test.png"
) -> bool:
    """
    Generates a Level H (30% recovery) QR code, intentionally damages it with a black
    rectangle over the center-right (avoiding the 3 corner finder patterns), and tests scannability.
    """
    # 1. Generate QR Code with Maximum Error Correction (Level H - 30%)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 2. Calculate Damage Box Size
    width, height = img.size
    # We want the area of the damage box to be a percentage of the total area
    damage_area = (width * height) * damage_percentage
    box_side = int(damage_area ** 0.5)

    # 3. Apply the Damage (Draw a black rectangle over the center-right)
    # Avoid hitting all three of the large square finder patterns in the corners
    draw = ImageDraw.Draw(img)
    start_x = width // 2
    start_y = height // 2
    draw.rectangle(
        [start_x, start_y, start_x + box_side, start_y + box_side],
        fill="black"
    )

    # Save the damaged image for visual inspection
    if output_path:
        img.save(output_path)
        print(f"Damaged QR code saved to {output_path}. Damage area: ~{damage_percentage*100:.1f}%")

    # 4. Attempt to Decode the Damaged Image
    decoded_objects = decode(img)

    if decoded_objects:
        recovered_data = decoded_objects[0].data.decode('utf-8')
        print("✅ SCAN SUCCESS! Reed-Solomon correction recovered the data.")
        print(f"Recovered Payload: {recovered_data[:60]}...")
        return True
    else:
        print("❌ SCAN FAILED! The damage exceeded the error correction capacity.")
        return False


def test_qr_resilience_isolated_finders(
    payload_data: str,
    damage_percentage: float = 0.20,
    output_path: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Precision degradation tester that strictly isolates the three corner finder patterns
    (top-left, top-right, bottom-left) by placing the damage rectangle squarely in the center data zone.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    width, height = img.size
    damage_area = (width * height) * damage_percentage
    box_side = int(damage_area ** 0.5)

    draw = ImageDraw.Draw(img)
    cx, cy = width // 2, height // 2
    half = box_side // 2
    draw.rectangle([cx - half, cy - half, cx + half, cy + half], fill="black")

    if output_path:
        img.save(output_path)

    decoded = decode(img)
    if decoded:
        return True, decoded[0].data.decode("utf-8")
    return False, None


# Disable pytest collection for utility functions
test_qr_resilience.__test__ = False
test_qr_resilience_isolated_finders.__test__ = False


if __name__ == "__main__":
    print("==========================================================")
    print("QR REED-SOLOMON DEGRADATION BENCHMARK (LEVEL H - 30%)")
    dummy_payload = '{"iss":"RRSL","cert_id":"OIML-01","sig":"Base64URL_Signature_String"}'
    print("\n--- Test 1: User Specification Nominal Test (20% Damage) ---")
    res = test_qr_resilience(dummy_payload, damage_percentage=0.20)
    print(f"Test result: {res}")
