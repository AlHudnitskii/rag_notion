import datetime
from collections import defaultdict
from typing import Dict

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, Update)
from telegram.ext import ContextTypes

import config
from analytics import Analytics
from analytics_visualizer import AnalyticsVisualizer
from rag_quality_metrics import RAGQualityMetrics
from rag_system import rag_system

user_contexts: Dict[int, Dict] = defaultdict(dict)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Statistics", callback_data="stats")],
        [InlineKeyboardButton("Graphs", callback_data="graphs")],
        [InlineKeyboardButton("Model", callback_data="model")],
        [InlineKeyboardButton("Update DB", callback_data="reload")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""
*Hello! I'm your local AI assistant*

*Features:*
- Fully local (Ollama + HuggingFace)
- Free and private
- Remember conversation context
- Work with your Notion notes
- Analytics with graphs

*Current model:* `{config.OLLAMA_MODEL}`

Simply ask a question!
"""

    await update.message.reply_text(
        welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    if not update.message:
        return

    help_text = f"""
*Guide*

*Commands:*
/start - Start working
/help - Show help
/clear - Clear dialog history
/stats - Statistics
/model - Model information
/reload - Update database from Notion
/graphs - Visualize statistics

*Example questions:*
• "Explain what closure is in Python"
• "Show examples of decorators in Python"
• "How does async/await work?"
• "Tell me about the Singleton pattern"

*Tips:*
• I remember context - ask follow-up questions
• Use /clear to start a new conversation
• All data is processed locally

*Configuration:*
• Model: `{config.OLLAMA_MODEL}`
• Embeddings: Local (multilingual)
• Database: Chroma (local)
"""

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /clear command."""
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    rag_system.clear_memory(user_id)

    if user_id in user_contexts:
        user_contexts[user_id].clear()

    await update.message.reply_text(
        "*Dialog history cleared!*\n\nYou can start a new conversation.",
        parse_mode="Markdown",
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /stats command."""
    if not update.message:
        return

    stats = await Analytics.get_stats()

    stats_text = f"""
*Usage Statistics*

Total queries: `{stats.get("total_queries", 0)}`
Unique users: `{stats.get("unique_users", 0)}`
Average response time: `{stats.get("avg_response_time", 0)}s`
Average number of sources: `{stats.get("avg_sources", 0)}`

*Feedback:*

Likes: `{stats.get("total_likes", 0)}`
Dislikes: `{stats.get("total_dislikes", 0)}`
Satisfaction rate: `{stats.get("satisfaction_rate", 0)}%`


Model: `{config.OLLAMA_MODEL}`
"""

    await update.message.reply_text(stats_text, parse_mode="Markdown")


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    model_info = f"""
*Model Information*

*Ollama:*
• URL: `{config.OLLAMA_BASE_URL}`
• Model: `{config.OLLAMA_MODEL}`
• Context: 4096 tokens
• Temperature: 0.1

*Embeddings:*
• Model: `{config.EMBEDDING_MODEL}`
• Device: CPU

*Vector Database:*
• Type: Faiss DB (local)
• Path: `{config.VECTOR_DB_PATH}`

*Advantages:*
- Completely free
- Data privacy
- No usage limits
"""

    await update.message.reply_text(model_info, parse_mode="Markdown")


async def reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /reload command."""
    if not update.message:
        return

    await update.message.reply_text("Starting database update...")

    try:
        success = rag_system.initialize(force_reload=True)
        if success:
            await update.message.reply_text("Database updated successfully!")
        else:
            await update.message.reply_text(
                "Error updating database.\n"
                "Please check that:\n"
                "• 'notion' folder exists\n"
                "• .md files are present in the folder\n"
                "• Ollama is running"
            )
    except Exception as e:
        config.logger.error(f"Error in reload_command: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def graphs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /graphs command."""
    if not update.message:
        return

    try:
        usage_chart = await AnalyticsVisualizer.generate_usage_chart()
        if usage_chart:
            await update.message.reply_photo(photo=usage_chart, caption="Usage by day")

        response_chart = await AnalyticsVisualizer.generate_response_time_chart()
        if response_chart:
            await update.message.reply_photo(
                photo=response_chart, caption="Response time"
            )

        feedback_chart = await AnalyticsVisualizer.generate_feedback_pie_chart()
        if feedback_chart:
            await update.message.reply_photo(photo=feedback_chart, caption="Feedback")

        sources_chart = await AnalyticsVisualizer.generate_sources_histogram()
        if sources_chart:
            await update.message.reply_photo(
                photo=sources_chart, caption="Sources used"
            )

    except Exception as e:
        config.logger.error(f"Error generating graphs: {e}")
        await update.message.reply_text("Error generating graphs")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""

    if not update.effective_user or not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    question = update.message.text

    config.logger.info(f"Question from @{username} (ID: {user_id}): {question}")

    await update.message.chat.send_action(action="typing")

    start_time = datetime.datetime.now()

    result = rag_system.query(question, user_id)

    response_time = float((datetime.datetime.now() - start_time).total_seconds())

    answer = result["answer"]
    sources = result["sources"]
    images = result.get("images", [])

    quality_metrics = await RAGQualityMetrics.evaluate_rag_response(
        question=question, answer=answer, sources=sources, response_time=response_time
    )

    await RAGQualityMetrics.save_quality_metrics(
        user_id=user_id, question=question, metrics=quality_metrics
    )

    await Analytics.log_query(
        user_id, username, question, answer, len(sources), response_time
    )

    user_contexts[user_id]["last_question"] = question
    user_contexts[user_id]["last_answer"] = answer
    user_contexts[user_id]["last_sources"] = sources
    user_contexts[user_id]["last_quality"] = quality_metrics
    user_contexts[user_id]["feedback_given"] = False

    quality_indicator = RAGQualityMetrics.interpret_score(
        quality_metrics["overall_score"]
    )

    keyboard = [
        [InlineKeyboardButton("Sources", callback_data=f"sources_{user_id}")],
        [InlineKeyboardButton("Quality", callback_data=f"quality_{user_id}")],
        [InlineKeyboardButton("Clear Context", callback_data="clear_context")],
        [
            InlineKeyboardButton("Like", callback_data="feedback_good"),
            InlineKeyboardButton("Dislike", callback_data="feedback_bad"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    formatted_answer = f"{answer}\n\n_ Sources: {len(sources)} | Time: {response_time:.1f}s | Quality: {quality_indicator}_"

    try:
        await update.message.reply_text(
            formatted_answer, parse_mode="Markdown", reply_markup=reply_markup
        )

        if images:
            if len(images) == 1:
                await update.message.reply_photo(photo=images[0])
            else:
                media_group = [InputMediaPhoto(media=url) for url in images[:10]]
                await update.message.reply_media_group(media=media_group)

    except Exception as e:
        config.logger.error(f"Error sending formatted message: {e}")
        await update.message.reply_text(
            f"{answer}\n\nSources: {len(sources)} | Time: {response_time:.1f}s",
            reply_markup=reply_markup,
        )


async def quality_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /quality command."""
    if not update.message:
        return

    report = await RAGQualityMetrics.get_quality_report()

    if "message" in report:
        await update.message.reply_text(report["message"])
        return

    avg = report["average_metrics"]
    dist = report["quality_distribution"]

    quality_text = f"""
*Report about RAG quality*

*Average metrics:*
• Relevance: `{avg.get("relevance", 0):.2%}`
• Faithfulness: `{avg.get("faithfulness", 0):.2%}`
• Completeness: `{avg.get("completeness", 0):.2%}`
• Efficiency: `{avg.get("efficiency", 0):.2%}`
• *Overall score: `{avg.get("overall_score", 0):.2%}`*

*Quality distribution:*
Excellent: `{dist["excellent"]}`
Good: `{dist["good"]}`
Average: `{dist["average"]}`
Poor: `{dist["poor"]}`

Total evaluations: `{report["total_evaluations"]}`
"""

    await update.message.reply_text(quality_text, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries."""

    query = update.callback_query

    if not query or not update.effective_user:
        return

    await query.answer()

    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    data = query.data or ""

    if data == "help":
        if query.message:
            help_text = f"""
*Guide*

*Commands:*
/start, /help, /clear, /stats, /model, /reload

*Example questions:*
• "Explain closures in Python"
• "Show decorator examples"
• "How does async/await work?"

*Configuration:*
Model: `{config.OLLAMA_MODEL}`
Embeddings: Local
Database: Chroma (local)
"""
            await query.message.reply_text(help_text, parse_mode="Markdown")

    elif data == "stats":
        if query.message:
            stats = await Analytics.get_stats()
            stats_text = f"""
*Statistics*

Queries: `{stats.get("total_queries", 0)}`
Users: `{stats.get("unique_users", 0)}`
Avg time: `{stats.get("avg_response_time", 0)}s`
Avg sources: `{stats.get("avg_sources", 0)}`
"""
            await query.message.reply_text(stats_text, parse_mode="Markdown")

    elif data.startswith("quality_"):
        if query.message:
            quality = user_contexts[user_id].get("last_quality", {})
            if quality:
                quality_text = f"""
*Quality of Last Answer:*

• Relevance: `{quality.get("relevance", 0):.1%}`
• Faithfulness: `{quality.get("faithfulness", 0):.1%}`
• Completeness: `{quality.get("completeness", 0):.1%}`
• Efficiency: `{quality.get("efficiency", 0):.1%}`

*Overall Score: {RAGQualityMetrics.interpret_score(quality.get("overall_score", 0))}*
`{quality.get("overall_score", 0):.1%}`
"""
                await query.message.reply_text(quality_text, parse_mode="Markdown")
            else:
                await query.message.reply_text("Metrics not available")

    elif data == "model":
        if query.message:
            model_info = f"""
*Model Info*

Ollama: `{config.OLLAMA_MODEL}`
URL: `{config.OLLAMA_BASE_URL}`
Embeddings: Local
Database: Chroma
"""
            await query.message.reply_text(model_info, parse_mode="Markdown")

    elif data == "graphs":
        if query.message:
            try:
                usage_chart = await AnalyticsVisualizer.generate_usage_chart()
                if usage_chart:
                    await query.message.reply_photo(
                        photo=usage_chart, caption="Bot Usage"
                    )

                response_chart = (
                    await AnalyticsVisualizer.generate_response_time_chart()
                )
                if response_chart:
                    await query.message.reply_photo(
                        photo=response_chart, caption="Response Time"
                    )

                feedback_chart = await AnalyticsVisualizer.generate_feedback_pie_chart()
                if feedback_chart:
                    await query.message.reply_photo(
                        photo=feedback_chart, caption="Feedback"
                    )

                generate_sources_histogram = (
                    await AnalyticsVisualizer.generate_sources_histogram()
                )
                if generate_sources_histogram:
                    await query.message.reply_photo(
                        photo=generate_sources_histogram, caption="Sources"
                    )

            except Exception as e:
                await query.message.reply_text("Error generating graphs")

    elif data == "reload":
        if query.message:
            await query.message.reply_text("Updating database...")
            try:
                success = rag_system.initialize(force_reload=True)
                if success:
                    await query.message.reply_text("Updated!")
                else:
                    await query.message.reply_text("Update failed")
            except Exception as e:
                await query.message.reply_text(f"Error: {str(e)}")

    elif data.startswith("sources_"):
        if query.message:
            sources = user_contexts[user_id].get("last_sources", [])
            if sources:
                sources_text = "*Sources:*\n\n"
                for i, source in enumerate(sources[:3], 1):
                    title = source.metadata.get("title", "Untitled")
                    sources_text += f"{i}. {title}\n"

                await query.message.reply_text(sources_text, parse_mode="Markdown")
            else:
                await query.message.reply_text("No sources found for this query")

    elif data == "clear_context":
        rag_system.clear_memory(user_id)
        if query.message:
            await query.message.reply_text(
                "Context cleared! Starting fresh conversation."
            )

    elif data in ["feedback_good", "feedback_bad"]:
        if query.message:
            if user_contexts[user_id].get("feedback_given", False):
                await query.message.reply_text("You've already rated this answer!")
                return

            if data == "feedback_good":
                feedback = "like"
            else:
                feedback = "dislike"
            question = user_contexts[user_id].get("last_question", "")
            answer = user_contexts[user_id].get("last_answer", "")

            if not question or not answer:
                await query.message.reply_text(
                    "Unable to save feedback - no recent query found."
                )
                return

            await Analytics.update_feedback(
                user_id, username, question, answer, feedback
            )

            user_contexts[user_id]["feedback_given"] = True

            if feedback == "like":
                await query.message.reply_text("Thank you for your positive feedback!")
            else:
                await query.message.reply_text(
                    "Thank you for your feedback!\n"
                    "Try rephrasing your question or use /clear to start fresh."
                )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""

    config.logger.error(f"Update {update} caused error: {context.error}")

    import traceback

    config.logger.error(traceback.format_exc())

    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "An error occurred. Please try:\n"
                "- /clear - to reset conversation\n"
                "- /reload - to reload database\n"
                "- Rephrase your question"
            )
        except Exception as e:
            config.logger.error(f"Error while replying to error: {e}")
