from autogen_agentchat.agents import AssistantAgent
from src.model_client.model_client import ModelClient
from src.prompts.guardrail_prompts.prompts_config import GuardrailPromptConfig


class GuardrailAgents:
    def __init__(self):
        self.model_client = ModelClient().model_client
        self._prompt_config = GuardrailPromptConfig()

    def input_guardrail_agent(self):
        prompt_config = self.prompt_config._get_prompt(key="refining_prompt")

        input_guardrail = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return input_guardrail
    
    def output_guardrail_agent(self):
        prompt_config = self.prompt_config._get_prompt(key="refining_prompt")

        output_guardrail = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return output_guardrail
