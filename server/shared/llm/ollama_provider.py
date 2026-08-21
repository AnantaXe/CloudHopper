import os
from shared.config.settings import *
from langchain_ollama import ChatOllama

def get_ollama_llm():

    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise RuntimeError("OLLAMA_API_KEY not configured")
    return ChatOllama(
        model="minimax-m3:cloud",
        api_key=api_key,
        temperature=0
    )
