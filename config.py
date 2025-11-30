import os

# --- Telegram Bot Configuration ---
# The bot token must be set as an environment variable
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# --- AI Configuration ---
# Using the pre-configured OPENAI_API_KEY and custom base URL for Gemini 2.5 Flash
GEMINI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_BASE_URL = "https://api.gemini.com/v1" # Placeholder, will use the pre-configured OpenAI client which is set up for Gemini.
# The actual model name for Gemini 2.5 Flash
GEMINI_MODEL = "gemini-2.5-flash"

# --- Conversation States for ConversationHandler ---
# Used in the /start command for user onboarding
NAME, GOAL = range(2)

# Used in the /create command for persona selection
SELECT_PERSONA = 2

# --- User Data Keys ---
USER_DATA_NAME = "user_name"
USER_DATA_GOAL = "user_goal"
USER_DATA_PERSONA = "active_persona"
USER_DATA_HISTORY = "conversation_history"
