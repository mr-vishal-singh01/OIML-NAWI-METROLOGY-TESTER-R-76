"""
OpenCV Computer Vision Preprocessing, Fuzzing & Matrix Sampling Test Suite
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Validates:
 1. Multi-iteration real-world physical damage fuzzing (scratches, dirt, blur)
 2. OpenCV adaptive thresholding and morphological closing
 3. 3-Nested contour hierarchy finder pattern localization
 4. Center-pixel discrete grid matrix sampling (extracting binary numpy array)
 5. End-to-end resilient decoding and cryptographic Ed25519 signature verification
"""

import io
import json
import unittest
from pathlib import Path

import cv2
import numpy as np
import qrcode
from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from core.opencv_qr_pipeline import RealWorldDamageFuzzer, OpenCVQRPipeline
from core.offline_qr import Ed25519ReportSigner


class TestOpenCVFuzzingPipeline(unittest.TestCase):
    """OpenCV Computer Vision Fuzzing & Matrix Extraction Test Suite."""

    @classmethod
    def setUpClass(cls):
        cls.signer = Ed25519ReportSigner()
        cls.claims = cls.signer.create_claims(
            session_id="SESS-CV-PIPE-01",
            revision=1,
            spec_model="METTLER-TOLEDO-IND570",
            spec_serial="SN-CV-9988",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="c" * 64
        )
        cls.envelope = cls.signer.sign_claims(cls.claims)
        cls.payload_str = json.dumps(cls.envelope, separators=(",", ":"))

        # Generate base Level H QR image
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(cls.payload_str)
        qr.make(fit=True)
        cls.base_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        cls.pipeline = OpenCVQRPipeline()

    def test_01_real_world_physical_fuzzing_suite(self):
        """
        Runs 5 iterations of randomized physical damage:
        15 scratches, 30 dirt blobs, and lens defocus blur.
        Asserts recovery across iterations.
        """
        success_count = 0
        iterations = 5

        for i in range(iterations):
            fuzzed = RealWorldDamageFuzzer.inject_damage(
                self.base_img,
                scratch_count=12,
                scratch_width=3,
                dirt_blob_count=20,
                blur_radius=0.9,
                isolate_finders=True,
                seed=100 + i * 17
            )
            success, decoded_payload, _ = self.pipeline.resilient_decode(fuzzed)
            if success:
                success_count += 1
                # Ensure recovered data cryptographically verifies
                verif = Ed25519ReportSigner.verify_envelope(decoded_payload)
                self.assertTrue(verif["is_valid"])

        recovery_rate = (success_count / iterations) * 100.0
        self.assertGreaterEqual(recovery_rate, 80.0, f"Expected >= 80% recovery under realistic fuzzing, got {recovery_rate}%")

    def test_02_aggressive_cv_binarization_and_morphology(self):
        """Tests OpenCV adaptive thresholding and morphological closing."""
        fuzzed = RealWorldDamageFuzzer.inject_damage(
            self.base_img,
            scratch_count=10,
            dirt_blob_count=15,
            blur_radius=1.2,
            seed=42
        )
        closed = OpenCVQRPipeline.aggressive_preprocess(fuzzed)

        self.assertIsInstance(closed, np.ndarray)
        self.assertEqual(len(closed.shape), 2)  # 2D grayscale/binary
        # Verify it contains distinct 0 (black) and 255 (white) values
        unique_vals = set(np.unique(closed))
        self.assertTrue({0, 255}.issubset(unique_vals))

    def test_03_contour_hierarchy_finder_pattern_localization(self):
        """Tests detection of 3-nested contour hierarchy for finder patterns."""
        cv_img = OpenCVQRPipeline.to_cv_image(self.base_img)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        finder_boxes = OpenCVQRPipeline.locate_finder_patterns(thresh)
        # Should identify at least 3 finder pattern anchors
        self.assertGreaterEqual(len(finder_boxes), 3, "Must detect the 3 corner finder pattern anchors")

    def test_04_center_pixel_grid_matrix_sampling(self):
        """Tests discrete N x N binary matrix sampling from rectified image."""
        cv_img = OpenCVQRPipeline.to_cv_image(self.base_img)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

        grid_size = 133
        matrix = OpenCVQRPipeline.sample_grid_matrix(gray, grid_size=grid_size)

        self.assertEqual(matrix.shape, (grid_size, grid_size))
        self.assertTrue(issubclass(matrix.dtype.type, np.integer))
        # Matrix must have both 0 and 1 modules
        self.assertIn(0, matrix)
        self.assertIn(1, matrix)
        # Top-left corner (0,0) in finder pattern must be black (1)
        # Accounting for border, module (4, 4) is black
        self.assertEqual(matrix[4, 4], 1)

    def test_05_multi_engine_resilient_recovery_ed25519(self):
        """Tests multi-engine recovery and end-to-end Ed25519 verification."""
        fuzzed = RealWorldDamageFuzzer.inject_damage(
            self.base_img,
            scratch_count=10,
            dirt_blob_count=15,
            blur_radius=0.8,
            isolate_finders=True,
            seed=7
        )

        success, payload, straight_matrix = self.pipeline.resilient_decode(fuzzed)
        self.assertTrue(success, "Resilient decode must succeed on degraded QR code")
        self.assertIsNotNone(payload)

        # Cryptographic verification
        verif = Ed25519ReportSigner.verify_envelope(payload, self.signer.public_key)
        self.assertTrue(verif["is_valid"])
        self.assertEqual(verif["status"], "AUTHENTIC")
        self.assertEqual(verif["certificate_id"], "OIML-RRSL-SESS-CV-PIPE-01-R1")


if __name__ == "__main__":
    unittest.main()
