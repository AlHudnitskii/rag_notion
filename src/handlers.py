import asyncio
import datetime
import html
import re
from collections import defaultdict
from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import config
from analytics import Analytics
from analytics_visualizer import AnalyticsVisualizer
from rag_quality_metrics import RAGQualityMetrics
from rag_statistics import RAGStatisticsReport, RetrievalAnswerCorrelation
from rag_system import rag_system

user_contexts: Dict[int, Dict] = defaultdict(dict)


def _md_to_telegram_html(text: str) -> str:
    """Convert LLM markdown output to Telegram HTML (parse_mode='HTML')."""
    code_blocks: list[str] = []
    inline_codes: list[str] = []

    def save_fenced(m: re.Match) -> str:
        code_blocks.append(f"<pre><code>{html.escape(m.group(2))}</code></pre>")
        return f"\x00BLOCK{len(code_blocks) - 1}\x00"

    def save_inline(m: re.Match) -> str:
        inline_codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00INLINE{len(inline_codes) - 1}\x00"

    text = re.sub(r"```(\w*)\n?(.*?)```", save_fenced, text, flags=re.DOTALL)
    text = re.sub(r"`([^`\n]+)`", save_inline, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text, flags=re.DOTALL)
    text = re.sub(r"\*([^\s*][^*]*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"__(.+?)__", r"<u>\1</u>", text, flags=re.DOTALL)
    text = re.sub(r"_([^\s_][^_]*?)_", r"<i>\1</i>", text)
    text = re.sub(r"^#{1,6}\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)

    for i, block in enumerate(inline_codes):
        text = text.replace(f"\x00INLINE{i}\x00", block)
    for i, block in enumerate(code_blocks):
        text = text.replace(f"\x00BLOCK{i}\x00", block)

    return text


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data="help"), InlineKeyboardButton("📊 Statistics", callback_data="stats")],
        [InlineKeyboardButton("📈 Graphs", callback_data="graphs"), InlineKeyboardButton("🤖 Model Info", callback_data="model")],
        [InlineKeyboardButton("🔄 Update Knowledge Base", callback_data="reload")],
    ]
    await update.message.reply_text(
        f"*👋 Hello\\! I'm your Notion AI Assistant*\n\n"
        f"I can answer questions based on your Notion notes using a fully local RAG pipeline\\.\n\n"
        f"*What I can do:*\n"
        f"\\- Search and retrieve relevant notes from your Notion workspace\n"
        f"\\- Answer questions using context from those notes\n"
        f"\\- Remember our conversation history\n"
        f"\\- Show analytics and quality metrics\n\n"
        f"*Current model:* `{config.OLLAMA_MODEL}`\n\n"
        f"💬 Just send me any question to get started\\!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="MarkdownV2",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "📖 Available Commands\n\n"
        "/start    — Welcome message & main menu\n"
        "/help     — Show this help message\n"
        "/clear    — Clear conversation history\n"
        "/stats    — Usage statistics\n"
        "/quality  — RAG quality report\n"
        "/model    — Current model details\n"
        "/reload   — Reload knowledge base from Notion\n"
        "/graphs   — Usage & feedback charts\n"
        "/ragstats — Advanced RAG analytics\n\n"
        f"Active model: {config.OLLAMA_MODEL}\n"
        "Vector DB: FAISS (local)\n\n"
        "💡 Tip: after each answer you can rate it with 👍 / 👎 and view the sources used.",
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    rag_system.clear_memory(user_id)
    user_contexts[user_id].clear()
    await update.message.reply_text(
        "🗑 Conversation history cleared.\n\n"
        "You can start a fresh conversation now."
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    stats = await Analytics.get_stats()
    await update.message.reply_text(
        "📊 Usage Statistics\n"
        "─────────────────\n"
        f"Total queries:      {stats.get('total_queries', 0)}\n"
        f"Unique users:       {stats.get('unique_users', 0)}\n"
        f"Avg response time:  {stats.get('avg_response_time', 0):.1f}s\n"
        f"Avg sources used:   {stats.get('avg_sources', 0):.1f}\n\n"
        "📝 Feedback\n"
        "─────────────────\n"
        f"👍 Likes:            {stats.get('total_likes', 0)}\n"
        f"👎 Dislikes:         {stats.get('total_dislikes', 0)}\n"
        f"Satisfaction rate:  {stats.get('satisfaction_rate', 0):.0f}%\n\n"
        f"Model: {config.OLLAMA_MODEL}",
    )


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "🤖 Model Information\n"
        "─────────────────\n"
        f"Ollama URL:   {config.OLLAMA_BASE_URL}\n"
        f"Model:        {config.OLLAMA_MODEL}\n"
        f"Context:      3000 tokens\n"
        f"Temperature:  0.1\n\n"
        "📦 Embeddings\n"
        "─────────────────\n"
        f"Model:  {config.EMBEDDING_MODEL}\n"
        f"Device: CPU\n\n"
        "🗄 Vector Database\n"
        "─────────────────\n"
        f"Engine: FAISS (local)\n"
        f"Path:   {config.VECTOR_DB_PATH}",
    )


async def reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("🔄 Starting knowledge base update from Notion...")
    try:
        success = await rag_system.initialize(force_reload=True)
        if success:
            await update.message.reply_text(
                "✅ Knowledge base updated successfully!\n\n"
                "All Notion pages have been re-indexed."
            )
        else:
            await update.message.reply_text(
                "❌ Update failed.\n\n"
                "Please check the logs or try again later."
            )
    except Exception as e:
        config.logger.error(f"Error in reload_command: {e}")
        await update.message.reply_text(
            f"❌ An error occurred during update:\n{e}"
        )


async def graphs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("📈 Generating charts, please wait...")
    try:
        for generator, caption in [
            (AnalyticsVisualizer.generate_usage_chart, "📅 Usage by day"),
            (AnalyticsVisualizer.generate_response_time_chart, "⏱ Response time"),
            (AnalyticsVisualizer.generate_feedback_pie_chart, "👍 Feedback breakdown"),
            (AnalyticsVisualizer.generate_sources_histogram, "📚 Sources used per query"),
        ]:
            chart = await generator()
            if chart:
                await update.message.reply_photo(photo=chart, caption=caption)
    except Exception as e:
        config.logger.error(f"Error generating graphs: {e}")
        await update.message.reply_text("❌ Error generating graphs. Please try again later.")


async def ragstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("📊 Calculating advanced RAG statistics, please wait...")
    try:
        import io
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        report = await RAGStatisticsReport.full_report(vectorstore=rag_system.vectorstore)

        ans = report.get("answer_aggregate", {})
        ent = ans.get("entropy_stats", {})
        div_s = ans.get("lexical_diversity_stats", {})
        vec = report.get("vector_index", {})
        idx = vec.get("index_info", {})
        cos = vec.get("cosine_similarity", {})
        icd = vec.get("intra_cluster_distance", 0)
        pca_var = vec.get("pca", {}).get("total_variance_explained", 0)
        corr_data = report.get("retrieval_correlation", {})
        corr_table = corr_data.get("correlations", {})
        fb = corr_data.get("feedback_analysis", {})

        plt.rcParams.update({
            "font.family": "monospace",
            "axes.grid": True,
            "grid.alpha": 0.15,
            "grid.color": "#555555",
            "axes.spines.top": False,
            "axes.spines.right": False,
        })

        BG = "#0f0f0f"
        FG = "#e0e0e0"
        DIM = "#666666"
        C1 = "#c8c8c8"
        C2 = "#888888"
        HL = "#ffffff"

        def make_fig(w=9, h=5):
            fig, ax = plt.subplots(figsize=(w, h), facecolor=BG)
            ax.set_facecolor(BG)
            for sp in ax.spines.values():
                sp.set_color("#2a2a2a")
            ax.tick_params(colors=DIM, labelsize=9)
            ax.xaxis.label.set_color(DIM)
            ax.yaxis.label.set_color(DIM)
            return fig, ax

        def save(fig):
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=BG)
            buf.seek(0)
            plt.close(fig)
            return buf

        fig, ax = make_fig()
        ax.set_title("Answers — Shannon Entropy & Lexical Diversity", color=FG, fontsize=11, pad=12, loc="left")
        ax2 = ax.twinx()
        ax2.set_facecolor(BG)
        ax2.tick_params(colors=DIM, labelsize=9)
        for sp in ax2.spines.values():
            sp.set_color("#2a2a2a")
        e_mean = ent.get("mean", 0) or 0
        e_std = ent.get("std", 0) or 0
        e_min = ent.get("min", 0) or 0
        e_max = ent.get("max", 0) or 0
        d_mean = div_s.get("mean", 0) or 0
        d_std = div_s.get("std", 0) or 0
        vals_e = [e_min, e_mean, e_max]
        bars = ax.bar(["min", "avg", "max"], vals_e, color=[C2, HL, C2], width=0.4, zorder=3)
        ax.errorbar(["avg"], [e_mean], yerr=[e_std], fmt="none", color=DIM, capsize=6, linewidth=1.2, zorder=4)
        ax.set_ylabel("entropy", fontsize=9)
        ax.set_ylim(0, (e_max or 1) * 1.35)
        for b, v in zip(bars, vals_e):
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.08, f"{v:.3f}", ha="center", color=FG, fontsize=9)
        ax2.bar(["diversity"], [d_mean], color=C2, width=0.25, zorder=3)
        ax2.errorbar(["diversity"], [d_mean], yerr=[d_std], fmt="none", color=DIM, capsize=6, linewidth=1.2, zorder=4)
        ax2.set_ylim(0, 1.35)
        ax2.set_ylabel("TTR", fontsize=9)
        ax2.text(3.0, d_mean + d_std + 0.03, f"{d_mean:.3f} ±{d_std:.3f}", ha="center", color=FG, fontsize=9)
        ax.text(0.98, 0.97, f"n={ans.get('sample_size', 0)}", transform=ax.transAxes, ha="right", va="top", color=DIM, fontsize=9)
        fig.tight_layout()
        buf1 = save(fig)

        fig, ax = make_fig()
        ax.set_title("Vector Index — Cosine Similarity Between Chunks", color=FG, fontsize=11, pad=12, loc="left")
        c_labels = ["min", "Q25", "median", "mean", "Q75", "max"]
        c_vals = [cos.get("min", 0), cos.get("q25", 0), cos.get("median", 0), cos.get("mean", 0), cos.get("q75", 0), cos.get("max", 0)]
        c_colors = [C2, C2, C1, HL, C2, C2]
        bars3 = ax.bar(c_labels, c_vals, color=c_colors, width=0.5, zorder=3)
        for b, v in zip(bars3, c_vals):
            ypos = b.get_height() + (0.01 if v >= 0 else -0.04)
            ax.text(b.get_x() + b.get_width()/2, ypos, f"{v:.3f}", ha="center", color=FG, fontsize=9)
        ax.axhline(0, color="#333333", linewidth=0.8)
        ax.set_ylabel("cosine similarity", fontsize=9)
        ax.text(0.98, 0.97,
            f"vectors: {idx.get('total_vectors', '—')}  dim: {idx.get('vector_dim', '—')}\n"
            f"intra-dist: {icd}  PCA 2D: {pca_var:.1%}",
            transform=ax.transAxes, ha="right", va="top", color=DIM, fontsize=8, linespacing=1.6)
        fig.tight_layout()
        buf2 = save(fig)

        fig, ax = make_fig(10, 5)
        ax.set_title("Pearson r Correlations — Retrieval Quality → Answer Quality", color=FG, fontsize=11, pad=12, loc="left")
        if corr_table:
            label_map = {
                "relevance": "Relevance",
                "faithfulness": "Faithfulness",
                "completeness": "Completeness",
                "overall": "Overall",
            }
            metrics = list(corr_table.keys())
            r_cos = [corr_table[m].get("vs_cosine_mean", 0) for m in metrics]
            r_div = [corr_table[m].get("vs_diversity", 0) for m in metrics]
            labels_en = [label_map.get(m, m) for m in metrics]
            x = np.arange(len(metrics))
            w = 0.32
            b1 = ax.bar(x - w/2, r_cos, width=w, color=HL, label="cosine → quality")
            b2 = ax.bar(x + w/2, r_div, width=w, color=C2, label="diversity → quality")
            for b, v in zip(list(b1) + list(b2), r_cos + r_div):
                yoff = 0.02 if v >= 0 else -0.06
                ax.text(b.get_x() + b.get_width()/2, v + yoff, f"{v:+.3f}", ha="center", color=FG, fontsize=8)
            ax.axhline(0, color="#333333", linewidth=0.8)
            ax.axhline(0.4, color="#555555", linewidth=0.7, linestyle="--")
            ax.axhline(-0.4, color="#555555", linewidth=0.7, linestyle="--")
            ax.set_xticks(x)
            ax.set_xticklabels(labels_en, color=FG, fontsize=10)
            ax.set_ylabel("r", fontsize=9)
            ax.set_ylim(-1.15, 1.15)
            ax.legend(facecolor="#1a1a1a", edgecolor="#333333", labelcolor=FG, fontsize=8, loc="upper right")
            ax.text(0.01, 0.03, "dashed line = threshold ±0.4", transform=ax.transAxes, color=DIM, fontsize=8)
            ax.text(0.99, 0.03, f"n={corr_data.get('total_data_points', 0)}", transform=ax.transAxes, ha="right", color=DIM, fontsize=8)
        else:
            ax.axis("off")
            ax.text(0.5, 0.5, "Not enough data yet (need >= 5 queries)", ha="center", va="center", color=DIM, fontsize=11, transform=ax.transAxes)
        fig.tight_layout()
        buf3 = save(fig)

        fig, ax = make_fig(8, 5)
        ax.set_title("Feedback — Likes vs Dislikes Comparison", color=FG, fontsize=11, pad=12, loc="left")
        if fb:
            fb_metrics = ["avg cosine", "avg quality", "avg diversity"]
            liked = [fb.get("liked_avg_cosine_mean", 0), fb.get("liked_avg_overall_quality", 0), fb.get("liked_avg_diversity", 0)]
            disliked = [fb.get("disliked_avg_cosine_mean", 0), fb.get("disliked_avg_overall_quality", 0), fb.get("disliked_avg_diversity", 0)]
            x = np.arange(len(fb_metrics))
            w = 0.32
            b1 = ax.bar(x - w/2, liked, width=w, color=HL, label=f"likes ({fb.get('like_count', 0)})")
            b2 = ax.bar(x + w/2, disliked, width=w, color=C2, label=f"dislikes ({fb.get('dislike_count', 0)})")
            for b, v in zip(list(b1) + list(b2), liked + disliked):
                ax.text(b.get_x() + b.get_width()/2, v + 0.01, f"{v:.3f}", ha="center", color=FG, fontsize=9)
            ax.set_xticks(x)
            ax.set_xticklabels(fb_metrics, color=FG, fontsize=10)
            ax.set_ylim(0, max(liked + disliked) * 1.3)
            ax.set_ylabel("value", fontsize=9)
            ax.legend(facecolor="#1a1a1a", edgecolor="#333333", labelcolor=FG, fontsize=8)
            lc = fb.get("like_count", 0)
            dc = fb.get("dislike_count", 0)
            sat = lc / (lc + dc) if (lc + dc) else 0
            ax.text(0.98, 0.97, f"satisfaction {sat:.0%}", transform=ax.transAxes, ha="right", va="top", color=FG, fontsize=10)
        else:
            ax.axis("off")
            ax.text(0.5, 0.5, "No feedback data available yet", ha="center", va="center", color=DIM, fontsize=11, transform=ax.transAxes)
        fig.tight_layout()
        buf4 = save(fig)

        fig, ax = make_fig(9, 4)
        ax.axis("off")
        ax.set_title("Summary", color=FG, fontsize=11, pad=12, loc="left")
        lc = fb.get("like_count", 0)
        dc = fb.get("dislike_count", 0)
        sat_str = f"{lc/(lc+dc):.0%}" if (lc + dc) else "—"
        rows = [
            ["Queries", str(ans.get("sample_size", 0))],
            ["Entropy avg / std", f"{ent.get('mean', 0):.3f} / {ent.get('std', 0):.3f}"],
            ["Diversity avg / std", f"{div_s.get('mean', 0):.3f} / {div_s.get('std', 0):.3f}"],
            ["Vectors / dim", f"{idx.get('total_vectors', '—')} / {idx.get('vector_dim', '—')}"],
            ["Cosine avg / std", f"{cos.get('mean', 0):.3f} / {cos.get('std', 0):.3f}"],
            ["Intra-cluster dist", str(icd)],
            ["PCA variance 2D", f"{pca_var:.1%}"],
            ["Correlation records", str(corr_data.get("total_data_points", 0))],
            ["Likes / Dislikes", f"{lc} / {dc}"],
            ["Satisfaction", sat_str],
        ]
        tbl = ax.table(cellText=rows, colLabels=["Metric", "Value"], loc="center", cellLoc="left", bbox=[0, 0, 1, 1])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        for (r, c), cell in tbl.get_celld().items():
            cell.set_facecolor("#1a1a1a" if r % 2 == 0 else "#111111")
            cell.set_text_props(color=FG if r > 0 else C1, fontfamily="monospace")
            cell.set_edgecolor("#2a2a2a")
            cell.set_height(0.09)
            if r == 0:
                cell.set_facecolor("#1f1f1f")
        fig.tight_layout()
        buf5 = save(fig)

        for buf in [buf1, buf2, buf3, buf4, buf5]:
            await update.message.reply_photo(photo=buf)

    except Exception as e:
        config.logger.error(f"ragstats error: {e}")
        await update.message.reply_text(f"❌ Error generating RAG statistics: {e}")


