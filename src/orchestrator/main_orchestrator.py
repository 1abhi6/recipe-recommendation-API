from src.autogen_agents_logic.guardrails import GuardrailAgents
from src.autogen_agents_logic.agents import RecipeAgents
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from src.autogen_agents_logic.pydantic_models import GuardrailPydanticModel


class Orchestrator:
    def __init__(self, user_input: str):
        self._user_input = user_input
        self._recipe_agents = RecipeAgents()
        self._guardrail_agents = GuardrailAgents()

    async def input_guardrail(self) -> GuardrailPydanticModel:
        input_guardrail_agent = self._guardrail_agents.input_guardrail_agent()
        response = await input_guardrail_agent.run(task=self._user_input)

        final_response = response.messages[-1].content

        return final_response

    async def output_guardrail(self, generated_recipe: str) -> GuardrailPydanticModel:
        output_guardrail_agent = self._guardrail_agents.output_guardrail_agent()
        response = await output_guardrail_agent.run(task=generated_recipe)

        final_response = response.messages[-1].content

        return final_response
    
    async def generate_recipe(self) -> str:
        prompt_refining_agent = self._recipe_agents.prompt_refining_agent()
        recipe_generator_agent = self._recipe_agents.recipe_generator_agent()
        reviewer_agent = self._recipe_agents.reviewer_agent()
        
        termination_condition = TextMentionTermination("APPROVE")
        
        team = RoundRobinGroupChat(
            participants=[prompt_refining_agent, recipe_generator_agent, reviewer_agent],
            termination_condition=termination_condition
        )
        
        recipe_generated = await team.run(task=self._user_input)
        
        final_response = recipe_generated.messages[-2].content
        
        return final_response

            
    