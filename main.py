import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN, NAME, GOAL, SELECT_PERSONA
from handlers import (
    start_command, start_get_name, start_get_goal, help_command, about_command,
    settings_command, end_command, create_command, investor_pitch_command,
    select_persona_callback, message_handler, fallback_handler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set. Exiting.")
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable not set. Please set it to run the bot.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # --- Conversation Handlers ---

    # 1. Start/Onboarding Conversation Handler
    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_get_name)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_get_goal)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, fallback_handler)],
    )
    application.add_handler(start_conv_handler)

    # 2. Create/Persona Selection Conversation Handler
    create_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create", create_command)],
        states={
            SELECT_PERSONA: [CallbackQueryHandler(select_persona_callback, pattern='^select_')],
        },
        fallbacks=[MessageHandler(filters.COMMAND, fallback_handler)],
    )
    application.add_handler(create_conv_handler)


    # --- Command Handlers ---
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("end", end_command))
    application.add_handler(CommandHandler("investor_pitch", investor_pitch_command))

    # --- Message Handler (Must be last to catch all non-command messages) ---
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Run the bot until the user presses Ctrl-C
    print("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
