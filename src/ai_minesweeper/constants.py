# constants.py
DEBUG = False

try:
    with open("data/chi_50digits.txt") as f:
        chi = float(f.read().strip().split()[0])
except FileNotFoundError:
    chi = 1.071428  # Correct fallback approximation (1 + 1/14)
