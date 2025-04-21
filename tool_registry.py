"""
Central Tool Registry for all agents and observability hooks.
Provides: registration, lookup, and monitoring dashboard integration.
"""

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.observers = []

    def register_tool(self, name, tool):
        self.tools[name] = tool
        self.notify_observers(f"Tool registered: {name}")

    def get_tool(self, name):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.update(event)

# Example observer for monitoring dashboard
class MonitoringDashboard:
    def __init__(self):
        self.events = []
    def update(self, event):
        self.events.append(event)
        print(f"[Monitoring] {event}")
