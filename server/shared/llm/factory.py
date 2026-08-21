from shared.llm.openai_provider import get_openai_llm
from shared.llm.ollama_provider import get_ollama_llm
from shared.llm.anthropic_provder import get_anthropic_llm

def get_llm(provider: str):

    if provider == "openai":
        return get_openai_llm()
    elif provider == "ollama":
        return get_ollama_llm()
    elif provider == "anthropic":
        return get_anthropic_llm()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")