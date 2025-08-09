from __future__ import annotations
import os
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class OpenAIBackend:
    def __init__(self) -> None:
        # Lazy import to avoid hard dependency when disabled
        try:
            import openai  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("openai package required for OpenAI backend") from e

        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        self._openai = openai
        self._openai.api_key = api_key
        self._model = model

    def suggest(self, board_snapshot: Dict) -> List[Dict]:
        """
        Return list of dicts with:
          {"action": "flag"|"reveal"|"abstain", "cell": (r,c), "reason": str, "p": float}
        Deterministic params; on error return [].
        """
        try:
            system = (
                "You are a deterministic assistant. "
                "Recommend a single Minesweeper action with a probability p in [0,1]. "
                "Never reveal hidden truth; only reason from the provided snapshot."
            )
            user = "Given this board snapshot, rank one next action:\n" + str(board_snapshot)
            params = dict(
                model=self._model,
                temperature=0.0, top_p=1.0, n=1, max_tokens=192, request_timeout=6,
            )
            # Prefer ChatCompletion if available
            if hasattr(self._openai, "ChatCompletion"):
                resp = self._openai.ChatCompletion.create(
                    messages=[{"role": "system", "content": system},
                              {"role": "user", "content": user}],
                    **params,
                )
                text = resp.choices[0].message["content"].strip()
            else:
                resp = self._openai.Completion.create(
                    prompt=(system + "\n" + user),
                    **params,
                )
                text = resp.choices[0].text.strip()
            # Sanitization
            action = "abstain"
            cell = (0, 0)
            p = 0.0
            reason = text
            lowered = text.lower()
            if "flag" in lowered:
                action = "flag"
            elif "reveal" in lowered:
                action = "reveal"
            import re
            m = re.search(r"\((\s*\d+\s*),(\s*\d+\s*)\)", text)
            if m:
                r = int(m.group(1))
                c = int(m.group(2))
                cell = (int(r), int(c))
            m2 = re.search(r"p\s*[=:]\s*([01](?:\.\d+)?)", lowered)
            if m2:
                try:
                    p = float(m2.group(1))
                except Exception:
                    p = 0.0
            p = min(1.0, max(0.0, float(p)))
            return [{"action": action, "cell": (int(cell[0]), int(cell[1])), "reason": reason, "p": float(p)}]
        except Exception as e:  # pragma: no cover
            logger.warning("OpenAI suggest failed: %s", e)
            return []
