"""
Role-specific prompt template for the PM Agent.
"""
from prompt_engineering import PromptTemplate, ContextInjector

def get_pm_prompt(agent, tools, project_state):
    instructions = (
        "You are the Product Manager agent. Focus on planning, risk management, resource allocation, and stakeholder coordination. "
        "Use Monte Carlo simulation for risk and adaptive scheduling."
    )
    template = PromptTemplate(
        role="PM",
        system_instructions=instructions,
        tools=tools,
        project_state=project_state
    )
    injector = ContextInjector(agent)
    return injector.inject(template)
