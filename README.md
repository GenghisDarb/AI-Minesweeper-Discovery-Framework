# Minesweeper Discovery Framework (MDF)

![CI](https://github.com/genghisdarb/AI-Minesweeper-Discovery-Framework/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/genghisdarb/AI-Minesweeper-Discovery-Framework)
![Docs](https://img.shields.io/badge/docs-online-blue)
![License](https://img.shields.io/badge/license-MIT-green)

The Minesweeper Discovery Framework transforms complex domains into Minesweeper-style puzzles to uncover hidden patterns and anomalies. By leveraging advanced theories like the χ-cycle and controller dimension, MDF enables hypothesis discovery in fields ranging from nuclear physics to prime number distributions.

## Key Features
- **Modular Design**: Easily extendable to new domains via adapters.
- **Interactive Tools**: Includes a Streamlit web app and Binder notebook for demos.
- **Robust Validation**: Backed by 8-σ empirical evidence.

## Quick Start
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Streamlit app: `streamlit run streamlit_app.py`.
4. Note: This framework can operate in LLM-assisted or LLM-free modes. LLMs are optional and used only for unstructured hypothesis generation.

## What This Is
This framework is not a game. It uses Minesweeper-like reasoning structures to recursively resolve hypotheses in uncertain domains using logic, constraint propagation, and confidence-driven risk assessment.

## LLM-Free Mode
This tool can operate in fully symbolic, LLM-free mode using human-supplied or structured input data.

## LLM Configuration
MDF supports optional integration with LLMs for advanced reasoning. To enable, configure `llm.yaml` in the `config/` directory with your LLM API credentials. If no LLM is configured, MDF will gracefully fall back to deterministic logic.

## TORUS Theory
The χ-cycle and controller dimension principles underpin MDF's hypothesis discovery engine. See [Why TORUS Matters](docs/why_torus_matters.md) for an in-depth explanation.

## Validation Tracks

- **Gravitational Wave Detectors**: 8-σ evidence of χ-cycle in noise patterns. [Full validation](docs/gw_validation.md).
- **Prime Spirals**: Recursive prime residue patterns match χ-cycle predictions. [Full validation](docs/prime_spirals.md).
- **Bicycle Ghost-Rider**: Dynamic stabilization mirrors controller dimension. [Full validation](docs/bicycle_validation.md).

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

The full white-paper is available in [PDF format](docs/whitepaper.pdf).

## Web Demo

![screenshot](docs/screenshot.png)

To launch the Streamlit UI:

```bash
streamlit run [streamlit_app.py](http://_vscodecontentref_/1)
```

[![Streamlit Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-green?logo=streamlit)](https://genghisdarb.github.io/AI-Minesweeper-Discovery-Framework/)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GenghisDarb/AI-Minesweeper-Discovery-Framework/HEAD?filepath=notebooks/confidence_oscillation_demo.ipynb)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GenghisDarb/AI-Minesweeper-Discovery-Framework/HEAD?filepath=notebooks/prime_spiral_validation.ipynb)

[![codecov](https://codecov.io/gh/GenghisDarb/AI-Minesweeper-Discovery-Framework/branch/main/graph/badge.svg)](https://codecov.io/gh/GenghisDarb/AI-Minesweeper-Discovery-Framework)

## [Live Demo](https://minesweeper-discovery.streamlit.app)

Experience the Minesweeper Discovery Framework live on Streamlit Cloud. Explore the interactive UI, confidence charts, and dynamic board expansion.

## New Domains: Recursive Structure Discovery
- Prime spiral mod-14 structure (χ-cycle)
- Time-series φ-phase gate discovery

## New Features

### Streamlit Enhancements
- **Confidence Display**: Real-time progress bar and percentage indicator.
- **Color-Coded Board Rendering**: Visual styling for cell states (safe, hidden, mine, clue).
- **Copy Results Button**: Export board state and confidence trajectory.

### CLI Improvements
- **Interactive Play Mode**: Load a CSV board, solve it step-by-step, and view the board state after each move.

### Dependency Updates
- Added `pandas` for CSV handling.

## Usage

### Streamlit App
Launch the Streamlit app:
```bash
streamlit run streamlit_app.py
```

### CLI
Run the CLI play command to simulate Minesweeper gameplay:
```bash
python -m src.ai_minesweeper.cli play examples/boards/sample.csv
```

Validate a CSV board to ensure its integrity before gameplay:
```bash
python -m src.ai_minesweeper.cli validate examples/boards/sample.csv
```
The `validate` command checks for inconsistencies or errors in the board configuration, ensuring a smooth gameplay experience.

### Testing
Run all tests:
```bash
pytest
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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

*This project is MIT licensed.*

<p align="center">
  <img src="figures/torus_brot_demo.png" width="320"/><br/>
  <em>χ-recursive TORUS-brot fractal</em>
</p>

![χ-value](https://img.shields.io/badge/χ-$(cat data/chi_50digits.txt | head -c 10)…-informational?style=flat&logo=wolfram)
![τ (χ-cycle)](https://img.shields.io/badge/τ≈$(jq '.tau' data/confidence_fit_params.json | xargs printf '%.2f')-success)
![Prime S stat](https://img.shields.io/badge/S=$(tail -n1 reports/prime_residue_S.csv)-critical)

> Nightly badges auto-update via Wolfram pipeline.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Streamlit app: `streamlit run streamlit_app.py`.

> **CI secret required**  
> Add `CODECOV_TOKEN` under **Settings → Secrets → Actions** to enable  
> coverage reporting. See `docs/ci_setup.md` for full instructions.

## TORUS-Brot Demo

![TORUS-Brot Fractal](docs/figures/torus_brot_hero_labeled.png)

The TORUS-Brot fractal visualization demonstrates recursive χ-phase pattern generation derived from the TORUS-brot symbolic seed map. This fractal highlights the depth and beauty of the recursive discovery process at the heart of the framework.

## TORUS 14-Lane Recursion Mode

The AI Minesweeper Discovery Framework now includes a 14-lane recursion engine based on TORUS Theory. This engine simulates parallel solving across 14 dimensions, tracking χ values and detecting resonance zones.

### Features
- **Deep Parallel Processing (DPP)**: 14 parallel lanes with cross-lane propagation.
- **χ Tracking**: Computes χ values for each lane and aggregates them into χ₁₄.
- **Resonance Detection**: Identifies stable regions and propagates knowledge across lanes.
- **Divergence Handling**: Handles lane collapses and updates surviving lanes.

### How to Use
Run the Streamlit app and click "Run 14-Lane Recursion Engine" to see the results of the multi-lane simulation.

## [1.0.0] - 2025-07-13
- Full Streamlit UI with copy/export/chat/confidence history
- Dynamic board expansion and visual feedback loop
- Debug matrix resolved (Tiers 1–3)
- Fractal χ-brot visualizer and prime/periodic examples included
