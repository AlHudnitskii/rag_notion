import json
from decimal import Decimal
from typing import Dict

import aiofiles

import config
from models import FeedbackEntry, QueryLog


class Analytics:
    """Class for tracking and saving analytics data."""

    @staticmethod
    async def log_query(
        user_id: int,
        username: str,
        question: str,
        answer: str,
        sources_count: int,
        response_time: Decimal,
    ) -> None:
        """Log a query with Pydantic model validation."""
        log_entry = QueryLog(
            user_id=user_id,
            username=username,
            question=question,
            answer_length=len(answer),
            sources_count=sources_count,
            response_time=response_time,
            model=config.OLLAMA_MODEL,
        )

        async with aiofiles.open(config.ANALYTICS_FILE, "a", encoding="utf-8") as f:
            await f.write(log_entry.model_dump_json() + "\n")

    @staticmethod
    async def update_feedback(
        user_id: int,
        username: str,
        question: str,
        answer: str,
        feedback: str,
    ) -> None:
        """Save user feedback separately for analysis."""
        feedback_entry = FeedbackEntry(
            user_id=user_id,
            username=username,
            question=question,
            answer_preview=answer[:100],
            feedback=feedback,
        )

        feedback_file = config.FEEDBACK_FILE
        async with aiofiles.open(feedback_file, "a", encoding="utf-8") as f:
            await f.write(feedback_entry.model_dump_json() + "\n")

    @staticmethod
    async def get_stats() -> Dict:
        try:
            async with aiofiles.open(config.ANALYTICS_FILE, "r", encoding="utf-8") as f:
                logs = [json.loads(line) async for line in f]

            if not logs:
                return {"total_queries": 0}

            users = set(log["user_id"] for log in logs)
            avg_response_time = sum(log["response_time"] for log in logs) / len(logs)
            avg_sources = sum(log["sources_count"] for log in logs) / len(logs)

            return {
                "total_queries": len(logs),
                "unique_users": len(users),
                "avg_response_time": round(avg_response_time, 2),
                "avg_sources": round(avg_sources, 2),
            }
        except FileNotFoundError:
            return {"total_queries": 0}
