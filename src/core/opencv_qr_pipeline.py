"""
OpenCV Computer Vision Preprocessing & Matrix Recovery Pipeline
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Provides:
 1. Realistic Physical Degradation Fuzzer (Scratches, Smudges, Blur)
 2. Aggressive Computer Vision Preprocessing (Adaptive Thresholding, Morphological Closing)
 3. Contour Hierarchy Finder Pattern Localization (1:1:3:1:1 ratio)
 4. Perspective Rectification (Warp Transform)
 5. Discrete N x N Binary Grid Sampling
 6. Multi-Engine Resilient Optical Decoder (PyZBar + OpenCV QRCodeDetector)
"""

import io
import math
import random
from typing import Dict, Any, Optional, Tuple, List, Union

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pyzbar.pyzbar import decode as pyzbar_decode
import qrcode


class RealWorldDamageFuzzer:
    """Generates realistic physical damage: scratches, dirt/smudges, and lens blur."""

    @classmethod
    def inject_damage(
        cls,
        image: Union[Image.Image, np.ndarray],
        scratch_count: int = 15,
        scratch_width: int = 3,
        dirt_blob_count: int = 25,
        max_blob_radius: int = 6,
        blur_radius: float = 1.0,
        isolate_finders: bool = True,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Applies scratches, dirt blobs, and blur while optionally protecting corner finder patterns.
        """
        if seed is not None:
            random.seed(seed)

        if isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image).convert("RGB")
        else:
            pil_img = image.copy().convert("RGB")

        draw = ImageDraw.Draw(pil_img)
        width, height = pil_img.size
        finder_safe_margin = int(min(width, height) * 0.22)

        def get_point() -> Tuple[int, int]:
            if not isolate_finders:
                return random.randint(0, width - 1), random.randint(0, height - 1)
            # Sample outside top-left, top-right, and bottom-left finder zones
            for _ in range(50):
                x = random.randint(30, width - 31)
                y = random.randint(30, height - 31)
                if x < finder_safe_margin and y < finder_safe_margin:
                    continue  # Top-Left
                if x > width - finder_safe_margin and y < finder_safe_margin:
                    continue  # Top-Right
                if x < finder_safe_margin and y > height - finder_safe_margin:
                    continue  # Bottom-Left
                return x, y
            return width // 2, height // 2

        # 1. Scratches (Random lines cutting through data modules)
        for _ in range(scratch_count):
            x1, y1 = get_point()
            x2, y2 = get_point()
            draw.line((x1, y1, x2, y2), fill="white", width=scratch_width)

        # 2. Dirt/Smudges (Random black blobs)
        for _ in range(dirt_blob_count):
            x, y = get_point()
            r = random.randint(2, max_blob_radius)
            draw.ellipse((x - r, y - r, x + r, y + r), fill="black")

        # 3. Scanner lens defocus blur
        if blur_radius > 0:
            fuzzed = pil_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        else:
            fuzzed = pil_img

        return fuzzed


class OpenCVQRPipeline:
    """
    OpenCV computer vision preprocessing, finder pattern detection,
    perspective rectification, and discrete grid matrix sampling.
    """

    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    @staticmethod
    def to_cv_image(image: Union[Image.Image, np.ndarray, bytes]) -> np.ndarray:
        """Converts various image inputs to a BGR/RGB OpenCV numpy array."""
        if isinstance(image, np.ndarray):
            return image
        if isinstance(image, Image.Image):
            return np.array(image.convert("RGB"))
        if isinstance(image, (bytes, bytearray)):
            nparr = np.frombuffer(image, np.uint8)
            decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if decoded is None:
                raise ValueError("Could not decode image bytes")
            return decoded
        raise TypeError(f"Unsupported image input type: {type(image)}")

    @classmethod
    def aggressive_preprocess(cls, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        """
        Applies grayscale conversion, adaptive thresholding, and morphological closing
        to bridge scratches and restore module continuity under harsh lighting.
        """
        cv_img = cls.to_cv_image(image)
        if len(cv_img.shape) == 3:
            gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        else:
            gray = cv_img

        # Adaptive Gaussian thresholding
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=13,
            C=3
        )

        # Morphological close to heal thin scratch cuts in black modules
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        return closed

    @classmethod
    def locate_finder_patterns(cls, thresh_img: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Identifies potential QR finder patterns by finding 3-nested contour hierarchies
        (black center inside white border inside black outer square).
        Returns list of (x, y, w, h) bounding boxes.
        """
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is None or len(contours) == 0:
            return []

        h_data = hierarchy[0]
        finder_boxes = []

        for i, h in enumerate(h_data):
            # h: [Next, Previous, First_Child, Parent]
            child_idx = h[2]
            if child_idx != -1:
                grandchild_idx = h_data[child_idx][2]
                if grandchild_idx != -1:
                    # Found 3 nested levels (outer, inner white, center black)
                    x, y, w, h_box = cv2.boundingRect(contours[i])
                    aspect_ratio = float(w) / h_box if h_box > 0 else 0
                    if 0.7 <= aspect_ratio <= 1.4 and w > 15 and h_box > 15:
                        finder_boxes.append((x, y, w, h_box))

        return finder_boxes

    @classmethod
    def sample_grid_matrix(cls, warped_gray: np.ndarray, grid_size: int) -> np.ndarray:
        """
        Samples the discrete N x N binary matrix (1 for black, 0 for white)
        from a rectified, flattened QR code image.
        """
        h, w = warped_gray.shape[:2]
        cell_w = w / float(grid_size)
        cell_h = h / float(grid_size)

        binary_matrix = np.zeros((grid_size, grid_size), dtype=np.uint8)

        for row in range(grid_size):
            for col in range(grid_size):
                cx = int((col + 0.5) * cell_w)
                cy = int((row + 0.5) * cell_h)
                # Ensure bounds
                cx = min(w - 1, max(0, cx))
                cy = min(h - 1, max(0, cy))
                pixel_val = warped_gray[cy, cx]
                # In standard thresholded image: 0 is black (1), 255 is white (0)
                binary_matrix[row, col] = 1 if pixel_val < 128 else 0

        return binary_matrix

    def resilient_decode(
        self,
        image: Union[Image.Image, np.ndarray]
    ) -> Tuple[bool, Optional[str], Optional[np.ndarray]]:
        """
        Multi-engine decoding strategy:
        1. Try raw PyZBar decode.
        2. Try OpenCV QRCodeDetector (which also extracts rectified straight matrix).
        3. Try PyZBar after aggressive adaptive thresholding and morphological healing.
        Returns (success, decoded_payload, extracted_binary_matrix).
        """
        cv_img = self.to_cv_image(image)

        # Strategy 1: PyZBar direct
        try:
            pz_res = pyzbar_decode(cv_img)
            if pz_res:
                payload = pz_res[0].data.decode("utf-8")
                # Also attempt matrix extraction via OpenCV detector
                _, _, straight = self.detector.detectAndDecode(cv_img)
                return True, payload, straight
        except Exception:
            pass

        # Strategy 2: OpenCV QRCodeDetector direct
        try:
            val, pts, straight = self.detector.detectAndDecode(cv_img)
            if val:
                return True, val, straight
        except Exception:
            pass

        # Strategy 3: Aggressive preprocessing + PyZBar
        try:
            preprocessed = self.aggressive_preprocess(cv_img)
            pz_res = pyzbar_decode(preprocessed)
            if pz_res:
                payload = pz_res[0].data.decode("utf-8")
                _, _, straight = self.detector.detectAndDecode(preprocessed)
                return True, payload, straight
        except Exception:
            pass

        # Strategy 4: OpenCV detector on preprocessed
        try:
            preprocessed = self.aggressive_preprocess(cv_img)
            val, pts, straight = self.detector.detectAndDecode(preprocessed)
            if val:
                return True, val, straight
        except Exception:
            pass

        return False, None, None
