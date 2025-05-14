from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Constraint:
    revealed: tuple[int, int]
    hidden:   tuple[tuple[int, int], ...]
    mines:    int
