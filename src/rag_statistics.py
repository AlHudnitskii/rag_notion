import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import aiofiles
import numpy as np
from langchain_core.documents import Document
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

import config


class AnswerStatistics:
    @staticmethod
    def shannon_entropy(text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0

        freq = Counter(words)
        total = len(words)
        entropy = -sum(
            (count / total) * math.log2(count / total)
            for count in freq.values()
        )
        return round(entropy, 4)

    @staticmethod
    def lexical_diversity(text: str) -> float:
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        return round(len(set(words)) / len(words), 4)

    @staticmethod
    def jaccard_similarity(text_a: str, text_b: str) -> float:
        stop_words = {
            "и", "в", "на", "с", "для", "по", "из", "к", "о", "от", "до",
            "это", "что", "как", "не", "но", "а", "или", "если", "то",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "of", "in", "to", "and", "or", "for", "that", "this",
        }
        words_a = set(re.findall(r"\w+", text_a.lower())) - stop_words
        words_b = set(re.findall(r"\w+", text_b.lower())) - stop_words

        if not words_a or not words_b:
            return 0.0

        intersection = words_a & words_b
        union = words_a | words_b
        return round(len(intersection) / len(union), 4)

    @staticmethod
    def answer_structure_score(answer: str) -> Dict[str, Any]:
        has_headers = bool(re.search(r"^#+\s", answer, re.MULTILINE))
        has_bullets = bool(re.search(r"^[-*]\s", answer, re.MULTILINE))
        has_numbered = bool(re.search(r"^\d+\.\s", answer, re.MULTILINE))
        has_code = "```" in answer
        has_bold = bool(re.search(r"\*\*\w", answer))

        sentences = [s.strip() for s in re.split(r"[.!?]+", answer) if s.strip()]
        avg_sentence_len = (
            sum(len(s.split()) for s in sentences) / len(sentences)
            if sentences else 0
        )

        structure_score = sum([
            0.2 if has_headers else 0,
            0.2 if has_bullets or has_numbered else 0,
            0.25 if has_code else 0,
            0.15 if has_bold else 0,
            min(len(sentences) / 10, 0.2),
        ])

        return {
            "has_headers": has_headers,
            "has_bullets": has_bullets or has_numbered,
            "has_code": has_code,
            "sentence_count": len(sentences),
            "avg_sentence_len_words": round(avg_sentence_len, 2),
            "structure_score": round(structure_score, 4),
        }

    @staticmethod
    def word_frequency_distribution(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        stop_words = {
            "и", "в", "на", "с", "для", "по", "из", "к", "о", "от", "до",
            "это", "что", "как", "не", "но", "а", "или", "если", "то", "при",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "of", "in", "to", "and", "or", "for", "that", "this", "it",
        }
        words = [w for w in re.findall(r"\w{3,}", text.lower()) if w not in stop_words]
        return Counter(words).most_common(top_n)

    @classmethod
    def full_answer_analysis(cls, question: str, answer: str) -> Dict[str, Any]:
        return {
            "entropy": cls.shannon_entropy(answer),
            "lexical_diversity": cls.lexical_diversity(answer),
            "q_a_jaccard": cls.jaccard_similarity(question, answer),
            "structure": cls.answer_structure_score(answer),
            "top_words": cls.word_frequency_distribution(answer, top_n=5),
            "char_count": len(answer),
            "word_count": len(re.findall(r"\w+", answer)),
        }


class VectorStatistics:
    @staticmethod
    def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
        normed = normalize(vectors, norm="l2")
        return normed @ normed.T

    @staticmethod
    def cosine_distribution_stats(vectors: np.ndarray) -> Dict[str, float]:

        if len(vectors) < 2:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}

        sim_matrix = VectorStatistics.cosine_similarity_matrix(vectors)
        n = len(vectors)
        idx = np.triu_indices(n, k=1)
        upper = sim_matrix[idx]

        return {
            "mean": round(float(np.mean(upper)), 4),
            "std": round(float(np.std(upper)), 4),
            "min": round(float(np.min(upper)), 4),
            "max": round(float(np.max(upper)), 4),
            "median": round(float(np.median(upper)), 4),
            "q25": round(float(np.percentile(upper, 25)), 4),
            "q75": round(float(np.percentile(upper, 75)), 4),
        }

    @staticmethod
    def pca_projection(vectors: np.ndarray, n_components: int = 2) -> Dict[str, Any]:
        n_samples = len(vectors)
        if n_samples < 2:
            return {"coordinates": [], "explained_variance_ratio": [], "total_variance_explained": 0.0}

        n_components = min(n_components, n_samples, vectors.shape[1])
        pca = PCA(n_components=n_components, random_state=42)
        coords = pca.fit_transform(vectors)

        return {
            "coordinates": coords.tolist(),
            "explained_variance_ratio": [round(v, 4) for v in pca.explained_variance_ratio_],
            "total_variance_explained": round(float(np.sum(pca.explained_variance_ratio_)), 4),
        }

    @staticmethod
    def intra_cluster_distance(vectors: np.ndarray) -> float:
        if len(vectors) < 2:
            return 0.0

        normed = normalize(vectors, norm="l2")
        diffs = []
        for i in range(min(len(normed), 200)):
            for j in range(i + 1, min(len(normed), 200)):
                diffs.append(float(np.linalg.norm(normed[i] - normed[j])))

        return round(float(np.mean(diffs)), 4) if diffs else 0.0

    @staticmethod
    def vector_norm_distribution(vectors: np.ndarray) -> Dict[str, float]:
        norms = np.linalg.norm(vectors, axis=1)
        return {
            "mean_norm": round(float(np.mean(norms)), 4),
            "std_norm": round(float(np.std(norms)), 4),
            "min_norm": round(float(np.min(norms)), 4),
            "max_norm": round(float(np.max(norms)), 4),
        }

    @classmethod
    def analyze_faiss_index(cls, vectorstore) -> Dict[str, Any]:
        try:
            index = vectorstore.index
            n_vectors = index.ntotal
            dim = index.d

            if n_vectors == 0:
                return {"error": "Empty FAISS index"}

            sample_size = min(n_vectors, 500)
            vectors = np.zeros((sample_size, dim), dtype=np.float32)
            index.reconstruct_n(0, sample_size, vectors)

            config.logger.info(f"Extracted {sample_size}/{n_vectors} vectors (dim={dim}) for analysis")

            cosine_stats = cls.cosine_distribution_stats(vectors)
            pca_result = cls.pca_projection(vectors, n_components=2)
            intra_dist = cls.intra_cluster_distance(vectors)
            norm_stats = cls.vector_norm_distribution(vectors)

            return {
                "index_info": {
                    "total_vectors": n_vectors,
                    "vector_dim": dim,
                    "analyzed_sample": sample_size,
                },
                "cosine_similarity": cosine_stats,
                "pca": pca_result,
                "intra_cluster_distance": intra_dist,
                "norm_distribution": norm_stats,
            }

        except Exception as e:
            config.logger.error(f"FAISS analysis error: {e}")
            return {"error": str(e)}


class RetrievalAnswerCorrelation:
    CORRELATION_FILE = getattr(__import__("config"), "RAG_METRICS_FILE", "rag_metrics.jsonl")

    @staticmethod
    def chunk_query_cosine(
        query_embedding: np.ndarray,
        chunk_embeddings: List[np.ndarray],
    ) -> Dict[str, float]:
        if not chunk_embeddings:
            return {"mean": 0.0, "max": 0.0, "min": 0.0, "std": 0.0}

        q = query_embedding.reshape(1, -1)
        chunks = np.array(chunk_embeddings)
        sims = cosine_similarity(q, chunks)[0]

        return {
            "mean": round(float(np.mean(sims)), 4),
            "max": round(float(np.max(sims)), 4),
            "min": round(float(np.min(sims)), 4),
            "std": round(float(np.std(sims)), 4),
            "values": [round(float(s), 4) for s in sims],
        }

    @staticmethod
    def retrieval_diversity(chunk_embeddings: List[np.ndarray]) -> float:
        if len(chunk_embeddings) < 2:
            return 0.0

        chunks = np.array(chunk_embeddings)
        normed = normalize(chunks, norm="l2")
        sim_matrix = normed @ normed.T
        n = len(chunks)
        idx = np.triu_indices(n, k=1)
        mean_sim = float(np.mean(sim_matrix[idx]))
        return round(1 - mean_sim, 4)

    @classmethod
    async def save_retrieval_metrics(
        cls,
        user_id: int,
        question: str,
        retrieval_cosine_stats: Dict[str, float],
        retrieval_diversity: float,
        quality_metrics: Dict[str, float],
        feedback: Optional[str] = None,
    ) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "question_len": len(question),
            "retrieval_cosine_mean": retrieval_cosine_stats.get("mean", 0),
            "retrieval_cosine_max": retrieval_cosine_stats.get("max", 0),
            "retrieval_cosine_std": retrieval_cosine_stats.get("std", 0),
            "retrieval_diversity": retrieval_diversity,
            "quality_relevance": quality_metrics.get("relevance", 0),
            "quality_faithfulness": quality_metrics.get("faithfulness", 0),
            "quality_completeness": quality_metrics.get("completeness", 0),
            "quality_overall": quality_metrics.get("overall_score", 0),
            "feedback": feedback,
        }

        async with aiofiles.open(cls.CORRELATION_FILE, "a", encoding="utf-8") as f:
            await f.write(json.dumps(entry) + "\n")

    @classmethod
    async def compute_pearson_correlations(cls) -> Dict[str, Any]:
        try:
            async with aiofiles.open(cls.CORRELATION_FILE, "r", encoding="utf-8") as f:
                entries = [json.loads(line) async for line in f]
        except FileNotFoundError:
            return {"error": "No correlation data yet"}

        if len(entries) < 5:
            return {"error": f"Need at least 5 data points, have {len(entries)}"}

        def pearson(x: List[float], y: List[float]) -> float:
            n = len(x)
            if n < 2:
                return 0.0
            mx, my = sum(x) / n, sum(y) / n
            num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
            den_x = math.sqrt(sum((xi - mx) ** 2 for xi in x))
            den_y = math.sqrt(sum((yi - my) ** 2 for yi in y))
            if den_x == 0 or den_y == 0:
                return 0.0
            return round(num / (den_x * den_y), 4)

        cos_mean = [e["retrieval_cosine_mean"] for e in entries]
        cos_max  = [e["retrieval_cosine_max"] for e in entries]
        diversity = [e["retrieval_diversity"] for e in entries]

        quality_keys = ["quality_relevance", "quality_faithfulness", "quality_completeness", "quality_overall"]

        correlations = {}
        for qk in quality_keys:
            q_vals = [e[qk] for e in entries]
            short_name = qk.replace("quality_", "")
            correlations[short_name] = {
                "vs_cosine_mean": pearson(cos_mean, q_vals),
                "vs_cosine_max": pearson(cos_max, q_vals),
                "vs_diversity": pearson(diversity, q_vals),
            }

        feedback_entries = [e for e in entries if e.get("feedback") in ("like", "dislike")]
        feedback_analysis = {}
        if feedback_entries:
            liked = [e for e in feedback_entries if e["feedback"] == "like"]
            disliked = [e for e in feedback_entries if e["feedback"] == "dislike"]

            def safe_mean(lst, key):
                return round(sum(e[key] for e in lst) / len(lst), 4) if lst else 0.0

            feedback_analysis = {
                "like_count": len(liked),
                "dislike_count": len(disliked),
                "liked_avg_cosine_mean": safe_mean(liked, "retrieval_cosine_mean"),
                "disliked_avg_cosine_mean": safe_mean(disliked, "retrieval_cosine_mean"),
                "liked_avg_overall_quality": safe_mean(liked, "quality_overall"),
                "disliked_avg_overall_quality": safe_mean(disliked, "quality_overall"),
                "liked_avg_diversity": safe_mean(liked, "retrieval_diversity"),
                "disliked_avg_diversity": safe_mean(disliked, "retrieval_diversity"),
            }

        return {
            "total_data_points": len(entries),
            "correlations": correlations,
            "feedback_analysis": feedback_analysis,
            "interpretation": cls._interpret_correlations(correlations),
        }

    @staticmethod
    def _interpret_correlations(corr: Dict) -> List[str]:
        insights = []

        def strength(r: float) -> str:
            abs_r = abs(r)
            if abs_r >= 0.7: return "strong"
            if abs_r >= 0.4: return "moderate"
            if abs_r >= 0.2: return "weak"
            return "negligible"

        for metric, values in corr.items():
            r = values.get("vs_cosine_mean", 0)
            s = strength(r)
            direction = "positive" if r > 0 else "negative"
            if abs(r) >= 0.2:
                insights.append(
                    f"Retrieval cosine sim has {s} {direction} correlation "
                    f"(r={r}) with answer {metric}."
                )

        diversity_overall = corr.get("overall", {}).get("vs_diversity", 0)
        if abs(diversity_overall) >= 0.2:
            direction = "positive" if diversity_overall > 0 else "negative"
            insights.append(
                f"Chunk diversity has {strength(diversity_overall)} {direction} "
                f"correlation (r={diversity_overall}) with overall quality."
            )

        if not insights:
            insights.append("No strong correlations detected yet — collect more data.")

        return insights


