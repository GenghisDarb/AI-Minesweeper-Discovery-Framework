# Changelog

## [Unreleased]
- Fix: resolve syntax/indentation and type guard issues in confidence tracker, CLI, and board.
- Tooling: ruff config tuned (line-length 120, expanded excludes/ignores) to reduce CI noise.
- Stability: deterministic paths verified; tests stabilized and passing in CI.

## [1.0.2] - 2025-07-20
- **Build/Packaging:** Restructured the project to eliminate duplicate module paths. All imports now use the singular `ai_minesweeper` namespace (ensuring a single observer-state locus per TORUS Theory). Removed shadow `src.ai_minesweeper` references and added a CI guard to prevent dual-loading the module. This fixes the MyPy “Source file found twice under different module names” error.

## [1.0.1] - 2025-07-19
- Connected confidence bar in Streamlit UI to BetaConfidence tracker for real-time updates.
- Integrated RiskAssessor into ConstraintSolver for probabilistic fallback.
- Added integration tests for solver logic.
- Replaced debug print statements with proper logging.
- Unified changelogs into a single file.

## v0.4 – TORUS-brot and Meta-Cell Update (2025-07)
- Integrated TORUS-brot fractal module (renderer, data, notebook, documentation).
- Streamlit app now includes TORUS-brot demo domain.
- Meta-Cell Confidence Module can be toggled; added UI visualization of solver confidence.
- Improved documentation (README, glossary) to explain new features and theoretical context.

## v0.4-stable (CI Stability & Bug Fixes)

### Fixed
- **RecursionError in ConstraintSolver**: Refactored circular `choose_move`/`solve` dependency into iterative loop with base-case guard
- **AttributeError 'tuple' has no attribute 'row'**: Updated `RiskAssessor.choose_move` to return Cell objects instead of tuples
- **Type validation**: Added comprehensive type checking in `ConfidencePolicy.choose_move` with fallback handling
- **CSV parsing**: Fixed `BoardBuilder.from_csv` to properly respect `header` parameter and support both relational and grid CSV formats  
- **Board constructor**: Fixed Board(n_rows, n_cols) pattern to properly initialize grid when dimensions are provided
- **State enum usage**: Replaced invalid `State.TRUE` references with `State.REVEALED` in tests
- **Board validation**: Fixed `is_valid()` method to check logical consistency instead of requiring all cells to be revealed
- **Hidden cells logic**: Removed incorrect assertion in `hidden_cells()` method that prevented boards with mixed states
- **Bounds checking**: Added comprehensive bounds validation to DPP14RecursionEngine and other utilities
- **CLI output**: Standardized messages to match test expectations and added backwards compatibility for move handling
- **BetaConfidence update**: Fixed probability-based update logic to match expected test behavior

### Enhanced
- **Defensive programming**: Added `dict.get()` with defaults for optional keys in engine results
- **Error handling**: Improved exception handling and fallback logic throughout the codebase
- **Type safety**: Enhanced type annotations and validation across policy wrappers
- **CSV support**: Added robust parsing for both traditional grid and relational CSV formats

### CI Improvements
- **Multi-version testing**: Added Python 3.10, 3.11, 3.12 compatibility testing
- **Additional linting**: Integrated pylint and mypy checks into CI pipeline
- **Enhanced validation**: Improved test coverage and edge case handling

### Breaking Changes
- `RiskAssessor.choose_move()` now returns Cell objects instead of tuples
- `ConfidencePolicy.choose_move()` returns Cell objects with enhanced type validation
- CSV parsing behavior changed to respect header parameter properly

## v0.3-beta
- Added Meta-Cell Confidence Module.
- Created tutorial notebook demonstrating confidence oscillation.
- Updated README with Binder badge and σ-evidence auto-update.
- Enforced coverage thresholds in CI pipeline.

## [1.0.0] - 2025-07-13
- Full Streamlit UI with copy/export/chat/confidence history.
- Dynamic board expansion and visual feedback loop.
- Debug matrix resolved (Tiers 1–3).
- Fractal χ-brot visualizer and prime/periodic examples included.
- Enhanced performance for large datasets.
- Improved documentation and inline code comments.
- Fixed minor bugs and UI glitches.
