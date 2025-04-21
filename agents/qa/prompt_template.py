"""
Role-specific prompt template for the QA Agent.
"""
from prompt_engineering import PromptTemplate, ContextInjector

def get_qa_prompt(agent, tools, project_state):
    instructions = (
        "You are the QA agent. Focus on automated/manual testing, regression, compliance, and performance validation. "
        "Ensure high coverage and reliability."
    )
    template = PromptTemplate(
        role="QA",
        system_instructions=instructions,
        tools=tools,
        project_state=project_state
    )
    injector = ContextInjector(agent)
    return injector.inject(template)
