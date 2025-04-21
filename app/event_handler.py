def handle_event(event):
    # Simulated event handler for testing
    data = event.get("data", "")
    severity = event.get("severity", "INFO")
    if not data:
        return "ignored"
    if severity == "ERROR":
        return "error"
    return "processed"
