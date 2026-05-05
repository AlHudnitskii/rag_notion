import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Set

import aiofiles

import config

_STOP_WORDS = {
    "и", "в", "на", "с", "для", "по", "из", "к", "о", "от", "до", "что", "это",
    "как", "не", "но", "а", "или", "если", "то", "при", "за", "со", "об", "то",
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "of", "to", "in",
    "and", "or", "for", "that", "this", "it", "with", "by",
}


class RAGQualityMetrics:
    # ROUGE-1 Precision  P = |W_ans ∩ W_src| / |W_ans|
    @staticmethod
    async def calculate_relevance_score(sources: List, answer: str) -> float:
        if not sources or not answer:
            return 0.0
        source_text = " ".join(s.page_content for s in sources)
        answer_words = set(re.findall(r"\w+", answer.lower())) - _STOP_WORDS
        source_words = set(re.findall(r"\w+", source_text.lower())) - _STOP_WORDS
        if not answer_words:
            return 0.0
        return round(len(answer_words & source_words) / len(answer_words), 4)


    # ROUGE-1 Recall  R = |W_ans ∩ W_src| / |W_src|
    @staticmethod
    async def calculate_source_coverage(sources: List, answer: str) -> float:
        if not sources or not answer:
            return 0.0
        source_text = " ".join(s.page_content for s in sources)
        answer_words = set(re.findall(r"\w+", answer.lower())) - _STOP_WORDS
        source_words = set(re.findall(r"\w+", source_text.lower())) - _STOP_WORDS
        if not source_words:
            return 0.0
        return round(len(answer_words & source_words) / len(source_words), 4)


    # ROUGE-1 Harmonic mean of precision and recall:  F1 = 2*P*R / (P + R)
    @staticmethod
    async def calculate_rouge1_f1(precision: float, recall: float) -> float:
        if precision + recall == 0.0:
            return 0.0
        return round(2 * precision * recall / (precision + recall), 4)


    @staticmethod
    def _get_ngrams(text: str, n: int) -> Set[str]:
        words = [w.lower() for w in re.findall(r"\w+", text) if len(w) > 2]
        if len(words) < n:
            return set()
        return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


    # ROUGE-2 Precision  Faith = |bigrams(ans) ∩ bigrams(src)| / |bigrams(ans)|
    @classmethod
    async def calculate_faithfulness(cls, sources: List, answer: str) -> float:
        if not sources or not answer:
            return 0.0
        source_text = " ".join(s.page_content for s in sources)
        answer_bigrams = cls._get_ngrams(answer, 2)
        source_bigrams = cls._get_ngrams(source_text, 2)
        if not answer_bigrams:
            return 0.0
        return round(
            sum(1 for bg in answer_bigrams if bg in source_bigrams) / len(answer_bigrams),
            4,
        )

    # Answer Completeness  C = 0.7*min(|ans|/500, 1) + 0.2*I_struct + 0.1*I_code
    @staticmethod
    async def calculate_answer_completeness(answer: str) -> float:
        if not answer:
            return 0.0
        length_score = min(len(answer) / 500, 1.0)
        has_structure = bool(re.search(r"(\n[-•*]\s|\n\d+\.\s|^#{1,4}\s)", answer, re.MULTILINE))
        has_code = "```" in answer or "def " in answer or "function" in answer
        return min((length_score * 0.7) + (0.2 if has_structure else 0) + (0.1 if has_code else 0), 1.0)


    # Response Efficiency  (piecewise-linear decay in response time)
    #   E(t) = 1.0,                             t ≤ 5 s
    #   E(t) = 1 − 0.03(t − 5),                 5 < t ≤ 15 s
    #   E(t) = max(0.7 − (t − 15)/60, 0.2),     t > 15 s
    @staticmethod
    async def calculate_response_efficiency(response_time: float) -> float:
        if response_time <= 5:
            return 1.0
        elif response_time <= 15:
            return round(1.0 - (response_time - 5) / 10 * 0.3, 4)
        else:
            return round(max(0.7 - (response_time - 15) / 60, 0.2), 4)


    # Shannon Entropy  H = −sum(p_i * log2(p_i))
    @staticmethod
    def _shannon_entropy(text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        freq = Counter(words)
        total = len(words)
        return round(-sum((c / total) * math.log2(c / total) for c in freq.values()), 4)


    # Lexical Diversity     TTR = |V| / N
    @staticmethod
    def _lexical_diversity(text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        return round(len(set(words)) / len(words), 4)

    @classmethod
    async def evaluate_rag_response(
        cls, question: str, answer: str, sources: List, response_time: float
    ) -> Dict[str, float]:
        relevance = await cls.calculate_relevance_score(sources, answer)
        source_coverage = await cls.calculate_source_coverage(sources, answer)
        rouge1_f1 = await cls.calculate_rouge1_f1(relevance, source_coverage)
        faithfulness = await cls.calculate_faithfulness(sources, answer)
        completeness = await cls.calculate_answer_completeness(answer)
        efficiency = await cls.calculate_response_efficiency(response_time)

        metrics: Dict[str, float] = {
            "relevance": relevance,
            "source_coverage": source_coverage,
            "rouge1_f1": rouge1_f1,
            "faithfulness": faithfulness,
            "completeness": completeness,
            "efficiency": efficiency,
        }

        weights = {
            "rouge1_f1": 0.25,
            "faithfulness": 0.35,
            "completeness": 0.25,
            "efficiency": 0.15,
        }
        metrics["overall_score"] = round(
            sum(metrics[k] * weights[k] for k in weights), 4
        )
        return metrics

    @staticmethod
    async def save_quality_metrics(
        user_id: int, question: str, metrics: Dict[str, float], answer: str = ""
    ) -> None:
        from rag_statistics import AnswerStatistics
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "question_length": len(question),
            "entropy": RAGQualityMetrics._shannon_entropy(answer),
            "lexical_diversity": RAGQualityMetrics._lexical_diversity(answer),
            "q_a_jaccard": AnswerStatistics.jaccard_similarity(question, answer),
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

        metric_keys = [
            "relevance", "source_coverage", "rouge1_f1",
            "faithfulness", "completeness", "efficiency", "overall_score",
            "entropy", "lexical_diversity", "q_a_jaccard",
        ]
        metrics_sum: Dict[str, float] = defaultdict(float)
        metrics_count: Dict[str, int] = defaultdict(int)
        for entry in entries:
            for key in metric_keys:
                if key in entry:
                    metrics_sum[key] += entry[key]
                    metrics_count[key] += 1

        avg_metrics = {
            k: round(metrics_sum[k] / metrics_count[k], 4)
            for k in metrics_sum if metrics_count[k] > 0
        }
        return {
            "total_evaluations": len(entries),
            "average_metrics": avg_metrics,
            "quality_distribution": {
                "excellent": sum(1 for e in entries if e.get("overall_score", 0) >= 0.8),
                "good":      sum(1 for e in entries if 0.6 <= e.get("overall_score", 0) < 0.8),
                "average":   sum(1 for e in entries if 0.4 <= e.get("overall_score", 0) < 0.6),
                "poor":      sum(1 for e in entries if e.get("overall_score", 0) < 0.4),
            },
            "latest_score": entries[-1].get("overall_score", 0),
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
