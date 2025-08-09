from __future__ import annotations

import os
from typing import Any

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI provider compatible with both legacy (0.x) and new (1.x) SDKs.

    - Prefers the new client API if available: openai.OpenAI().
    - Falls back to legacy openai.ChatCompletion/Completion.
    - Deterministic defaults: temperature=0.0, top_p=1.0.
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        # Lazy import so environments without openai still work when not used
        try:  # pragma: no cover - optional dependency
            import openai  # type: ignore
        except Exception as e:  # pragma: no cover - optional dependency
            raise RuntimeError("openai package is required for OpenAIProvider") from e

        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set api_key or OPENAI_API_KEY.")
        self.model = model

        # Detect SDK flavor
        self._mode: str
        self._client: Any
        if hasattr(openai, "OpenAI"):
            # New SDK (>=1.0)
            self._mode = "v1"
            self._client = openai.OpenAI(api_key=self.api_key)
        else:
            # Legacy SDK
            self._mode = "legacy"
            self._client = openai
            self._client.api_key = self.api_key

    def query(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.0,
        request_timeout: int | float | None = 15,
        max_tokens: int = 256,
    ) -> str:
        # Prefer new SDK client if available; otherwise use legacy API
        if self._mode == "v1":  # new SDK
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=1.0,
                max_tokens=max_tokens,
            )
            return (resp.choices[0].message.content or "").strip()
        # Legacy SDK path
        if hasattr(self._client, "ChatCompletion"):
            messages = []  # type: ignore[var-annotated]
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = self._client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=1.0,
                max_tokens=max_tokens,
                request_timeout=request_timeout,
            )
            return resp.choices[0].message["content"].strip()
        resp = self._client.Completion.create(
            model=self.model,
            prompt=(system + "\n" + prompt).strip(),
            temperature=temperature,
            top_p=1.0,
            max_tokens=max_tokens,
            request_timeout=request_timeout,
        )
        return resp.choices[0].text.strip()

    def chat(
        self,
        history: list[dict[str, str]],
        temperature: float = 0.0,
        request_timeout: int | float | None = 15,
        max_tokens: int = 256,
    ) -> str:
        if self._mode == "v1":
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=history,
                temperature=temperature,
                top_p=1.0,
                max_tokens=max_tokens,
            )
            return (resp.choices[0].message.content or "").strip()
        resp = self._client.ChatCompletion.create(
            model=self.model,
            messages=history,
            temperature=temperature,
            top_p=1.0,
            max_tokens=max_tokens,
            request_timeout=request_timeout,
        )
        return resp.choices[0].message["content"].strip()

    def name(self) -> str:
        return "OpenAI"
