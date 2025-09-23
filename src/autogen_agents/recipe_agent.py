from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()


class RecipeAgent:
    def __init__(self):
        self.model_client = AnthropicChatCompletionClient(
            model="claude-opus-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
    def prompt_refining_agent(self):
        refined_prompt = AssistantAgent(
            name="Prompt_Refining_Agent",
            description="You will recieve prompt from the user and your task is to refine it so that"
        )
