"""LLM module for career assistant."""

from langchain.llms import Ollama


def get_ollama_llm() -> Ollama:
    """Get the LLM for the career assistant.

    Returns:
        Ollama: The LLM.
    """
    llm = Ollama(
        model="llama3",
        temperature=0.3
    )
    return llm
