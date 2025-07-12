# Example Boards

This folder contains sample datasets for the AI Minesweeper Discovery Framework.

## Files
- **mini.csv**: A small 5x5 Minesweeper board for quick tests.
- **elements.csv**: Represents the periodic table with discovered and undiscovered elements.

## Format
- `mine`: Indicates a mine (false hypothesis).
- Blank or other values: Safe cells.

## Notes
Custom boards can be uploaded via the Streamlit app.

# Board Fixtures

This folder contains example Minesweeper boards used for testing, documentation, and demos.

## Coordinate Convention
- The top-left corner is (0,0).
- `M` represents a mine.
- Blank cells represent hidden tiles.

## Files
- `simple.csv`: A 5x5 board with 5 mines, used in tutorial examples.
- `divergent.csv`: An 8x8 board with a symmetric mine pattern, used to test unsolvable scenarios.

