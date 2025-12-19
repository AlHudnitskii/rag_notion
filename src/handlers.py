import datetime
import os
from collections import defaultdict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import config
from analytics import Analytics
from rag_system import rag_system

user_contexts = defaultdict(dict)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Statistics", callback_data="stats")],
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

*Current model:* `{config.OLLAMA_MODEL}`

Simply ask a question!
"""

    await update.message.reply_text(
        welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    rag_system.clear_memory(user_id)

    await update.message.reply_text(
        "*Dialog history cleared!*\n\nYou can start a new conversation.",
        parse_mode="Markdown",
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    stats = await Analytics.get_stats()

    stats_text = f"""
*Usage Statistics*

Total queries: `{stats.get("total_queries", 0)}`
Unique users: `{stats.get("unique_users", 0)}`
Average response time: `{stats.get("avg_response_time", 0)}s`
Average number of sources: `{stats.get("avg_sources", 0)}`

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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await Analytics.log_query(
        user_id, username, question, answer, len(sources), response_time
    )

    keyboard = [
        [InlineKeyboardButton("Sources", callback_data=f"sources_{user_id}")],
        [InlineKeyboardButton("Clear Context", callback_data="clear_context")],
        [
            InlineKeyboardButton("Like", callback_data="feedback_good"),
            InlineKeyboardButton("Dislike", callback_data="feedback_bad"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    formatted_answer = (
        f"{answer}\n\n_ Sources: {len(sources)} | Time: {response_time:.1f}s_"
    )

    user_contexts[user_id]["last_sources"] = sources

    try:
        await update.message.reply_text(
            formatted_answer, parse_mode="Markdown", reply_markup=reply_markup
        )
    except Exception as e:
        config.logger.error(f"Error sending formatted message: {e}")
        await update.message.reply_text(
            f"{answer}\n\nSources: {len(sources)} | Time: {response_time:.1f}s",
            reply_markup=reply_markup,
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query or not update.effective_user:
        return

    await query.answer()

    user_id = update.effective_user.id
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
                    source_path = source.metadata.get("source", "")
                    sources_text += f"{i}. {title}\n"
                    if source_path:
                        sources_text += f"   _({os.path.basename(source_path)})_\n"

                await query.message.reply_text(sources_text, parse_mode="Markdown")
            else:
                await query.message.reply_text("No sources found for this query")

    elif data == "clear_context":
        rag_system.clear_memory(user_id)
        if query.message:
            await query.message.reply_text(
                "Context cleared! Starting fresh conversation."
            )

    elif data == "feedback_good":
        if query.message:
            await query.message.reply_text("Thank you for your feedback!")

    elif data == "feedback_bad":
        if query.message:
            await query.message.reply_text(
                "Thank you for your feedback. I'll try to improve!\n"
                "Try rephrasing your question or use /clear to start fresh."
            )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
