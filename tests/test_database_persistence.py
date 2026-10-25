"""
Test suite for SQLite WAL persistence repository.
Verifies WAL mode, foreign keys, and restart persistence.
"""

import unittest
import tempfile
import sqlite3
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api.database import DatabaseRepository, get_connection


class TestDatabasePersistence(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "test_wal.db"
        self.repo = DatabaseRepository(self.db_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_wal_mode_and_foreign_keys_enabled(self):
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("PRAGMA journal_mode;")
        mode = cur.fetchone()[0]
        self.assertEqual(mode.lower(), "wal")

        cur.execute("PRAGMA foreign_keys;")
        fk = cur.fetchone()[0]
        self.assertEqual(fk, 1)
        conn.close()

    def test_session_and_observation_persistence(self):
        snap = {
            "snapshot_id": "INST-001",
            "manufacturer": "Essae",
            "model": "DS-852",
            "serial_number": "SN-001",
            "accuracy_class": "Class III",
            "max_capacity": "15000",
            "min_capacity": "100",
            "e": "5",
            "d": "5",
            "unit": "g",
            "testing_context": "Initial Verification"
        }
        self.repo.save_instrument_snapshot(snap)

        self.repo.save_session_state(
            session_id="SESS-001",
            instrument_id="INST-001",
            current_revision=1,
            completion_status="IN_PROGRESS",
            review_status="DRAFT",
            instrument_verdict="PASSED",
            zero_error_e0="0.0",
            engine_version="v1.0"
        )

        obs = {
            "observation_id": "OBS-001",
            "step_index": 1,
            "load": "2500.0",
            "indication": "2500.0",
            "delta_l": "1.5",
            "direction": "ascending",
            "operator_id": "OP1",
            "revision": 1,
            "timestamp_iso": "2026-09-11T12:00:00Z"
        }
        calc = {
            "calculation_id": "CALC-001",
            "observation_id": "OBS-001",
            "observation_revision": 1,
            "step_index": 1,
            "p": "2501.0",
            "raw_error_e": "1.0",
            "corrected_error_ec": "1.0",
            "mpe": "2.5",
            "passed": True,
            "deviation": "0.0",
            "derivation": {"rule": "Table 6"},
            "is_stale": False,
            "calculated_at_iso": "2026-09-11T12:00:00Z"
        }
        self.repo.record_observation_and_calc("SESS-001", obs, calc)

        # Reopen connection (simulating clean server restart)
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sessions WHERE session_id = 'SESS-001'")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["current_revision"], 1)
        self.assertEqual(row["review_status"], "DRAFT")

        cur.execute("SELECT * FROM observations WHERE session_id = 'SESS-001'")
        obs_row = cur.fetchone()
        self.assertEqual(obs_row["load"], "2500.0")

        cur.execute("SELECT * FROM calculations WHERE session_id = 'SESS-001'")
        calc_row = cur.fetchone()
        self.assertEqual(calc_row["corrected_error_ec"], "1.0")
        self.assertEqual(calc_row["passed"], 1)
        conn.close()


if __name__ == "__main__":
    unittest.main()
