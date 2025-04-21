import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
import redis.asyncio as redis

class AIHintEngine:
    def __init__(self, redis_conn):
        self.redis = redis_conn
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.task_registry = "dev:tasks"

    async def suggest_task_fields(self, description: str, context: dict) -> dict:
        existing_tasks = await self._get_similar_tasks(description)
        assigned_to = await self._suggest_assignee(context.get('module'))
        return {
            "priority": self._suggest_priority(description),
            "dependencies": self._suggest_dependencies(existing_tasks),
            "assigned_to": assigned_to
        }

    async def _get_similar_tasks(self, query: str, threshold=0.4) -> List[dict]:
        all_tasks_raw = await self.redis.hvals(self.task_registry)
        all_tasks = [json.loads(t) for t in all_tasks_raw]
        if not all_tasks:
            return []
        descriptions = [t['description'] for t in all_tasks] + [query]
        matrix = self.vectorizer.fit_transform(descriptions)
        similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
        similar_idxs = np.where(similarities > threshold)[0]
        return [all_tasks[i] for i in similar_idxs]

    async def semantic_similarity(self, desc_a: str, desc_b: str) -> float:
        """
        Compute semantic similarity between two task descriptions using TF-IDF and cosine similarity.
        Returns a float between 0 (not similar) and 1 (identical).
        """
        matrix = self.vectorizer.fit_transform([desc_a, desc_b])
        sim = cosine_similarity(matrix[0], matrix[1])[0, 0]
        return float(sim)

    def _suggest_priority(self, text: str) -> int:
        urgency_terms = {'critical': 4, 'urgent': 3, 'important': 2}
        for k, v in urgency_terms.items():
            if k in text.lower():
                return v
        return 1

    def _suggest_dependencies(self, similar_tasks: List[dict]) -> List[str]:
        return list({t['id'] for t in similar_tasks if t.get('status') not in ['completed', 'archived']})

    async def _suggest_assignee(self, module: Optional[str]) -> Optional[str]:
        if not module:
            return None
        maintainers = await self.redis.hget("dev:module_maintainers", module)
        if maintainers:
            return maintainers.split(',')[0]
        return None
