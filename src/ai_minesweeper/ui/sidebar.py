from ai_minesweeper.constants import CHI_STR6


def render_constants() -> dict:
    """Return canonical constants for display in UI/CLI."""
    return {"χ": CHI_STR6}

__all__ = ["render_constants"]
