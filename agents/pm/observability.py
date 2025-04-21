"""
Observability hooks for the PM Agent.
"""
from tool_registry import ToolRegistry, MonitoringDashboard

def setup_pm_observability():
    registry = ToolRegistry()
    dashboard = MonitoringDashboard()
    registry.register_observer(dashboard)
    registry.notify_observers("PM Agent observability initialized.")
    return registry, dashboard
