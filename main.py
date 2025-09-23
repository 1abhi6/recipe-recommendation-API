import asyncio
from src.autogen_agents_logic.guardrails import GuardrailAgents
from src.autogen_agents_logic.agents import RecipeAgents
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

async def main():
    user_input = "Surprise me!"
    
    guardrail_agents = GuardrailAgents()
    recipe_agents = RecipeAgents()
    
    # Implement Input Guardrail
    input_guardrail_agent = guardrail_agents.input_guardrail_agent()
    response = await input_guardrail_agent.run(task=user_input)
    
    # Check condition
    if not response.messages[-1].content.status:
        # END the response
        pass
    
    # If input is within the context
    prompt_refining_agent = recipe_agents.prompt_refining_agent()
    recipe_generator_agent = recipe_agents.recipe_generator_agent()
    reviewer_agent = recipe_agents.reviewer_agent()
    
    termination_condition = TextMentionTermination("APPROVE")
    
    team = RoundRobinGroupChat(
        participants=[prompt_refining_agent, recipe_generator_agent, reviewer_agent],
        termination_condition=termination_condition
    )
    
    response = await team.run(task=user_input)
    
    
    print(response)
    
    print("\n\n\n")
    
    print(response.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