class RAGStatisticsReport:
    @staticmethod
    async def load_quality_data() -> List[Dict]:
        try:
            async with aiofiles.open(config.QUALITY_FILE, "r", encoding="utf-8") as f:
                return [json.loads(line) async for line in f]
        except FileNotFoundError:
            return []

    @staticmethod
    async def answer_stats_from_history() -> Dict[str, Any]:
        data = await RAGStatisticsReport.load_quality_data()
        if not data:
            return {"error": "No quality data"}

        entropies = []
        diversities = []

        for entry in data:
            if "entropy" in entry:
                entropies.append(entry["entropy"])
            if "lexical_diversity" in entry:
                diversities.append(entry["lexical_diversity"])

        def safe_stats(lst):
            if not lst:
                return {}
            return {
                "mean": round(float(np.mean(lst)), 4),
                "std": round(float(np.std(lst)), 4),
                "min": round(float(np.min(lst)), 4),
                "max": round(float(np.max(lst)), 4),
            }

        return {
            "sample_size": len(data),
            "entropy_stats": safe_stats(entropies),
            "lexical_diversity_stats": safe_stats(diversities),
        }

    @classmethod
    async def full_report(cls, vectorstore=None) -> Dict[str, Any]:
        report = {
            "generated_at": datetime.now().isoformat(),
            "answer_aggregate": await cls.answer_stats_from_history(),
            "retrieval_correlation": await RetrievalAnswerCorrelation.compute_pearson_correlations(),
        }

        if vectorstore is not None:
            report["vector_index"] = VectorStatistics.analyze_faiss_index(vectorstore)

        return report
