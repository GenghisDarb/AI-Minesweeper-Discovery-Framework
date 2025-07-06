# AI Minesweeper Discovery Framework

[![CI](https://github.com/<org>/AI-Minesweeper-Discovery-Framework/actions/workflows/ci.yml/badge.svg)](https://github.com/<org>/AI-Minesweeper-Discovery-Framework/actions/workflows/ci.yml)
[![Test Coverage](https://coveralls.io/repos/github/<org>/AI-Minesweeper-Discovery-Framework/badge.svg)](https://coveralls.io/github/<org>/AI-Minesweeper-Discovery-Framework)
[![Evidence Sigma](https://img.shields.io/badge/evidence-8--σ-blue)](docs/roadmap_overview.md)

## TORUS in a Nutshell

TORUS Theory addresses recursive self-correction in complex systems, revealing hidden patterns through a 14-layer loop structure. The controller dimension stabilizes these cycles, enabling breakthroughs in domains like gravitational wave detection, prime spirals, and dynamic systems (e.g., bicycle ghost-rider).

Key insight: The χ-cycle predicts oscillatory behavior (~14 moves) in recursive systems, validated across multiple domains with 8-σ evidence (1 in 10¹⁵ chance of coincidence).

## Validation Tracks

- **Gravitational Wave Detectors**: 8-σ evidence of χ-cycle in noise patterns. [Full validation](docs/gw_validation.md).
- **Prime Spirals**: Recursive prime residue patterns match χ-cycle predictions. [Full validation](docs/prime_spirals.md).
- **Bicycle Ghost-Rider**: Dynamic stabilization mirrors controller dimension. [Full validation](docs/bicycle_validation.md).

## Project Structure

- **Minesweeper Framework**: Demonstrates χ-spiral recursion in hypothesis discovery.
- **Confidence Module**: Tracks solver calibration and adjusts risk dynamically.
- **Bicycle Simulation**: Validates controller dimension in dynamic systems.

## Glossary & FAQ

See [Glossary](docs/glossary.md) for quick definitions of χ-cycle, controller dimension, ERC, and more.

## Roadmap

Explore the full theory, simulations, and empirical tests in [Roadmap Overview](docs/roadmap_overview.md).

## Core Modules

| Module         | Purpose                                                      |
| -------------- | ------------------------------------------------------------ |
| BoardBuilder   | Ingests domain relations & builds cell network               |
| ClickEngine    | Propagates constraints, reveals safe cells                   |
| RiskAssessor   | Scores unknown cells for next probe                          |

## White-paper

See [Framework Overview (PDF)](docs/whitepaper.pdf) for the full technical overview.

## Quick Start

```bash
git clone https://github.com/<your-handle>/ai-minesweeper-framework.git
cd ai-minesweeper-framework
pip install -e .
pytest
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

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<org>/AI-Minesweeper-Discovery-Framework/HEAD?filepath=notebooks/confidence_oscillation_demo.ipynb)

## New Domains: Recursive Structure Discovery
- Prime spiral mod-14 structure (χ-cycle)
- Time-series φ-phase gate discovery

## Usage

### Quick Start
Launch the Streamlit app:
```bash
streamlit run streamlit_app.py
```

### Features
- **Interactive Solver**: Select domains like Prime Number Spiral, Phase-Lock φ Reset, or Periodic Table.
- **Custom Data Upload**: Upload CSV, TXT, or PDF files for analysis.
- **AI Integration**: Choose an AI assistant (e.g., OpenAI GPT-4) for advanced parsing.
- **Meta-Cell Confidence Module**: Tracks solver calibration and adjusts risk tolerance dynamically. See [Meta-Cell Confidence Design](docs/design_meta_cell.md).

### Example Domains
- **Prime Number Spiral**: Uncover patterns in prime distribution.
- **Phase-Lock φ Reset**: Detect phase discontinuities in signals.
- **Periodic Table**: Identify missing elements.

### Developer Notes
Run tests:
```bash
pytest
```

Contribute by adding new domains or improving the solver logic.
