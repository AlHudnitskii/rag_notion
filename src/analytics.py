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

        async with aiofiles.open(config.FEEDBACK_FILE, "a", encoding="utf-8") as f:
            await f.write(feedback_entry.model_dump_json() + "\n")

    @staticmethod
    async def get_stats() -> Dict:
        """Reads and counts likes/dislikes from FEEDBACK_FILE."""
        result = {
            "total_queries": 0,
            "unique_users": 0,
            "avg_response_time": 0,
            "avg_sources": 0,
            "total_likes": 0,
            "total_dislikes": 0,
            "satisfaction_rate": 0,
        }

        try:
            async with aiofiles.open(config.ANALYTICS_FILE, "r", encoding="utf-8") as f:
                logs = [json.loads(line) async for line in f]

            if logs:
                users = set(log["user_id"] for log in logs)
                avg_response_time = sum(log["response_time"] for log in logs) / len(logs)
                avg_sources = sum(log["sources_count"] for log in logs) / len(logs)

                result.update({
                    "total_queries": len(logs),
                    "unique_users": len(users),
                    "avg_response_time": round(avg_response_time, 2),
                    "avg_sources": round(avg_sources, 2),
                })
        except FileNotFoundError:
            pass

        try:
            async with aiofiles.open(config.FEEDBACK_FILE, "r", encoding="utf-8") as f:
                feedback_logs = [json.loads(line) async for line in f]

            total_likes = sum(1 for f in feedback_logs if f.get("feedback") == "like")
            total_dislikes = sum(1 for f in feedback_logs if f.get("feedback") == "dislike")
            total_feedback = total_likes + total_dislikes
            satisfaction_rate = round((total_likes / total_feedback) * 100, 1) if total_feedback > 0 else 0

            result.update({
                "total_likes": total_likes,
                "total_dislikes": total_dislikes,
                "satisfaction_rate": satisfaction_rate,
            })
        except FileNotFoundError:
            pass

        return result
