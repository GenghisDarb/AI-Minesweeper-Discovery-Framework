import openai
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def query(self, prompt: str, system: str = "", temperature: float = 0.7) -> str:
        response = openai.Completion.create(
            model=self.model,
            prompt=system + "\n" + prompt,
            temperature=temperature,
            max_tokens=150,
        )
        return response.choices[0].text.strip()

    def chat(self, history: list[dict]) -> str:
        response = openai.ChatCompletion.create(
            model=self.model, messages=history, temperature=0.7
        )
        return response.choices[0].message["content"].strip()

    def name(self) -> str:
        return "OpenAI"
