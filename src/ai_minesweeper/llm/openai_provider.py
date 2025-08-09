from __future__ import annotations

import os
from typing import Any, List, Dict

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        # Lazy import so environments without openai still work when not used
        try:
            import openai  # type: ignore
        except Exception as e:  # pragma: no cover - optional dependency
            raise RuntimeError("openai package is required for OpenAIProvider") from e

        self._openai = openai
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set api_key or OPENAI_API_KEY.")
        self.model = model
        self._openai.api_key = self.api_key

    def query(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.0,
        request_timeout: int | float | None = 15,
        max_tokens: int = 256,
    ) -> str:
        # Prefer Chat Completions if available in SDK; otherwise fall back
        if hasattr(self._openai, "ChatCompletion"):
            messages = []  # type: List[Dict[str, str]]
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = self._openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                request_timeout=request_timeout,
            )
            return resp.choices[0].message["content"].strip()
        else:
            resp = self._openai.Completion.create(
                model=self.model,
                prompt=(system + "\n" + prompt).strip(),
                temperature=temperature,
                max_tokens=max_tokens,
                request_timeout=request_timeout,
            )
            return resp.choices[0].text.strip()

    def chat(
        self,
        history: List[Dict[str, str]],
        temperature: float = 0.0,
        request_timeout: int | float | None = 15,
        max_tokens: int = 256,
    ) -> str:
        resp = self._openai.ChatCompletion.create(
            model=self.model,
            messages=history,
            temperature=temperature,
            max_tokens=max_tokens,
            request_timeout=request_timeout,
        )
        return resp.choices[0].message["content"].strip()

    def name(self) -> str:
        return "OpenAI"
