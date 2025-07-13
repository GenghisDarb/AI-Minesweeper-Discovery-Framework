# constants.py
DEBUG = False

try:
    with open("chi_50digits.txt") as f:
        chi = float(f.read().strip().split()[0])
except FileNotFoundError:
    chi = 0.792537  # fallback approximation

from enum import Enum

class State(Enum):
    HIDDEN = "hidden"
    SAFE = "safe"
    MINE = "mine"
    CLUE = "clue"
