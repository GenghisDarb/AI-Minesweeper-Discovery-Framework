#!/bin/bash
set -euo pipefail

WHITEPAPER="AI Minesweeper Discovery Framework.docx"
cp "../$WHITEPAPER" docs/whitepaper.docx
if command -v pandoc >/dev/null; then
  pandoc docs/whitepaper.docx -o docs/whitepaper.md
  pandoc docs/whitepaper.docx -o docs/whitepaper.pdf
fi
