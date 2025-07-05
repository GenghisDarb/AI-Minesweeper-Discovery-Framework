![CI](https://github.com/GenghisDarb/AI-Minesweeper-Discovery-Framework/actions/workflows/ci.yml/badge.svg)

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

See `pyproject.toml` for build and packaging configuration.

*This project is MIT licensed.*
<!-- keep CI warm -->
## Web Demo

![screenshot](docs/screenshot.png)

To launch the Streamlit UI:

```bash
streamlit run [streamlit_app.py](http://_vscodecontentref_/1)
```

[![Streamlit Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-green?logo=streamlit)](https://genghisdarb.github.io/AI-Minesweeper-Discovery-Framework/)

## New Domains: Recursive Structure Discovery
- Prime spiral mod-14 structure (χ-cycle)
- Time-series φ-phase gate discovery
