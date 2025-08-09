from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .base import LLMProvider
from .openai_provider import OpenAIProvider

CONFIG_PATH = Path("config/llm.yaml")


def _load_yaml_config(path: Path) -> dict[str, Any]:
    # Optional dependency: PyYAML. If unavailable, return empty dict and rely on env vars
    try:
        import yaml  # type: ignore
    except Exception:  # pragma: no cover - optional
        return {}
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            return {}
        return data  # type: ignore[return-value]


def get_provider(name: str) -> LLMProvider:
    cfg = _load_yaml_config(CONFIG_PATH)

    if name == "openai":
        api_key = cfg.get("api_key") or os.getenv("OPENAI_API_KEY")
        model = cfg.get("model") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAIProvider(api_key=api_key, model=model)

    raise ValueError(f"Unknown provider: {name}")
