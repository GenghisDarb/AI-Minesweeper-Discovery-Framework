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

## Test Code

```python
from ai_minesweeper.board import Board, State

def test_neighbors_count():
    ...
```

---

## 2. **Fix the Git Push Issue**

Your push is being rejected because your local branch is behind the remote.  
**To fix:**

```bash
git pull --rebase origin main
# If there are conflicts, VS Code will show you how to resolve them.
# After resolving any conflicts:
git push origin main
```

---

*This project is MIT licensed.*