#!/usr/bin/env python3
"""
Unit test suite verifying citizen one-time registration,
multi-credential authentication (Username, ID, Phone, Email),
and legal report verification under Section 15 of Legal Metrology Act, 2009.
"""

import unittest
from fastapi.testclient import TestClient
try:
    from api.main import app
except ImportError:
    from backend.api.main import app

class TestCitizenAuthAndVerification(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_citizen_registration_password_mismatch(self):
        res = self.client.post("/api/citizen/register", json={
            "name": "Test Citizen",
            "phone": "9998887771",
            "address": "Zone 2, Delhi Mandi",
            "email": "mismatch@test.com",
            "username": "mismatch_user",
            "password": "Password123",
            "confirm_password": "WrongPassword456"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Passwords do not match", res.json()["detail"])

    def test_02_citizen_registration_and_multi_credential_login(self):
        import secrets
        rnd = secrets.token_hex(3)
        username = f"trader_{rnd}"
        phone = f"987{secrets.token_hex(3)[:7]}"
        email = f"trader_{rnd}@mandi.in"

        # 1. Register
        res_reg = self.client.post("/api/citizen/register", json={
            "name": "Manoj Kumar Traders",
            "phone": phone,
            "address": "Grain Market Shop 45, APMC, Pune",
            "email": email,
            "username": username,
            "password": "SecurePassword#2026",
            "confirm_password": "SecurePassword#2026"
        })
        self.assertEqual(res_reg.status_code, 200)
        data_reg = res_reg.json()
        self.assertEqual(data_reg["status"], "success")
        citizen_id = data_reg["citizen"]["citizen_id"]
        self.assertTrue(citizen_id.startswith("CIT-2026-"))

        # 2. Login using Username
        res_log_user = self.client.post("/api/citizen/login", json={
            "identifier": username,
            "password": "SecurePassword#2026"
        })
        self.assertEqual(res_log_user.status_code, 200)
        self.assertTrue(res_log_user.json()["authenticated"])
        self.assertEqual(res_log_user.json()["role"], "CITIZEN")

        # 3. Login using Phone Number
        res_log_phone = self.client.post("/api/citizen/login", json={
            "identifier": phone,
            "password": "SecurePassword#2026"
        })
        self.assertEqual(res_log_phone.status_code, 200)
        self.assertTrue(res_log_phone.json()["authenticated"])

        # 4. Login using Email ID
        res_log_email = self.client.post("/api/citizen/login", json={
            "identifier": email,
            "password": "SecurePassword#2026"
        })
        self.assertEqual(res_log_email.status_code, 200)
        self.assertTrue(res_log_email.json()["authenticated"])

        # 5. Login using Citizen ID
        res_log_id = self.client.post("/api/citizen/login", json={
            "identifier": citizen_id,
            "password": "SecurePassword#2026"
        })
        self.assertEqual(res_log_id.status_code, 200)
        self.assertTrue(res_log_id.json()["authenticated"])

    def test_03_citizen_report_verification_endpoint(self):
        res = self.client.post("/api/citizen/verify-report", json={
            "query": "SESS-2026-001"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["verified"])
        self.assertIn("certificate", data)
        self.assertIn("verdict", data["certificate"])

if __name__ == "__main__":
    unittest.main()
