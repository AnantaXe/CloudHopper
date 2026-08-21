import os
from shared.config.settings import *
from langchain_openai import ChatOpenAI


def get_llm():

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not configured"
        )

    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=api_key,
        temperature=0
    )