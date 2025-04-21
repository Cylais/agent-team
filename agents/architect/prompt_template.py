"""
Role-specific prompt template for the TA Agent.
"""
from prompt_engineering import PromptTemplate, ContextInjector

def get_ta_prompt(agent, tools, project_state):
    instructions = (
        "You are the Technical Architect agent. Focus on architecture, tech stack, security, scalability, and API design. "
        "Ensure robustness and future-proofing."
    )
    template = PromptTemplate(
        role="TA",
        system_instructions=instructions,
        tools=tools,
        project_state=project_state
    )
    injector = ContextInjector(agent)
    return injector.inject(template)
