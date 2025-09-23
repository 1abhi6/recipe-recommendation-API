import os
import yaml

class PromptConfig:
    def __init__(self, config_file=None):
        if config_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(base_dir, "prompts.yaml")

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, "r", encoding="utf-8") as f:
            self.prompts = yaml.safe_load(f)

    def get_prompt(self, key: str) -> dict:
        prompt_dict = self.prompts["PROMPTS"].get(key)
        
        if prompt_dict is None:
            raise KeyError(f"Prompt '{key}' not found in config")
        
        return prompt_dict
    
response = PromptConfig().get_prompt("refine_prompt_agent")
print(response.get("system_prompt", None))