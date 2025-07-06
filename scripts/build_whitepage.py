import subprocess
import os

def build_whitepage():
    src_path = "docs/whitepaper_src/whitepage.md"
    output_path = "docs/whitepage.pdf"

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")

    command = [
        "pandoc",
        src_path,
        "-o",
        output_path
    ]

    subprocess.run(command, check=True)
    print(f"White-paper built successfully: {output_path}")

if __name__ == "__main__":
    build_whitepage()
