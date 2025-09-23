import asyncio
from src.orchestrator import Orchestrator


async def main():
    user_input = "HEy How are you!"

    orchestrator = Orchestrator(user_input=user_input)

    input_guardrail = await orchestrator.input_guardrail()

    # Check condition
    if not input_guardrail.status:
        # END the response
        print(f"Input Guardrail failed! \n User Message: {user_input}")
        print("Reponse", input_guardrail.message)

    else:
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            generated_recipe = await orchestrator.generate_recipe()
            output_guardrail = await orchestrator.output_guardrail(
                generated_recipe=generated_recipe
            )

            if output_guardrail.status:
                print("✅ Output Guardrail Passed!")
                print(f"Generated Recipe:\n{generated_recipe}")
                break
            else:
                print(f"⚠️ Output Guardrail failed on attempt {attempt}")
                if attempt == max_retries:
                    print("❌ Max retries reached. Ending execution.")
                else:
                    print("🔄 Retrying...\n")


if __name__ == "__main__":
    asyncio.run(main())
