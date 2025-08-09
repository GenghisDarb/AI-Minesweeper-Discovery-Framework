from __future__ import annotations
import os
import logging
from typing import Protocol, List, Dict, Optional

logger = logging.getLogger(__name__)

class LLMProvider(Protocol):
    def suggest(self, board_snapshot: Dict) -> List[Dict]: ...

def load_provider() -> Optional[LLMProvider]:
    """Load LLM provider from env.

    AIMS_LLM_PROVIDER in {"openai","anthropic","local","disabled"}
    default "openai" if OPENAI_API_KEY present, else "disabled".
    """
    name = (os.getenv("AIMS_LLM_PROVIDER") or "").strip().lower()
    if not name:
        name = "openai" if os.getenv("OPENAI_API_KEY") else "disabled"

    try:
        if name == "openai":
            from .openai_backend import OpenAIBackend
            return OpenAIBackend()
        if name == "anthropic":
            from .anthropic_backend import AnthropicBackend
            return AnthropicBackend()
        if name == "local":
            from .local_backend import LocalBackend
            return LocalBackend()
        if name == "disabled":
            return None
    except Exception as e:  # pragma: no cover
        logger.warning("LLM provider init failed (%s); disabling.", e)
        return None
    return None
