# constants.py
DEBUG = False

try:
    with open("data/chi_50digits.txt") as f:
        chi = float(f.read().strip().split()[0])
except FileNotFoundError:
<<<<<<< HEAD
    chi = 0.785398  # π/4 as fallback approximation


class State(Enum):
    HIDDEN = "hidden"
    SAFE = "safe"  # Alias for revealed safe cells
    MINE = "mine"
    CLUE = "clue"
=======
    chi = 1.071428  # Correct fallback approximation (1 + 1/14)
>>>>>>> origin/copilot/fix-66e80e14-9a03-42e2-940c-2e106230e889
