"""
Prompt Engineering module for role-specific templates and dynamic context injection.
"""
from typing import Dict, Any

class PromptTemplate:
    def __init__(self, role: str, system_instructions: str, tools: list, project_state: Dict[str, Any]):
        self.role = role
        self.system_instructions = system_instructions
        self.tools = tools
        self.project_state = project_state

    def render(self, memory: Dict[str, Any], status: Dict[str, Any]) -> str:
        prompt = f"""
Role: {self.role}\n"""
        prompt += f"System Instructions: {self.system_instructions}\n"
        prompt += f"Available Tools: {', '.join(self.tools)}\n"
        prompt += f"Project State: {self.project_state}\n"
        prompt += f"Memory: {memory}\n"
        prompt += f"Status: {status}\n"
        return prompt

class ContextInjector:
    def __init__(self, agent):
        self.agent = agent

    def get_context(self):
        # Gather dynamic memory and status for the agent
        return {
            "memory": getattr(self.agent, "memory", {}),
            "status": getattr(self.agent, "status", {})
        }

    def inject(self, prompt_template: PromptTemplate) -> str:
        context = self.get_context()
        return prompt_template.render(memory=context["memory"], status=context["status"])
