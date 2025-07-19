from enum import Enum

# constants.py
DEBUG = False

try:
    with open("chi_50digits.txt") as f:
        chi = float(f.read().strip().split()[0])
except FileNotFoundError:
    chi = 1.071428  # Correct fallback approximation (1 + 1/14)


class State(Enum):
    HIDDEN = "hidden"
    SAFE = "safe"  # Alias for revealed safe cells
    MINE = "mine"
    CLUE = "clue"
