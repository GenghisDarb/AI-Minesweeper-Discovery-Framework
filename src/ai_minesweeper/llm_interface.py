from __future__ import annotations
import logging
from typing import List, Dict, Any, Tuple
from .llm_providers import load_provider

logger = logging.getLogger(__name__)

def llm_suggest(board_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Ask the configured provider for suggestions.
    Returns a sorted list of dicts: {"action","cell","reason","p"}.
    Deterministic, non-blocking semantics: if provider is absent/fails, return [].
    """
    provider = load_provider()
    if provider is None:
        return []
    try:
        suggestions = provider.suggest(board_snapshot) or []
    except Exception as e:  # pragma: no cover
        logger.warning("LLM provider failed: %s", e)
        return []
    def norm(item: Dict[str, Any]) -> Tuple[float, int, int, str, str]:
        r, c = tuple(item.get("cell", (0, 0)))
        p = float(item.get("p", 0.0))
        action = str(item.get("action", "abstain"))
        reason = str(item.get("reason", ""))
        return (min(1.0, max(0.0, p)), int(r), int(c), action, reason)
    # Stable ordering: (p, r, c, action, reason)
    ranked = [s for _, s in sorted((norm(x), x) for x in suggestions)]
    return ranked