async def _run_post_query_tasks(
    user_id: int,
    username: str,
    question: str,
    answer: str,
    sources: list,
    response_time: float,
    quality_metrics: dict,
):
    loop = asyncio.get_event_loop()
    stats = await loop.run_in_executor(None, rag_system.compute_retrieval_stats, question, sources)
    retrieval_cosine = stats["retrieval_cosine"]
    retrieval_diversity = stats["retrieval_diversity"]

    user_contexts[user_id]["retrieval_cosine"] = retrieval_cosine
    user_contexts[user_id]["retrieval_diversity"] = retrieval_diversity

    await RAGQualityMetrics.save_quality_metrics(user_id=user_id, question=question, metrics=quality_metrics, answer=answer)
    await Analytics.log_query(user_id, username, question, answer, len(sources), response_time)
    await RetrievalAnswerCorrelation.save_retrieval_metrics(
        user_id=user_id,
        question=question,
        retrieval_cosine_stats=retrieval_cosine,
        retrieval_diversity=retrieval_diversity,
        quality_metrics=quality_metrics,
        feedback=None,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    question = update.message.text

    config.logger.info(f"Question from @{username} (ID: {user_id}): {question}")
    await update.message.chat.send_action(action="typing")

    loop = asyncio.get_event_loop()
    start_time = datetime.datetime.now()
    result = await loop.run_in_executor(None, rag_system.query, question, user_id)
    response_time = float((datetime.datetime.now() - start_time).total_seconds())

    answer = result["answer"]
    sources = result["sources"]
    images = result.get("images", [])

    quality_metrics = await RAGQualityMetrics.evaluate_rag_response(
        question=question, answer=answer, sources=sources, response_time=response_time
    )

    seen_titles = set()
    unique_sources = []
    for s in sources:
        title = s.metadata.get("title", "Untitled")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_sources.append(s)

    user_contexts[user_id]["last_question"] = question
    user_contexts[user_id]["last_answer"] = answer
    user_contexts[user_id]["last_sources"] = unique_sources
    user_contexts[user_id]["last_quality"] = quality_metrics
    user_contexts[user_id]["retrieval_cosine"] = {}
    user_contexts[user_id]["retrieval_diversity"] = 0.0
    user_contexts[user_id]["feedback_given"] = False

    quality_indicator = RAGQualityMetrics.interpret_score(quality_metrics["overall_score"])

    keyboard = [
        [InlineKeyboardButton("👍 Like", callback_data="feedback_good"), InlineKeyboardButton("👎 Dislike", callback_data="feedback_bad")],
        [InlineKeyboardButton("📚 Sources", callback_data=f"sources_{user_id}"), InlineKeyboardButton("📊 Quality", callback_data=f"quality_{user_id}")],
        [InlineKeyboardButton("🗑 Clear Context", callback_data="clear_context")],
    ]

    footer = f"\n\nSources: {len(unique_sources)} | Time: {response_time:.1f}s | {quality_indicator}"
    try:
        await update.message.reply_text(
            _md_to_telegram_html(answer) + html.escape(footer, quote=False),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    except Exception:
        await update.message.reply_text(
            answer + footer,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    if images:
        try:
            await update.message.reply_photo(photo=images[0])
        except Exception as e:
            config.logger.warning(f"Failed to send image: {e}")

    asyncio.create_task(_run_post_query_tasks(
        user_id, username, question, answer, sources, response_time, quality_metrics
    ))


async def quality_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    report = await RAGQualityMetrics.get_quality_report()
    if "message" in report:
        await update.message.reply_text(report["message"])
        return
    avg = report["average_metrics"]
    dist = report["quality_distribution"]
    total = report["total_evaluations"]
    latest = report.get("latest_score", 0)

    def pct(key: str) -> str:
        v = avg.get(key)
        return f"{v:.1%}" if v is not None else "n/a"

    await update.message.reply_text(
        "📊 RAG Quality Report\n"
        "══════════════════════\n\n"
        "Word-Level Matching (ROUGE-1)\n"
        "─────────────────────────\n"
        f"Precision  (P):  {pct('relevance')}\n"
        f"Recall     (R):  {pct('source_coverage')}\n"
        f"F1-Score (P+R):  {pct('rouge1_f1')}\n\n"
        "Phrase-Level Grounding (ROUGE-2)\n"
        "─────────────────────────\n"
        f"Faithfulness:    {pct('faithfulness')}\n\n"
        "Answer Quality\n"
        "──────────────\n"
        f"Completeness:    {pct('completeness')}\n"
        f"Efficiency:      {pct('efficiency')}\n\n"
        "Lexical & Information Stats\n"
        "─────────────────────────\n"
        f"Shannon Entropy: {avg.get('entropy', 0):.3f} bits\n"
        f"Lexical Div TTR: {pct('lexical_diversity')}\n"
        f"Jaccard QA:     {pct('q_a_jaccard')}\n\n"
        "Overall Score  (weighted Σ)\n"
        "────────────────────────\n"
        f"Average:         {pct('overall_score')}\n"
        f"Latest query:    {latest:.1%}\n\n"
        "Score Distribution\n"
        "──────────────────\n"
        f"Excellent (≥80%): {dist['excellent']}\n"
        f"Good      (60–80%): {dist['good']}\n"
        f"Average   (40–60%): {dist['average']}\n"
        f"Poor      (<40%):   {dist['poor']}\n\n"
        f"Total evaluations: {total}\n\n"
        "Weights: F1=25% · Faith=35% · Complete=25% · Effic=15%",
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not update.effective_user:
        return
    await query.answer()

    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    data = query.data or ""

    if data == "help":
        if query.message:
            await query.message.reply_text(
                "📖 Available Commands\n\n"
                "/start    — Welcome message & main menu\n"
                "/help     — Show this help message\n"
                "/clear    — Clear conversation history\n"
                "/stats    — Usage statistics\n"
                "/quality  — RAG quality report\n"
                "/model    — Current model details\n"
                "/reload   — Reload knowledge base from Notion\n"
                "/graphs   — Usage & feedback charts\n"
                "/ragstats — Advanced RAG analytics\n\n"
                f"Active model: {config.OLLAMA_MODEL}"
            )

    elif data == "stats":
        if query.message:
            stats = await Analytics.get_stats()
            await query.message.reply_text(
                "📊 Usage Statistics\n"
                "─────────────────\n"
                f"Total queries:     {stats.get('total_queries', 0)}\n"
                f"Unique users:      {stats.get('unique_users', 0)}\n"
                f"Avg response time: {stats.get('avg_response_time', 0):.1f}s\n\n"
                f"👍 Likes:    {stats.get('total_likes', 0)}\n"
                f"👎 Dislikes: {stats.get('total_dislikes', 0)}\n"
                f"Satisfaction: {stats.get('satisfaction_rate', 0):.0f}%"
            )

    elif data.startswith("quality_"):
        if query.message:
            quality = user_contexts[user_id].get("last_quality", {})
            if quality:
                score = quality.get("overall_score", 0)
                label = RAGQualityMetrics.interpret_score(score)
                await query.message.reply_text(
                    "📊 Last Answer Quality\n"
                    "─────────────────\n"
                    f"Relevance:    {quality.get('relevance', 0):.1%}\n"
                    f"Faithfulness: {quality.get('faithfulness', 0):.1%}\n"
                    f"Completeness: {quality.get('completeness', 0):.1%}\n"
                    f"Efficiency:   {quality.get('efficiency', 0):.1%}\n\n"
                    f""
                    f"Overall: {label} ({score:.1%})"
                )
            else:
                await query.message.reply_text(
                    "No quality metrics available yet.\n\n"
                    "Ask a question first to see quality data."
                )

    elif data == "model":
        if query.message:
            await query.message.reply_text(
                f"🤖 Model: {config.OLLAMA_MODEL}\n"
                f"URL: {config.OLLAMA_BASE_URL}"
            )

    elif data == "graphs":
        if query.message:
            await query.message.reply_text("📈 Generating charts...")
            try:
                for generator, caption in [
                    (AnalyticsVisualizer.generate_usage_chart, "📅 Bot usage by day"),
                    (AnalyticsVisualizer.generate_response_time_chart, "⏱ Response time"),
                    (AnalyticsVisualizer.generate_feedback_pie_chart, "👍 Feedback breakdown"),
                    (AnalyticsVisualizer.generate_sources_histogram, "📚 Sources per query"),
                ]:
                    chart = await generator()
                    if chart:
                        await query.message.reply_photo(photo=chart, caption=caption)
            except Exception as e:
                await query.message.reply_text("❌ Error generating graphs. Please try again later.")

    elif data == "reload":
        if query.message:
            await query.message.reply_text("🔄 Updating knowledge base from Notion...")
            try:
                success = await rag_system.initialize(force_reload=True)
                if success:
                    await query.message.reply_text("✅ Knowledge base updated successfully!")
                else:
                    await query.message.reply_text("❌ Update failed. Please try again later.")
            except Exception as e:
                await query.message.reply_text(f"❌ Error: {e}")

    elif data.startswith("sources_"):
        if query.message:
            sources = user_contexts[user_id].get("last_sources", [])
            if sources:
                import re as _re
                def clean_title(t):
                    return _re.sub(r'^\d+\.\s*', '', t).strip() or t
                lines = ["📚 Sources used for this answer:\n"]
                for i, s in enumerate(sources, 1):
                    title = clean_title(s.metadata.get("title", "Untitled"))
                    url = s.metadata.get("source", "")
                    lines.append(f"{i}. {title}" + (f"\n   {url}" if url else ""))
                await query.message.reply_text("\n".join(lines))
            else:
                await query.message.reply_text(
                    "No sources found for this answer.\n\n"
                    "This may happen when the answer was generated without retrieving Notion pages."
                )

    elif data == "clear_context":
        rag_system.clear_memory(user_id)
        if query.message:
            await query.message.reply_text(
                "🗑 Context cleared!\n\n"
                "You can start a fresh conversation now."
            )

    elif data in ["feedback_good", "feedback_bad"]:
        if query.message:
            if user_contexts[user_id].get("feedback_given", False):
                await query.message.reply_text("You've already rated this answer!")
                return

            feedback = "like" if data == "feedback_good" else "dislike"
            question = user_contexts[user_id].get("last_question", "")
            answer = user_contexts[user_id].get("last_answer", "")

            if not question or not answer:
                await query.message.reply_text("No recent answer to rate. Ask a question first!")
                return

            await Analytics.update_feedback(user_id, username, question, answer, feedback)
            await RetrievalAnswerCorrelation.save_retrieval_metrics(
                user_id=user_id,
                question=question,
                retrieval_cosine_stats=user_contexts[user_id].get("retrieval_cosine", {}),
                retrieval_diversity=user_contexts[user_id].get("retrieval_diversity", 0.0),
                quality_metrics=user_contexts[user_id].get("last_quality", {}),
                feedback=feedback,
            )

            user_contexts[user_id]["feedback_given"] = True
            if feedback == "like":
                await query.message.reply_text(
                    "👍 Thanks for the positive feedback!\n\n"
                    "I'm glad the answer was helpful."
                )
            else:
                await query.message.reply_text(
                    "👎 Thanks for the feedback!\n\n"
                    "Try rephrasing your question or use /clear to reset context if I seem confused."
                )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config.logger.error(f"Update {update} caused error: {context.error}")
    import traceback
    config.logger.error(traceback.format_exc())
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ An unexpected error occurred.\n\n"
                "Try /clear to reset your context, or /reload to refresh the knowledge base."
            )
        except Exception as e:
            config.logger.error(f"Error while replying to error: {e}")
