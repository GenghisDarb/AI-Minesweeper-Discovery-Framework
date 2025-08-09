#!/bin/bash
set -euo pipefail

if ! command -v pandoc >/dev/null; then
  echo "Pandoc is not installed. Please install it to enable document conversion."
  exit 1
fi
if ! command -v xelatex >/dev/null; then
  echo "XeLaTeX is not installed. Please install texlive-xetex (or equivalent)."
  exit 1
fi

python3 scripts/build_whitepage.py
