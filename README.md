# AI Minesweeper Discovery Framework

A constraint-satisfaction engine that turns any knowledge domain into a Minesweeper-style board of hypotheses and uncovers true patterns through active learning loops.

## Core Modules

| Module         | Purpose                                                      |
| -------------- | ------------------------------------------------------------ |
| BoardBuilder   | Ingests domain relations & builds cell network               |
| ClickEngine    | Propagates constraints, reveals safe cells                   |
| RiskAssessor   | Scores unknown cells for next probe                          |

## White-paper

See `docs/whitepaper.pdf` for the full technical overview.

## Quick Start

```bash
git clone https://github.com/<your-handle>/ai-minesweeper-framework.git
cd ai-minesweeper-framework
pip install -e .
pytest
```

## Project Structure

```
/AI-Minesweeper-Discovery-Framework/
├── README.md
├── docs/
│   └── whitepaper.pdf
├── src/
│   └── ai_minesweeper/
│       ├── __init__.py
│       ├── cell.py
│       └── board.py
└── tests/
    └── test_board_attrs.py
    └── test_board_functions.py
```

## Project Configuration

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-minesweeper"
version = "0.1.0"
description = "AI Minesweeper Discovery Framework"
authors = [
    { name = "Your Name", email = "your@email.com" }
]
readme = "README.md"
requires-python = ">=3.8"
license = { file = "LICENSE" }
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest",
    "coverage",
    "ruff",
    "mkdocs",
    "mkdocstrings[python]"
]

[project.scripts]
minesweeper = "ai_minesweeper.cli:app"
```

*This project is MIT licensed.*