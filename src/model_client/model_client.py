from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()


class ModelClient:
    def __init__(self):
        self.model_client = AnthropicChatCompletionClient(
            model="claude-opus-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY")
        )
