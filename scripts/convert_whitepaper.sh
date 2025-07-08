#!/bin/bash
set -euo pipefail

WHITEPAPER="AI Minesweeper Discovery Framework.docx"
cp "$WHITEPAPER" docs/whitepaper.docx

if ! command -v xelatex >/dev/null; then
  echo "XeLaTeX is not installed. Attempting to install..."
  if command -v apt-get >/dev/null; then
    sudo apt-get update && sudo apt-get install -y texlive-xetex
  else
    echo "Please install XeLaTeX manually to enable PDF generation."
    exit 1
  fi
fi

if command -v pandoc >/dev/null; then
  pandoc docs/whitepaper.docx -o docs/whitepaper.md
  pandoc docs/whitepaper.docx -o docs/whitepaper.pdf
else
  echo "Pandoc is not installed. Please install it to enable document conversion."
  exit 1
fi
