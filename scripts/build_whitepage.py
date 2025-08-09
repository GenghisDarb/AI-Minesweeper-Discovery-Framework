import os
import subprocess
import os
import subprocess
from pathlib import Path


def build_whitepaper() -> Path:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "docs" / "whitepaper_src"
    output_pdf = root / "docs" / "whitepaper.pdf"

    parts = [
        src_dir / "whitepage.md",
    ]
    # Optionally include more theory files if present
    optional_parts = [
        root / "docs" / "torus_of_tori_and_dpp14.md",
        root / "docs" / "prime_spirals.md",
        root / "docs" / "confidence_osc.md",
    ]
    parts.extend(p for p in optional_parts if p.exists())

    for p in parts:
        if not p.exists():
            raise FileNotFoundError(f"Missing source part: {p}")

    cmd = [
        "pandoc",
        "--from",
        "markdown+footnotes+link_attributes",
        "--pdf-engine=xelatex",
        "-V",
        "geometry:margin=1in",
        "-V",
        "mainfont=DejaVu Serif",
        "-o",
        str(output_pdf),
        *[str(p) for p in parts],
    ]
    subprocess.run(cmd, check=True)
    return output_pdf


if __name__ == "__main__":
    out = build_whitepaper()
    print(f"Whitepaper built successfully: {out}")
