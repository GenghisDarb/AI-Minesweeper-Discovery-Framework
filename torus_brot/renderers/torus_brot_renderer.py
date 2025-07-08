"""
Render TORUS-brot fractal.
Usage: `python torus_brot_renderer.py --out image.png`
"""
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import hashlib

def torus_brot(z0, max_iter=512, escape=4.0):
    z = complex(z0)
    for n in range(max_iter):
        z = (abs(z.real) + 1j * abs(z.imag))**2 + z0
        if abs(z) > escape:
            return n
    return max_iter

def render_grid(n=400):
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    grid = np.zeros((n, n))
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            grid[j, i] = torus_brot(complex(xi, yj))
    return grid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="torus_brot.png", help="Output image filename")
    args = parser.parse_args()

    img = render_grid(n=400)
    plt.imshow(img, cmap="inferno", extent=[-2, 2, -2, 2])
    plt.axis("off")
    plt.title("TORUS-brot demo")
    outfile = pathlib.Path(args.out)
    plt.savefig(outfile, dpi=300)

    hash = hashlib.sha256(outfile.read_bytes()).hexdigest()
    print(f"✓ saved {outfile}  sha256:{hash}")
