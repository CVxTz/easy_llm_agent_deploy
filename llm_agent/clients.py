import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks

dot_env_path = Path(__file__).parents[1] / ".env"
if dot_env_path.is_file():
    load_dotenv(dotenv_path=dot_env_path)

LLM_API_KEY = os.environ.get("LLM_API_KEY")

client_medium = ChatFireworks(
    api_key=LLM_API_KEY,
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    temperature=0,
)

client_large = ChatFireworks(
    api_key=LLM_API_KEY,
    model="accounts/fireworks/models/llama-v3p1-70b-instruct",
    temperature=0,
)
