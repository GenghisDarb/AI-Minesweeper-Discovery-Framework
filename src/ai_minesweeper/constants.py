from decimal import Decimal, getcontext
from enum import Enum
from pathlib import Path

# Global debug toggle
DEBUG = False

"""Global constants for the framework.

Canonical χ is loaded from data/chi_50digits.txt (≈ ln φ ≈ 0.4812118…).
We keep Decimal for precision and provide float/string adapters for consumers.
"""

# High precision for Decimal math
getcontext().prec = 64

# Resolve repository root and file path robustly
_HERE = Path(__file__).resolve()
_ROOT = _HERE.parents[2]  # repo root (…/AI-Minesweeper-Discovery-Framework)
_CHI_FILE = _ROOT / "data" / "chi_50digits.txt"

# Fallback to known ln(phi) value if file cannot be read
_CHI_FALLBACK = Decimal("0.48121182505960344749775891342436842313518433438566051966")

def _load_chi_decimal() -> Decimal:
    try:
        txt = _CHI_FILE.read_text(encoding="utf-8").strip()
        # Guard against empty/invalid content
        if not txt:
            return _CHI_FALLBACK
        return Decimal(txt)
    except Exception:
        return _CHI_FALLBACK

CHI: Decimal = _load_chi_decimal()
CHI_F32: float = float(CHI)            # float for numpy/UI
CHI_STR6: str = f"{CHI_F32:.6f}"       # short string for sidebar/UI

# Backward-compat: legacy lowercase 'chi' used in a few places
chi = CHI_F32


class State(Enum):
    HIDDEN = "hidden"
    SAFE = "safe"  # Alias for revealed safe cells
    MINE = "mine"
    CLUE = "clue"

__all__ = ["DEBUG", "CHI", "CHI_F32", "CHI_STR6", "chi", "State"]
