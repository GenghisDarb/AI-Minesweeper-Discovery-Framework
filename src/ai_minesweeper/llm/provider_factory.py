from .openai_provider import OpenAIProvider
from .base import LLMProvider
import yaml

CONFIG_PATH = "config/llm.yaml"


def get_provider(name: str) -> LLMProvider:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    if name == "openai":
        return OpenAIProvider(api_key=config["api_key"], model=config["model"])
    # Add other providers here
    raise ValueError(f"Unknown provider: {name}")
