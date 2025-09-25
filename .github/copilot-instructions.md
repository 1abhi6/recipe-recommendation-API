# Copilot Instructions for Recipe Recommendation API

## Project Architecture
- **API Layer:** `src/api/` contains FastAPI endpoints (see `chat_api.py`).
- **Agent Logic:** `src/autogen_agents_logic/agents/` implements recipe generation logic (see `recipe_agent.py`).
- **Guardrails:** `src/autogen_agents_logic/guardrails/` enforces constraints and safety checks.
- **Model Client:** `src/autogen_agents_logic/model_client/` handles communication with OpenAI/Microsoft Autogen models.
- **Orchestration:** `src/orchestrator/main_orchestrator.py` coordinates agent, guardrail, and model interactions.
- **Prompts:** `src/prompts/` holds YAML and config for agent/guardrail prompt templates.
- **Config:** `src/config/redis_config.py` manages Redis connection.

## Key Workflows
- **Run with Docker:**
  - `docker pull iautomates/recipe-recommendation-api:v1`
  - `docker run --env-file .env -p 8000:8000 iautomates/recipe-recommendation-api:v1`
- **Local Dev:**
  - Use `uv` for dependency management: `uv pip install -e .`
  - Start API: `uvicorn main:app --reload`
- **Environment:**
  - All secrets/configs in `.env` (see `.env.example`).
  - Requires OpenAI API key and Redis details.

## Patterns & Conventions
- **Agents** are modular, each in its own file under `agents/`.
- **Guardrails** are enforced before/after model calls; see `guardrail.py`.
- **Prompt templates** are YAML-driven, loaded via `prompts_config.py`.
- **Redis** is used for caching and persistence; config in `redis_config.py`.
- **No monolithic logic:** Orchestration is separated from agent/model/guardrail logic.

## Integration Points
- **OpenAI/Microsoft Autogen:** Used via `model_client.py`.
- **Redis:** Used for storing recipes and metadata.
- **FastAPI:** Main API surface, documented at `/docs` when running.

## Examples
- To add a new agent: create a file in `agents/`, register in orchestrator.
- To add a new prompt: update YAML in `prompts/agent_prompts/` or `prompts/guardrail_prompts/`.

## References
- See `README.md` for setup, build, and run instructions.
- Explore `src/` for all core logic; each subfolder is a major component.

---
_Keep instructions concise and up-to-date. Update this file if project structure or workflows change._
