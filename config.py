import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

set_tracing_disabled(True)

MODEL_NAME = "gemini-3.8-flash"

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=60,       # give up after 60 seconds
    max_retries=1,    # try again only once
)
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=client,
)