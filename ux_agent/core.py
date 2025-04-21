from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
import uuid
import json
from redis import Redis

class UXFeedback(BaseModel):
    id: str
    description: str
    assigned_to: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    context: Optional[Dict] = None
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1
    timestamp: float = datetime.now().timestamp()

class UXStateManager:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis = Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.feedback_registry = "ux:feedbacks"

    def create_feedback(self, feedback: dict) -> str:
        feedback = feedback.copy()
        for k in ['created_at', 'updated_at']:
            if k in feedback and hasattr(feedback[k], 'isoformat'):
                feedback[k] = feedback[k].isoformat()
        feedback_id = f"uxfb_{uuid.uuid4().hex}"
        self.redis.hset(self.feedback_registry, feedback_id, json.dumps(feedback))
        return feedback_id

    def get_feedback(self, feedback_id: str) -> dict:
        raw = self.redis.hget(self.feedback_registry, feedback_id)
        if not raw:
            return None
        return json.loads(raw)

    def list_feedbacks(self) -> list:
        keys = self.redis.hkeys(self.feedback_registry)
        return [json.loads(self.redis.hget(self.feedback_registry, k)) for k in keys]

    def update_feedback(self, feedback_id: str, updates: dict) -> None:
        feedback = self.get_feedback(feedback_id)
        if not feedback:
            raise ValueError("Feedback not found")
        feedback.update(updates)
        for k in ['created_at', 'updated_at']:
            if k in feedback and hasattr(feedback[k], 'isoformat'):
                feedback[k] = feedback[k].isoformat()
        self.redis.hset(self.feedback_registry, feedback_id, json.dumps(feedback))

    def resolve_conflict(self, feedback_a: dict, feedback_b: dict, alpha: float = 0.7, beta: float = 0.3) -> dict:
        time_score = alpha * (feedback_a.get('timestamp', 0) - feedback_b.get('timestamp', 0))
        priority_score = beta * (feedback_a.get('priority', 1) - feedback_b.get('priority', 1))
        return feedback_a if (time_score + priority_score) >= 0 else feedback_b
