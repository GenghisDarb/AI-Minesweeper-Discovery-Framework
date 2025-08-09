from __future__ import annotations
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class AnthropicBackend:
    def __init__(self) -> None:
        logger.info("Anthropic backend scaffold loaded (disabled by default).")

    def suggest(self, board_snapshot: Dict) -> List[Dict]:
        logger.info("Anthropic suggest called (stub); returning [].")
        return []
