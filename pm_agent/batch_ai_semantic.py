# PM Agent: Batch Pipelining, AI Hints, Semantic Conflict Resolution
import json
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import redis.asyncio as aioredis
import asyncio

class PMBatchHelper:
    def __init__(self, redis_conn):
        self.redis = redis_conn
        self.task_registry = "pm:tasks"

    async def batch_update_tasks(self, updates: List[dict], batch_size: int = 50) -> List[str]:
        updated_ids = []
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i+batch_size]
            pipe = self.redis.pipeline()
            for upd in batch:
                task_id = upd['id']
                raw = await self.redis.hget(self.task_registry, task_id)
                if raw:
                    task = json.loads(raw)
                    task.update(upd)
                    pipe.hset(self.task_registry, task_id, json.dumps(task))
                    updated_ids.append(task_id)
            await pipe.execute()
        return updated_ids

class PMAIHintEngine:
    def __init__(self, redis_conn):
        self.redis = redis_conn
        self.task_registry = "pm:tasks"
        self.vectorizer = TfidfVectorizer(stop_words='english')

    async def suggest_task_fields(self, objective: str, context: dict) -> dict:
        existing_tasks = await self._get_similar_tasks(objective)
        assigned_to = await self._suggest_assignee(context.get('module'))
        return {
            "priority": self._suggest_priority(objective),
            "dependencies": self._suggest_dependencies(existing_tasks),
            "assigned_to": assigned_to
        }

    async def _get_similar_tasks(self, objective: str) -> List[dict]:
        keys = await self.redis.hkeys(self.task_registry)
        tasks = [json.loads(await self.redis.hget(self.task_registry, k)) for k in keys]
        if not tasks:
            return []
        corpus = [t['objective'] for t in tasks]
        X = self.vectorizer.fit_transform(corpus + [objective])
        sims = cosine_similarity(X[-1], X[:-1]).flatten()
        similar = [tasks[i] for i in sims.argsort()[-3:][::-1]]
        return similar

    def _suggest_priority(self, text: str) -> int:
        urgency_terms = {"urgent": 3, "high": 2, "medium": 1, "low": 0}
        for k, v in urgency_terms.items():
            if k in text.lower():
                return v
        return 1

    def _suggest_dependencies(self, similar_tasks: List[dict]) -> List[str]:
        return list({t['id'] for t in similar_tasks if t.get('status') not in ['completed', 'archived']})

    async def _suggest_assignee(self, module: Optional[str]) -> Optional[str]:
        if not module:
            return None
        maintainers = await self.redis.hget("pm:module_maintainers", module)
        if maintainers:
            return maintainers.split(',')[0]
        return None

def semantic_conflict_resolution(task_a: dict, task_b: dict, alpha: float = 0.7, beta: float = 0.3, gamma: float = 0.5) -> dict:
    # Use both timestamp, priority, and semantic similarity
    time_score = alpha * (task_a.get('timestamp', 0) - task_b.get('timestamp', 0))
    priority_score = beta * (task_a.get('priority', 1) - task_b.get('priority', 1))
    # Semantic similarity of objectives
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([task_a['objective'], task_b['objective']])
    sim = cosine_similarity(X[0], X[1])[0][0]
    semantic_score = gamma * sim
    return task_a if (time_score + priority_score + semantic_score) >= 0 else task_b
