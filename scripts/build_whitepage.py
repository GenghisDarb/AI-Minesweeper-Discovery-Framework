import os
import subprocess


def build_whitepage():
    src_path = "docs/whitepaper_src/whitepage.md"
    output_path = "docs/whitepage.pdf"

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")

    # Use an alternative PDF engine if pdflatex is missing
    command = [
        "pandoc",
        src_path,
        "-o",
        output_path,
        "--pdf-engine=xelatex",  # Alternative engine
    ]

    subprocess.run(command, check=True)
    print(f"White-paper built successfully: {output_path}")


if __name__ == "__main__":
    build_whitepage()
