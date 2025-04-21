"""
Role-specific prompt template for the UX Agent.
"""
from prompt_engineering import PromptTemplate, ContextInjector

def get_ux_prompt(agent, tools, project_state):
    instructions = (
        "You are the UX agent. Focus on wireframing, accessibility, user feedback, A/B testing, and analytics. "
        "Prioritize user experience and accessibility."
    )
    template = PromptTemplate(
        role="UX",
        system_instructions=instructions,
        tools=tools,
        project_state=project_state
    )
    injector = ContextInjector(agent)
    return injector.inject(template)
