# Element Discovery Tutorial

## Overview

This tutorial demonstrates how the AI Minesweeper Discovery Framework can be applied to uncover missing elements in the periodic table. The periodic table is represented as a grid, where each cell corresponds to an element. Discovered elements are marked as safe, while undiscovered elements are treated as mines.

## Dataset

The dataset used for this demo is `examples/boards/elements.csv`. It includes:

- **atomic_number**: The atomic number of the element.
- **symbol**: The chemical symbol.
- **group**: The group number in the periodic table.
- **period**: The period number in the periodic table.
- **is_discovered**: A boolean indicating whether the element is discovered.

## Rules

- A revealed cell provides a clue indicating the number of undiscovered elements adjacent to it.
- Adjacent relationships are based on the periodic table layout (groups and periods).

## Steps

1. Launch the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Select "Periodic Table (Element Discovery)" from the domain menu.
3. Observe the periodic table grid and interact with the solver to reveal clues and identify undiscovered elements.

## Example

Revealing Oxygen (O) might show a clue "1", indicating one of its adjacent cells contains an undiscovered element.

## Notes

This demo is a simplified representation of the periodic table and is intended for educational purposes.
