from autogen_agentchat.agents import AssistantAgent
from src.autogen_agents_logic.model_client import ModelClient
from src.prompts.guardrail_prompts import GuardrailPromptConfig
from src.autogen_agents_logic.pydantic_models import InputGuardrailPydanticModel

class GuardrailAgents:
    def __init__(self):
        self.model_client = ModelClient().model_client
        self._prompt_config = GuardrailPromptConfig()

    def input_guardrail_agent(self):
        prompt_config = self._prompt_config.get_prompt(key="input_guardrail_prompts")

        input_guardrail = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
            output_content_type=InputGuardrailPydanticModel
        )

        return input_guardrail
    
    def output_guardrail_agent(self):
        prompt_config = self._prompt_config.get_prompt(key="refining_prompt")

        output_guardrail = AssistantAgent(
            name=prompt_config.get("name", None),
            description=prompt_config.get("description", None),
            model_client=self.model_client,
            system_message=prompt_config.get("system_prompt", None),
        )

        return output_guardrail
