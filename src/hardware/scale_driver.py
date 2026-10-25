"""
Hardware Interface Driver & Serial Stream Parser
SIH26035: Non-Automatic Weighing Instruments Automated Test System
Supports RS-232, USB Virtual COM, and WebSerial continuous weight ingestion
Supported Protocols: MT-SICS (Mettler Toledo), SMA Protocol, Generic ASCII Continuous
"""

import re
from decimal import Decimal
from typing import Dict, Any, Optional

class ScaleStreamParser:
    """
    Parses live string streams received from laboratory balances and industrial scales.
    Eliminates human transcription errors during OIML testing.
    """

    @staticmethod
    def parse_mt_sics(raw_line: str) -> Optional[Dict[str, Any]]:
        """
        Parses Mettler Toledo Standard Interface Command Set (MT-SICS) response.
        Example: 'S S      100.00 g' (Stable 100.00 g)
                 'S D      100.00 g' (Dynamic / Unstable 100.00 g)
        """
        clean = raw_line.strip()
        # Regex for MT-SICS S response
        match = re.match(r"^S\s+([SDI])\s+([+-]?\d+\.?\d*)\s*([a-zA-Z]+)?", clean)
        if match:
            status_char, val_str, unit_str = match.groups()
            return {
                "protocol": "MT-SICS",
                "is_stable": status_char == "S",
                "indicated_value": Decimal(val_str),
                "unit": unit_str or "g",
                "raw": clean
            }
        return None

    @staticmethod
    def parse_generic_ascii(raw_line: str) -> Optional[Dict[str, Any]]:
        """
        Parses common industrial scale continuous stream format (CAS, Essae, Avery).
        Example: 'ST,GS,+00100.0,g' or 'US,NT,+00050.2,kg'
        """
        clean = raw_line.strip()
        parts = [p.strip() for p in clean.split(",")]
        if len(parts) >= 3:
            status_code = parts[0]
            val_match = re.search(r"([+-]?\d+\.?\d*)", parts[2])
            if val_match:
                val = Decimal(val_match.group(1))
                unit = parts[3] if len(parts) > 3 else "g"
                return {
                    "protocol": "Generic-ASCII",
                    "is_stable": "ST" in status_code.upper(),
                    "indicated_value": val,
                    "unit": unit,
                    "raw": clean
                }
    @staticmethod
    def parse_sma(raw_line: str) -> Optional[Dict[str, Any]]:
        """
        Parses Scale Manufacturers Association (SMA) standard stream format.
        Example: '<LF>11000000000002500000lb<CR>' or 'SMA: 11000000000002500.0g'
        Field 1: Scale status (1=Gross, 2=Net)
        Field 2: Stability (1=Stable, 2=In motion, 3=Error)
        """
        clean = raw_line.strip()
        sma_match = re.match(r"^(?:SMA:?\s*)?([12])([123])(\d{10,12}(?:\.\d+)?)\s*([a-zA-Z]+)?", clean)
        if sma_match:
            mode_char, motion_char, val_str, unit_str = sma_match.groups()
            try:
                # Value could be integer with implicit or explicit decimal
                val = Decimal(val_str)
                # If value is huge without dot (e.g. 10 digits representing 2500.00)
                if "." not in val_str and len(val_str) >= 6:
                    val = Decimal(val_str) / Decimal("100")
            except Exception:
                val = Decimal("0")
            return {
                "protocol": "SMA-Standard",
                "is_stable": motion_char == "1",
                "indicated_value": val,
                "unit": unit_str or "g",
                "raw": clean
            }
        return None

    @classmethod
    def parse_stream(cls, raw_line: str) -> Dict[str, Any]:
        """Auto-detects format and extracts stabilized weight."""
        res = cls.parse_mt_sics(raw_line)
        if res:
            return res
        res = cls.parse_generic_ascii(raw_line)
        if res:
            return res
        res = cls.parse_sma(raw_line)
        if res:
            return res
        
        # Fallback: simple numeric extraction
        num_match = re.search(r"([+-]?\d+\.?\d*)", raw_line)
        if num_match:
            return {
                "protocol": "Raw-Fallback",
                "is_stable": True,
                "indicated_value": Decimal(num_match.group(1)),
                "unit": "g",
                "raw": raw_line.strip()
            }

        return {
            "protocol": "Unknown",
            "is_stable": False,
            "indicated_value": Decimal("0"),
            "unit": "g",
            "raw": raw_line.strip()
        }


class MockScaleSimulator:
    """Simulates a connected laboratory balance over virtual serial for demo/testing."""

    @staticmethod
    def generate_mt_sics_reading(weight: Decimal, stable: bool = True, unit: str = "g") -> str:
        status = "S" if stable else "D"
        return f"S {status}      {weight:8.2f} {unit}\r\n"

    @staticmethod
    def generate_continuous_ascii(weight: Decimal, stable: bool = True, unit: str = "g") -> str:
        st = "ST" if stable else "US"
        sign = "+" if weight >= 0 else "-"
        return f"{st},GS,{sign}{abs(weight):07.2f},{unit}\r\n"

    @staticmethod
    def generate_settling_sequence(target_weight: Decimal, protocol: str = "mt_sics", unit: str = "g") -> list:
        """
        Generates a realistic 6-step time series simulating physical mass placement:
        Transient oscillation -> Overshoot -> Damped vibration -> Lock at final stable weight.
        """
        # Multipliers representing physical settling curve
        oscillation_factors = [
            (Decimal("0.65"), False),  # Initial mass impact
            (Decimal("1.18"), False),  # Mechanical spring overshoot
            (Decimal("0.92"), False),  # Damped rebound
            (Decimal("1.04"), False),  # Small oscillation
            (Decimal("0.99"), False),  # Final creep settling
            (Decimal("1.00"), True),   # Stabilized locked reading
        ]
        sequence = []
        for factor, is_stable in oscillation_factors:
            current_w = (target_weight * factor).quantize(Decimal("0.1"))
            if protocol == "ascii":
                raw = MockScaleSimulator.generate_continuous_ascii(current_w, stable=is_stable, unit=unit)
            else:
                raw = MockScaleSimulator.generate_mt_sics_reading(current_w, stable=is_stable, unit=unit)
            sequence.append({
                "weight": float(current_w),
                "is_stable": is_stable,
                "raw": raw.strip(),
                "unit": unit
            })
        return sequence


if __name__ == "__main__":
    parser = ScaleStreamParser()
    sim = MockScaleSimulator()

    line1 = sim.generate_mt_sics_reading(Decimal("500.00"), stable=True)
    parsed1 = parser.parse_stream(line1)
    print("Parsed MT-SICS:", parsed1)

    line2 = sim.generate_continuous_ascii(Decimal("250.50"), stable=True)
    parsed2 = parser.parse_stream(line2)
    print("Parsed Generic ASCII:", parsed2)
