from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

class LocalBackend:
    def __init__(self) -> None:
        logger.info("Local backend scaffold loaded (deterministic baseline).")

    def suggest(self, board_snapshot: dict) -> list[dict]:
        # Deterministic baseline: pick lowest (r,c) hidden if provided
        hidden: list[tuple[int,int]] = list(map(tuple, board_snapshot.get("hidden", [])))
        if not hidden:
            return []
        r, c = sorted(hidden)[0]
        return [
            {
                "action": "reveal",
                "cell": (int(r), int(c)),
                "reason": "deterministic baseline",
                "p": 0.5,
            }
        ]
