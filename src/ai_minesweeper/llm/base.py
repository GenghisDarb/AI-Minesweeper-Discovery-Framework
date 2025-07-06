from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def query(self, prompt: str, system: str = "", temperature: float = 0.7) -> str:
        """
        Send a query to the LLM and return the response.
        """
        pass

    @abstractmethod
    def chat(self, history: list[dict]) -> str:
        """
        Engage in a chat session with the LLM using a history of messages.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        Return the name of the LLM provider.
        """
        pass
