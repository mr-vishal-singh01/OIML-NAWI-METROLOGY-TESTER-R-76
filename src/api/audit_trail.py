"""
Immutable SHA-256 Merkle Chained Audit Trail Engine
Conforming to WELMEC Guide 7.2 (Extension L - Long-Term Storage) & ISO/IEC 17025
SIH26035: Non-Automatic Weighing Instruments Automated Test System
"""

import hashlib
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

class AuditEvent:
    def __init__(
        self,
        event_index: int,
        timestamp_iso: str,
        operator_id: str,
        action: str,
        payload: Dict[str, Any],
        prev_hash: str
    ):
        self.event_index = event_index
        self.timestamp_iso = timestamp_iso
        self.operator_id = operator_id
        self.action = action
        self.payload = payload
        self.prev_hash = prev_hash
        self.event_hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Computes SHA-256 hash across canonical serialized fields.
        Guarantees zero ambiguity in key sorting or whitespaces.
        """
        canonical_payload = json.dumps(self.payload, sort_keys=True)
        hash_input = f"{self.event_index}|{self.timestamp_iso}|{self.operator_id}|{self.action}|{canonical_payload}|{self.prev_hash}"
        return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_index": self.event_index,
            "timestamp_iso": self.timestamp_iso,
            "operator_id": self.operator_id,
            "action": self.action,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "event_hash": self.event_hash
        }


class ImmutableAuditTrail:
    """
    Manages an append-only, cryptographically chained audit log for metrological testing.
    Any attempt to retroactively modify an observation breaks the hash chain immediately.
    """
    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self.chain: List[AuditEvent] = []

    def log_action(self, operator_id: str, action: str, payload: Dict[str, Any]) -> AuditEvent:
        prev_hash = self.chain[-1].event_hash if self.chain else self.GENESIS_HASH
        event_index = len(self.chain) + 1
        timestamp_iso = datetime.now(timezone.utc).isoformat() + "Z"

        event = AuditEvent(
            event_index=event_index,
            timestamp_iso=timestamp_iso,
            operator_id=operator_id,
            action=action,
            payload=payload,
            prev_hash=prev_hash
        )
        self.chain.append(event)
        return event

    def verify_integrity(self) -> Tuple[bool, Optional[str]]:
        """
        Validates cryptographic integrity of the entire chain from Genesis to tip.
        """
        if not self.chain:
            return True, None

        expected_prev = self.GENESIS_HASH
        for idx, event in enumerate(self.chain):
            # Check previous hash link
            if event.prev_hash != expected_prev:
                return False, f"Broken link at event #{event.event_index}: prev_hash mismatch"

            # Check internal hash calculation
            recomputed = event.compute_hash()
            if event.event_hash != recomputed:
                return False, f"Tampered event payload at event #{event.event_index}: hash discrepancy"

            expected_prev = event.event_hash

        return True, None


if __name__ == "__main__":
    audit = ImmutableAuditTrail()
    audit.log_action("RRSL_TECH_04", "INITIALIZE_TEST", {"model": "Essae-DS852", "serial": "SN-9941"})
    audit.log_action("RRSL_TECH_04", "RECORD_STEP", {"step": 1, "load": "500.0", "indication": "500.0", "delta_l": "0.5"})
    
    valid, err = audit.verify_integrity()
    print(f"Chain Integrity: {valid} (Error: {err})")
    print(f"Latest Chained Hash: {audit.chain[-1].event_hash}")
