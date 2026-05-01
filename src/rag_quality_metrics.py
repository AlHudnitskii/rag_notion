import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Set

import aiofiles

import config


class RAGQualityMetrics:
    @staticmethod
    async def calculate_relevance_score(sources: List, answer: str) -> float:
        if not sources or not answer:
            return 0.0
        source_texts = " ".join([s.page_content for s in sources])
        answer_words = set(answer.lower().split())
        source_words = set(source_texts.lower().split())
        stop_words = {
            "и","в","на","с","для","по","из","к","о","от","до","что","это",
            "как","не","но","а","или","если","то","the","a","an","is","are",
            "was","were","be","been","of","to",
        }
        answer_words -= stop_words
        source_words -= stop_words
        if not answer_words:
            return 0.0
        return min(len(answer_words & source_words) / len(answer_words), 1.0)

    @staticmethod
    def _get_ngrams(text: str, n: int) -> Set[str]:
        words = [w.lower() for w in re.findall(r'\w+', text) if len(w) > 2]
        if len(words) < n:
            return set()
        return set(" ".join(words[i:i+n]) for i in range(len(words) - n + 1))

    @classmethod
    async def calculate_faithfulness(cls, sources: List, answer: str) -> float:
        if not sources or not answer:
            return 0.0
        source_text = " ".join([s.page_content for s in sources])
        answer_bigrams = cls._get_ngrams(answer, 2)
        source_bigrams = cls._get_ngrams(source_text, 2)
        if not answer_bigrams:
            return 0.0
        return sum(1 for bg in answer_bigrams if bg in source_bigrams) / len(answer_bigrams)

    @staticmethod
    async def calculate_answer_completeness(answer: str) -> float:
        if not answer:
            return 0.0
        length_score = min(len(answer) / 500, 1.0)
        has_structure = "\n" in answer or any(m in answer for m in ["-", "•", "1.", "2."])
        has_code = "```" in answer or "def " in answer or "function" in answer
        return min((length_score * 0.7) + (0.2 if has_structure else 0) + (0.1 if has_code else 0), 1.0)

    @staticmethod
    async def calculate_response_efficiency(response_time: float) -> float:
        if response_time <= 5:
            return 1.0
        elif response_time <= 15:
            return 1.0 - ((response_time - 5) / 10) * 0.3
        else:
            return max(0.7 - ((response_time - 15) / 30) * 0.5, 0.2)

    @staticmethod
    def _shannon_entropy(text: str) -> float:
        import math
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        freq = Counter(words)
        total = len(words)
        return round(-sum((c/total) * math.log2(c/total) for c in freq.values()), 4)

    @staticmethod
    def _lexical_diversity(text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        return round(len(set(words)) / len(words), 4)

    @classmethod
    async def evaluate_rag_response(cls, question: str, answer: str, sources: List, response_time: float) -> Dict[str, float]:
        metrics = {
            "relevance": await cls.calculate_relevance_score(sources, answer),
            "faithfulness": await cls.calculate_faithfulness(sources, answer),
            "completeness": await cls.calculate_answer_completeness(answer),
            "efficiency": await cls.calculate_response_efficiency(response_time),
        }
        weights = {"relevance": 0.25, "faithfulness": 0.35, "completeness": 0.25, "efficiency": 0.15}
        metrics["overall_score"] = sum(metrics[k] * weights[k] for k in weights)
        return metrics

    @staticmethod
    async def save_quality_metrics(user_id: int, question: str, metrics: Dict[str, float], answer: str = "") -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "question_length": len(question),
            # FIX: save entropy and lexical_diversity so ragstats can read them
            "entropy": RAGQualityMetrics._shannon_entropy(answer),
            "lexical_diversity": RAGQualityMetrics._lexical_diversity(answer),
            **metrics,
        }
        async with aiofiles.open(config.QUALITY_FILE, "a", encoding="utf-8") as f:
            await f.write(json.dumps(entry) + "\n")

    @staticmethod
    async def get_quality_report() -> Dict:
        try:
            async with aiofiles.open(config.QUALITY_FILE, "r", encoding="utf-8") as f:
                entries = [json.loads(line) async for line in f]
        except FileNotFoundError:
            return {"message": "No quality data available yet"}
        if not entries:
            return {"message": "No quality data available yet"}

        metrics_sum = defaultdict(float)
        metrics_count = defaultdict(int)
        for entry in entries:
            for key in ["relevance", "faithfulness", "completeness", "efficiency", "overall_score"]:
                if key in entry:
                    metrics_sum[key] += entry[key]
                    metrics_count[key] += 1

        avg_metrics = {k: round(metrics_sum[k] / metrics_count[k], 3) for k in metrics_sum if metrics_count[k] > 0}
        return {
            "total_evaluations": len(entries),
            "average_metrics": avg_metrics,
            "quality_distribution": {
                "excellent": sum(1 for e in entries if e.get("overall_score", 0) >= 0.8),
                "good": sum(1 for e in entries if 0.6 <= e.get("overall_score", 0) < 0.8),
                "average": sum(1 for e in entries if 0.4 <= e.get("overall_score", 0) < 0.6),
                "poor": sum(1 for e in entries if e.get("overall_score", 0) < 0.4),
            },
            "latest_score": entries[-1].get("overall_score", 0) if entries else 0,
        }

    @staticmethod
    def interpret_score(score: float) -> str:
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Average"
        else:
            return "Poor"
