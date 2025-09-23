from autogen_agentchat.agents import AssistantAgent
from src.prompts.agent_prompts import AgentPromptConfig
from src.autogen_agents_logic.model_client import ModelClient

class RecipeAgents:
    def __init__(self):
        self.model_client = ModelClient().model_client
        self._prompt_config = AgentPromptConfig()

    def prompt_refining_agent(self):
        prompt_config = self._prompt_config.get_prompt(key="refining_prompt")

        agent = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return agent

    def recipe_generator_agent(self):
        prompt_config = self._prompt_config.get_prompt(key="generate_recipe_prompt")

        agent = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return agent

    def reviewer_agent(self):
        prompt_config = self._prompt_config.get_prompt(key="reviewer_prompt")

        agent = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return agent
