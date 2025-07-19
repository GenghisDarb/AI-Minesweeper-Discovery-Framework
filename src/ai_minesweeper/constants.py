from enum import Enum

# constants.py
DEBUG = False

try:
    with open("chi_50digits.txt") as f:
        chi = float(f.read().strip().split()[0])
except FileNotFoundError:
    chi = 0.785398  # π/4 as fallback approximation


class State(Enum):
    HIDDEN = "hidden"
    SAFE = "safe"  # Alias for revealed safe cells
    MINE = "mine"
    CLUE = "clue"
