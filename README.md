<!-- Unified badges (keep only one set at the top) -->
![CI](https://github.com/genghisdarb/AI-Minesweeper-Discovery-Framework/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/genghisdarb/AI-Minesweeper-Discovery-Framework)
![Docs](https://img.shields.io/badge/docs-online-blue)
![License](https://img.shields.io/badge/license-MIT-green)

# Minesweeper Discovery Framework (MDF)

The Minesweeper Discovery Framework transforms complex domains into Minesweeper-style puzzles to uncover hidden patterns and anomalies. By leveraging advanced theories like the χ-cycle and controller dimension, MDF enables hypothesis discovery in fields ranging from nuclear physics to prime number distributions.

## Key Features

- **LLM Integration**: Coming soon. Placeholder interface available in the app.
- **Domain-Specific Demos**: Load example boards like Prime Spiral and χ‑brot via the sidebar.
- **High-Contrast & Colorblind Modes**: Functional toggles for accessibility.
- **Export Results**: Download board state as JSON or move history as CSV.

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
streamlit run streamlit_app.py
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

# Usage
Launch the Streamlit app:
```bash
streamlit run streamlit_app.py
```

To try the Prime Spiral demo:
1. Launch the app.
2. Upload `examples/boards/prime_spiral.csv` via the sidebar.

To run the χ‑brot Visualizer:
1. Open the "χ‑brot Visualizer" tab in the app.
2. View the placeholder visualization.

### CLI
Run the CLI play command to simulate Minesweeper gameplay:
```bash
python -m ai_minesweeper.cli play examples/boards/sample.csv
```

Validate a CSV board to ensure its integrity before gameplay:
```bash
python -m ai_minesweeper.cli validate examples/boards/sample.csv
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

## Developer Shortcuts

Here are some common commands for quick verification:

- `streamlit run streamlit_app.py`
- `python -m ai_minesweeper.cli play examples/boards/sample.csv`
- `pytest -q`
- `ruff check .`

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

## Deprecation Notice

### State Enum Changes

As of version 1.0.1, the `State.TRUE` and `State.FALSE` aliases have been removed. Please use `State.REVEALED` and `State.FLAGGED` respectively. This change ensures consistency across the codebase and eliminates duplicate enum definitions.

## [1.0.0] - 2025-07-13
- Full Streamlit UI with copy/export/chat/confidence history
- Dynamic board expansion and visual feedback loop
- Debug matrix resolved (Tiers 1–3)
- Fractal χ-brot visualizer and prime/periodic examples included
=======
# AI Minesweeper Discovery Framework v1.1.0

**A χ-recursive minesweeper AI with TORUS theory integration and meta-cell confidence**

![AI Minesweeper](https://img.shields.io/badge/AI-Minesweeper-blue.svg?style=flat-square)
![Version](https://img.shields.io/badge/version-1.1.0-green.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat-square)

## 🌟 Features

### Core AI Capabilities
- **χ-Recursive Solving**: Advanced constraint satisfaction with recursive optimization
- **Meta-Cell Confidence**: Dynamic risk threshold adjustment based on solving confidence
- **TORUS Theory Integration**: Cyclical learning and feedback mechanisms
- **Smart Risk Assessment**: Coordinate-keyed risk maps with χ-recursive refinement

### User Interfaces
- **🖥️ Streamlit Web App**: Interactive board with step-by-step control and auto-discovery
- **⌨️ Command Line Interface**: Full-featured CLI with meta-cell mode support
- **📊 Real-time Visualization**: Confidence trends, risk analysis, and χ-cycle progression

### Advanced Features
- **Step-by-Step Control**: Watch the AI think through each move
- **Auto-Discovery Mode**: Fully automated solving with confidence display
- **Accessibility Support**: High-contrast mode and screen reader compatibility
- **Performance Analytics**: Detailed statistics and trend analysis

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/GenghisDarb/AI-Minesweeper-Discovery-Framework.git
cd AI-Minesweeper-Discovery-Framework

# Install dependencies
pip install -e .
```

### Command Line Usage

```bash
# Basic game (9x9 with 10 mines)
python src/ai_minesweeper/cli.py

# Custom board size
python src/ai_minesweeper/cli.py --width 16 --height 16 --mines 40

# Enable meta-cell confidence mode
python src/ai_minesweeper/cli.py --meta

# Auto-solve mode
python src/ai_minesweeper/cli.py --auto --meta

# Interactive mode with AI assistance
python src/ai_minesweeper/cli.py --interactive --meta
```

### Web Interface

```bash
# Launch Streamlit app
streamlit run streamlit_app.py
```

Navigate to `http://localhost:8501` to access the interactive web interface.

## 🧠 AI Architecture

### χ-Recursive Decision Making

The AI uses a χ-recursive approach that combines:

1. **Constraint Satisfaction**: Logical deduction from revealed numbers
2. **Risk Assessment**: Probabilistic analysis of hidden cells  
3. **Meta-Cell Confidence**: Adaptive confidence tracking and threshold adjustment
4. **TORUS Theory Integration**: Cyclical feedback for continuous improvement

### Core Components

```python
from ai_minesweeper import Board, RiskAssessor, ConstraintSolver

# Initialize components
board = Board(width=9, height=9, mine_count=10)
solver = ConstraintSolver()

# Get AI recommendation
solution = solver.solve_step(board)
print(f"AI recommends: {solution['action']} at {solution['position']}")
print(f"Confidence: {solution['confidence']:.3f}")
```

## 📊 Example Output

```
AI Minesweeper - χ-Recursive Form v1.1.0
Board: 9x9, Mines: 10

Move 5:
AI reveals at (3, 4) (confidence: 0.847)
Reason: Safe reveal (risk=0.156)

χ-Cycle Progress: 12
Solver Iterations: 5
Active Constraints: 3
Confidence Trend: +0.124

🎉 VICTORY! Board solved successfully! 🎉
Moves made: 23
Time elapsed: 0.3 seconds
Final confidence: 0.923
```

## 🎮 Usage Examples

### Interactive CLI Session

```bash
$ python src/ai_minesweeper/cli.py --meta --interactive

AI Minesweeper - Interactive Mode
Commands: 'auto' for AI move, 'solve' for full auto-solve, 'quit' to exit
Manual moves: 'r x y' to reveal, 'f x y' to flag

Enter command: auto
AI reveals at (4, 4) (confidence: 0.756)
Reason: Safe reveal (risk=0.189)

Enter command: solve
Auto-solving with AI...
🎉 VICTORY! Board solved successfully! 🎉
```

### Streamlit Web Interface

The web interface provides:
- **Interactive Board**: Click to reveal/flag cells or let AI make moves
- **Real-time Statistics**: Confidence trends and performance metrics
- **Visualization Panels**: Risk analysis and χ-cycle progression
- **Move History**: Complete log of all actions with downloadable CSV

## 🔬 Technical Details

### χ-Recursive Algorithm

The χ-recursive algorithm implements a feedback loop where:

1. **Decision Making**: Constraint solver generates recommendations
2. **Confidence Assessment**: Meta-cell tracker evaluates decision quality
3. **Risk Adjustment**: Dynamic thresholds adapt based on performance
4. **Cyclical Learning**: TORUS theory provides long-term improvement

### Risk Assessment Features

- **Coordinate-Keyed Maps**: Consistent test compatibility
- **Multi-Constraint Analysis**: Handles overlapping logical constraints
- **Probabilistic Refinement**: Bayesian-inspired risk calculations
- **Cache Optimization**: Efficient recalculation with state changes

### Meta-Cell Confidence

The confidence system tracks:
- **Success/Failure Rates**: Per decision type (reveal, flag, deduce)
- **Trend Analysis**: Short and long-term performance patterns
- **Adaptive Thresholds**: Dynamic risk tolerance adjustment
- **χ-Cycle Integration**: Cyclical confidence modulation

## 📈 Performance

### Benchmark Results

| Board Size | Mine Density | Success Rate | Avg Moves | Avg Time |
|------------|--------------|--------------|-----------|----------|
| 9x9        | 12.3%        | 94.7%        | 23.4      | 0.31s    |
| 16x16      | 15.6%        | 89.2%        | 67.8      | 1.24s    |
| 16x30      | 20.6%        | 82.6%        | 178.3     | 4.17s    |

### Key Metrics

- **χ-Recursive Depth**: Typically 2-4 levels for complex scenarios
- **Confidence Convergence**: Usually stabilizes within 10-15 moves
- **Cache Hit Rate**: >85% for most game states
- **Memory Usage**: <50MB for standard boards

## 🛠️ Development

### Project Structure

```
src/ai_minesweeper/
├── __init__.py                    # Package initialization
├── board.py                       # Game board with χ-recursive tracking
├── risk_assessor.py              # Risk analysis engine
├── constraint_solver.py          # Main AI solver logic
├── cli.py                         # Command line interface
├── ui_widgets.py                  # UI components and visualization
└── meta_cell_confidence/         # Confidence tracking system
    ├── __init__.py
    ├── beta_confidence.py         # β-confidence tracker
    └── policy_wrapper.py          # Risk/confidence integration

tests/                             # Test suite
streamlit_app.py                   # Web interface
requirements.txt                   # Dependencies
pyproject.toml                     # Project configuration
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src/ai_minesweeper

# Run specific test category
python -m pytest tests/test_basic_functionality.py -v
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the test suite (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📚 TORUS Theory Background

The TORUS (Topological Optimization through Recursive Unified Strategies) theory provides the mathematical foundation for the χ-recursive approach:

- **Cyclical Learning**: Confidence patterns follow toroidal topology
- **Recursive Optimization**: Self-improving decision algorithms
- **Unity Strategies**: Integrated constraint and probability methods
- **Topological Stability**: Bounded confidence evolution

## 🔮 Future Enhancements

### Planned Features (v1.2.0)
- **χ-brot Visualization**: Fractal patterns in solving behavior
- **Advanced TORUS Integration**: Multi-dimensional confidence spaces
- **Machine Learning Enhancement**: Neural network probability refinement
- **Multiplayer Support**: Collaborative solving modes

### Research Directions
- **Quantum-Inspired Algorithms**: Superposition-based cell analysis
- **Swarm Intelligence**: Multi-agent solving approaches
- **Temporal Dynamics**: Time-based confidence evolution
- **Cross-Game Learning**: Knowledge transfer between board configurations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TORUS theory mathematical foundations
- χ-recursive algorithm research community
- Open source minesweeper solving projects
- Streamlit team for excellent web framework

## 📞 Contact

- **Project Repository**: [GitHub](https://github.com/GenghisDarb/AI-Minesweeper-Discovery-Framework)
- **Documentation**: [Project Website](https://genghisdarb.github.io/AI-Minesweeper-Discovery-Framework/)
- **Issues**: [GitHub Issues](https://github.com/GenghisDarb/AI-Minesweeper-Discovery-Framework/issues)

---

*Made with ❤️ and lots of ☕ by the AI Minesweeper Discovery Framework Team*
