"""
Role-specific prompt template for the DEV Agent.
"""
from prompt_engineering import PromptTemplate, ContextInjector

def get_dev_prompt(agent, tools, project_state):
    instructions = (
        "You are the Developer agent. Focus on multi-language code generation, implementation, code review, and testing. "
        "Follow best practices and ensure maintainability."
    )
    template = PromptTemplate(
        role="DEV",
        system_instructions=instructions,
        tools=tools,
        project_state=project_state
    )
    injector = ContextInjector(agent)
    return injector.inject(template)
