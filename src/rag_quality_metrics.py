import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

import aiofiles

import config


class RAGQualityMetrics:
    """Class for managing and storing RAG quality metrics."""

    @staticmethod
    async def calculate_relevance_score(sources: List, answer: str) -> float:
        """Calculate the relevance score for a given answer based on sources."""

        if not sources or not answer:
            return 0.0

        source_texts = " ".join([s.page_content for s in sources])

        answer_words = set(answer.lower().split())
        source_words = set(source_texts.lower().split())

        stop_words = {
            "и",
            "в",
            "на",
            "с",
            "для",
            "по",
            "из",
            "к",
            "о",
            "от",
            "до",
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
        }
        answer_words -= stop_words
        source_words -= stop_words

        if not answer_words:
            return 0.0

        intersection = answer_words & source_words
        relevance = len(intersection) / len(answer_words)

        return min(relevance, 1.0)

    @staticmethod
    async def calculate_context_utilization(
        question: str, sources: List, answer: str
    ) -> float:
        """Calculate the context utilization score for a given answer based on sources."""
        if not sources:
            return 0.0

        source_count = len(sources)
        optimal_sources = 3
        utilization = min(source_count / optimal_sources, 1.0)

        return utilization

    @staticmethod
    async def calculate_answer_completeness(answer: str) -> float:
        """Calculate the completeness score for a given answer."""
        if not answer:
            return 0.0

        length_score = min(len(answer) / 500, 1.0)

        has_structure = bool(
            "\n" in answer or any(marker in answer for marker in ["-", "•", "1.", "2."])
        )
        structure_score = 0.2 if has_structure else 0.0

        has_code = "```" in answer or "def " in answer or "function" in answer
        code_bonus = 0.1 if has_code else 0.0

        completeness = min((length_score * 0.7) + structure_score + code_bonus, 1.0)

        return completeness

    @staticmethod
    async def calculate_response_efficiency(response_time: float) -> float:
        """Calculate the efficiency score for a given response time."""
        if response_time <= 5:
            return 1.0
        elif response_time <= 15:
            return 1.0 - ((response_time - 5) / 10) * 0.3
        else:
            return max(0.7 - ((response_time - 15) / 30) * 0.5, 0.2)

    @classmethod
    async def evaluate_rag_response(
        cls, question: str, answer: str, sources: List, response_time: float
    ) -> Dict[str, float]:
        """Evaluate the quality of a RAG response."""
        metrics = {
            "relevance": await cls.calculate_relevance_score(sources, answer),
            "context_utilization": await cls.calculate_context_utilization(
                question, sources, answer
            ),
            "completeness": await cls.calculate_answer_completeness(answer),
            "efficiency": await cls.calculate_response_efficiency(response_time),
        }

        weights = {
            "relevance": 0.35,
            "context_utilization": 0.25,
            "completeness": 0.25,
            "efficiency": 0.15,
        }

        overall_score = sum(metrics[key] * weights[key] for key in metrics)
        metrics["overall_score"] = overall_score

        return metrics

    @staticmethod
    async def save_quality_metrics(
        user_id: int, question: str, metrics: Dict[str, float]
    ) -> None:
        """Save quality metrics"""
        quality_file = config.QUALITY_FILE
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "question_length": len(question),
            **metrics,
        }

        async with aiofiles.open(quality_file, "a", encoding="utf-8") as f:
            await f.write(json.dumps(entry) + "\n")

    @staticmethod
    async def get_quality_report() -> Dict:
        """Get quality report"""
        quality_file = config.ANALYTICS_FILE.replace(".jsonl", "_quality.jsonl")

        try:
            async with aiofiles.open(quality_file, "r", encoding="utf-8") as f:
                entries = [json.loads(line) async for line in f]
        except FileNotFoundError:
            return {"message": "No quality data available"}

        if not entries:
            return {"message": "No quality data available"}

        metrics_sum = defaultdict(float)
        metrics_count = defaultdict(int)

        for entry in entries:
            for key in [
                "relevance",
                "context_utilization",
                "completeness",
                "efficiency",
                "overall_score",
            ]:
                if key in entry:
                    metrics_sum[key] += entry[key]
                    metrics_count[key] += 1

        avg_metrics = {
            key: round(metrics_sum[key] / metrics_count[key], 3)
            for key in metrics_sum
            if metrics_count[key] > 0
        }

        quality_distribution = {
            "excellent": sum(1 for e in entries if e.get("overall_score", 0) >= 0.8),
            "good": sum(1 for e in entries if 0.6 <= e.get("overall_score", 0) < 0.8),
            "average": sum(
                1 for e in entries if 0.4 <= e.get("overall_score", 0) < 0.6
            ),
            "poor": sum(1 for e in entries if e.get("overall_score", 0) < 0.4),
        }

        return {
            "total_evaluations": len(entries),
            "average_metrics": avg_metrics,
            "quality_distribution": quality_distribution,
            "latest_score": entries[-1].get("overall_score", 0) if entries else 0,
        }

    @staticmethod
    def interpret_score(score: float) -> str:
        """Interprets the overall score into a human-readable string."""
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Average"
        else:
            return "Poor"
