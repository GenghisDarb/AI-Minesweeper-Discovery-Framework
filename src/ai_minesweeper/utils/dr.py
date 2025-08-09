import os
import random

_SEED = int(os.getenv("AI_MS_SEED", "1337"))
_rng = random.Random(_SEED)

def rng() -> random.Random:
    return _rng

def dr_sort(cells):
    return sorted(cells, key=lambda c: (
        getattr(c, "row", c[0] if isinstance(c, tuple) and len(c) == 2 else 0),
        getattr(c, "col", c[1] if isinstance(c, tuple) and len(c) == 2 else 0),
    ))
