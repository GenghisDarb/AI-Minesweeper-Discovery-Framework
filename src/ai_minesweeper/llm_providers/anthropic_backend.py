from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

class AnthropicBackend:
    def __init__(self) -> None:
        logger.info("Anthropic backend scaffold loaded (disabled by default).")

    def suggest(self, board_snapshot: dict) -> list[dict]:
        logger.info("Anthropic suggest called (stub); returning [].")
        return []
