from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()


class ModelClient:
    def __init__(self):
        self.anthropic_model_client = AnthropicChatCompletionClient(
            model="claude-opus-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")
        )
