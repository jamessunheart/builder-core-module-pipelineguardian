import time
from typing import Dict, Any, List

class PipelineGuardian:
    def __init__(self):
        self.event_log: List[Dict[str, Any]] = []

    def record_event(self, event_type: str, module: str, tool: str, error: str, suggestion: str):
        self.event_log.append({
            "event_type": event_type,
            "module": module,
            "tool": tool,
            "error": error,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "suggestion": suggestion
        })

    def get_latest_events(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.event_log[-limit:]

    def auto_analyze(self, module: str, tool: str, error: str) -> str:
        if "not found" in error.lower():
            return f"Check if '{tool}' is registered. Fallback to manual deployment if needed."
        if "missing" in error.lower():
            return f"Review parameter requirements for '{tool}' in module '{module}'."
        return "Unhandled error pattern. Manual review needed."

    def handle_error(self, module: str, tool: str, error: str):
        suggestion = self.auto_analyze(module, tool, error)
        self.record_event("tool_failure", module, tool, error, suggestion)