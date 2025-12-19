from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import config
from handlers import (
    button_callback,
    clear_command,
    error_handler,
    handle_message,
    help_command,
    model_command,
    reload_command,
    start_command,
    stats_command,
)
from rag_system import rag_system


def main():
    config.logger.info("Starting RagNotion bot...")
    success = rag_system.initialize()

    if not success:
        config.logger.error("Failed to initialize RagNotion system.")
        return

    application = Application.builder().token(str(config.TELEGRAM_BOT_TOKEN)).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("reload", reload_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)  # type: ignore

    application.run_polling()


if __name__ == "__main__":
    main()
