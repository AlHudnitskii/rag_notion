import io
import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import aiofiles
import matplotlib.pyplot as plt

import config


class AnalyticsVisualizer:
    """Creating analytics visualizations"""

    @staticmethod
    async def load_analytics_data() -> List[Dict]:
        """Load analytics data"""
        try:
            async with aiofiles.open(config.ANALYTICS_FILE, "r", encoding="utf-8") as f:
                logs = [json.loads(line) async for line in f]
            return logs
        except FileNotFoundError:
            return []

    @staticmethod
    async def load_feedback_data() -> List[Dict]:
        """Load feedback data"""
        try:
            async with aiofiles.open(
                config.ANALYTICS_FILE.replace(".jsonl", "_feedback.jsonl"),
                "r",
                encoding="utf-8",
            ) as f:
                feedback = [json.loads(line) async for line in f]
            return feedback
        except FileNotFoundError:
            return []

    @staticmethod
    async def generate_usage_chart() -> io.BytesIO:
        """Generate usage chart"""
        logs = await AnalyticsVisualizer.load_analytics_data()

        if not logs:
            return None

        daily_counts = defaultdict(int)
        for log in logs:
            timestamp = datetime.fromisoformat(log["timestamp"])
            date_key = timestamp.date()
            daily_counts[date_key] += 1

        sorted_dates = sorted(daily_counts.keys())
        counts = [daily_counts[date] for date in sorted_dates]

        fig, ax = plt.subplots(figsize=(10, 6))

        x_positions = range(len(sorted_dates))
        ax.bar(x_positions, counts, color="#5865F2", alpha=0.8, width=0.6)

        ax.set_xticks(x_positions)
        ax.set_xticklabels(
            [date.strftime("%d.%m") for date in sorted_dates], rotation=45, ha="right"
        )

        ax.set_title(
            "Amount of requests per day", fontsize=14, fontweight="bold", pad=20
        )
        ax.set_xlabel("Date", fontsize=11)
        ax.set_ylabel("Amount of requests", fontsize=11)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf

    @staticmethod
    async def generate_response_time_chart() -> io.BytesIO:
        """Generate response time chart"""
        logs = await AnalyticsVisualizer.load_analytics_data()

        if not logs:
            return None

        recent_logs = logs[-50:] if len(logs) > 50 else logs

        response_times = [log["response_time"] for log in recent_logs]
        indices = list(range(1, len(response_times) + 1))
        avg_time = sum(response_times) / len(response_times)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            indices,
            response_times,
            marker="o",
            linewidth=2,
            markersize=4,
            color="#57F287",
            alpha=0.7,
            label="Response Time",
        )
        ax.axhline(
            y=avg_time,
            color="#ED4245",
            linestyle="--",
            linewidth=2,
            label=f"Average: {avg_time:.1f}s",
        )

        ax.set_title(
            "Response Time (Last Requests)", fontsize=14, fontweight="bold", pad=20
        )
        ax.set_xlabel("Request Number", fontsize=11)
        ax.set_ylabel("Time (sec)", fontsize=11)
        ax.legend(loc="upper right")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf

    @staticmethod
    async def generate_feedback_pie_chart() -> io.BytesIO:
        """Pie chart feedback"""
        feedback = await AnalyticsVisualizer.load_feedback_data()

        if not feedback:
            return None

        likes = sum(1 for f in feedback if f["feedback"] == "like")
        dislikes = sum(1 for f in feedback if f["feedback"] == "dislike")

        if likes == 0 and dislikes == 0:
            return None

        fig, ax = plt.subplots(figsize=(8, 8))

        colors = ["#57F287", "#ED4245"]
        labels = [f"Like\n({likes})", f"Dislike\n({dislikes})"]
        sizes = [likes, dislikes]
        explode = (0.05, 0)

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            explode=explode,
            textprops={"fontsize": 12, "weight": "bold"},
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(14)

        ax.set_title("User Feedback", fontsize=14, fontweight="bold", pad=20)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf

    @staticmethod
    async def generate_sources_histogram() -> io.BytesIO:
        """Generate sources histogram"""
        logs = await AnalyticsVisualizer.load_analytics_data()

        if not logs:
            return None

        sources_counts = [int(log["sources_count"]) for log in logs]

        if not sources_counts:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        max_sources = max(sources_counts)
        bins = list(range(0, max_sources + 2))

        ax.hist(
            sources_counts,
            bins=bins,
            color="#FEE75C",
            edgecolor="black",
            alpha=0.7,
            rwidth=0.8,
        )

        ax.set_title("Histogram of Sources", fontsize=14, fontweight="bold", pad=20)
        ax.set_xlabel("Number of Sources", fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        n, bins_edges, patches = ax.hist(
            sources_counts, bins=bins, color="#FEE75C", edgecolor="black", alpha=0
        )
        for i, (count, x) in enumerate(zip(n, bins_edges[:-1])):
            if count > 0:
                ax.text(
                    x + 0.5,
                    count,
                    int(count),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                )

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf
