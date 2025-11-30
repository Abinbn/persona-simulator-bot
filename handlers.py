from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config import NAME, GOAL, SELECT_PERSONA, USER_DATA_NAME, USER_DATA_GOAL, USER_DATA_PERSONA
from persona_data import PERSONAS, get_persona_keyboard
from ai_service import AIService

# --- Helper Functions ---

def get_ai_service(context: ContextTypes.DEFAULT_TYPE):
    """Initializes and returns the AIService instance."""
    return AIService(context.user_data)

def is_simulation_active(context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Checks if a simulation is currently active."""
    return USER_DATA_PERSONA in context.user_data

def get_user_info(context: ContextTypes.DEFAULT_TYPE) -> tuple[str, str]:
    """Retrieves user name and goal, defaulting to placeholders if not set."""
    name = context.user_data.get(USER_DATA_NAME, "a valued user")
    goal = context.user_data.get(USER_DATA_GOAL, "to practice social skills")
    return name, goal

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the user onboarding conversation."""
    if USER_DATA_NAME in context.user_data:
        await update.message.reply_text(
            f"Welcome back, {context.user_data[USER_DATA_NAME]}! "
            "You can use /create to start a new simulation or /help for commands."
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "👋 Welcome to Persona Simulator! I'm here to help you practice your social skills. "
        "Before we begin, what is your name?"
    )
    return NAME

async def start_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's name and asks for their goal."""
    user_name = update.message.text.strip()
    context.user_data[USER_DATA_NAME] = user_name

    await update.message.reply_text(
        f"Nice to meet you, {user_name}! What is one main goal you hope to achieve by using this bot?"
    )
    return GOAL

async def start_get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's goal and ends the onboarding."""
    user_goal = update.message.text.strip()
    context.user_data[USER_DATA_GOAL] = user_goal

    await update.message.reply_text(
        "✅ Goal set! You are all set up. "
        "You can now use the /create command to select a persona and start practicing, or use /help to see all commands."
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays a list of all available commands."""
    help_text = (
        "🤖 **Persona Simulator Commands**\n\n"
        "**/start** - Begin the user onboarding process (if you haven't already).\n"
        "**/create** - Select a persona to start a new conversation simulation.\n"
        "**/end** - End the current simulation and clear the conversation history.\n"
        "**/about** - Learn more about the bot's concept and uniqueness.\n"
        "**/settings** - View your current user settings (name, goal).\n"
        "**/investor_pitch** - Shortcut to start the Investor persona simulation.\n"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provides information about the bot's concept."""
    about_text = (
        "✨ **Persona Simulator – AI Social Practice Bot**\n\n"
        "This bot is designed to help you practice real-world social interactions with AI characters "
        "that behave with personality and memory.\n\n"
        "**Why Unique?**\n"
        "We use the powerful **Gemini 2.5 Flash** model to ensure real-time, context-aware, and "
        "personality-driven conversations. It's great for education, mental resilience, "
        "relationships, and soft skills training."
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays current user settings."""
    name, goal = get_user_info(context)
    settings_text = (
        "⚙️ **Your Current Settings**\n\n"
        f"**Name:** {name}\n"
        f"**Goal:** {goal}\n\n"
        "To change these, you would need to reset your user data (feature coming soon)."
    )
    await update.message.reply_text(settings_text, parse_mode='Markdown')

async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ends the current simulation and resets the state."""
    if is_simulation_active(context):
        persona = context.user_data.pop(USER_DATA_PERSONA)
        get_ai_service(context).reset_history()
        await update.message.reply_text(
            f"🛑 Simulation with **{persona}** ended. "
            "Your conversation history has been cleared. Use /create to start a new one!",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("There is no active simulation to end.")

# --- Persona Selection Handlers ---

async def create_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the persona selection process."""
    if not USER_DATA_NAME in context.user_data:
        await update.message.reply_text(
            "Please use the /start command first to set up your profile before creating a simulation."
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🎭 **Select a Persona**\n\n"
        "Choose who you want to practice talking to:",
        reply_markup=get_persona_keyboard(),
        parse_mode='Markdown'
    )
    return SELECT_PERSONA

async def investor_pitch_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shortcut for the Investor persona."""
    await start_simulation(update, context, "Investor")

async def select_persona_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the inline button press for persona selection."""
    query = update.callback_query
    await query.answer()

    # Extract persona name from callback data (e.g., "select_Investor")
    persona_name = query.data.split('_')[1]

    # Start the simulation
    await start_simulation(update, context, persona_name)

    # End the conversation handler state
    return ConversationHandler.END

async def start_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE, persona_name: str) -> None:
    """Common function to start any simulation."""
    # Check if a simulation is already active
    if is_simulation_active(context):
        await update.effective_message.reply_text(
            f"A simulation with **{context.user_data[USER_DATA_PERSONA]}** is already active. "
            "Please use /end to finish it before starting a new one.",
            parse_mode='Markdown'
        )
        return

    # Store the active persona
    context.user_data[USER_DATA_PERSONA] = persona_name

    # Get user info for personalization
    name, goal = get_user_info(context)

    # Initialize AI service and get the first response
    ai_service = get_ai_service(context)
    first_response = ai_service.set_persona(persona_name, name, goal)

    # Send confirmation and the AI's first message
    await update.effective_message.reply_text(
        f"✅ Simulation started with **{persona_name}**!\n\n"
        f"**{persona_name}:** {first_response}",
        parse_mode='Markdown'
    )

# --- Message Handler (The main simulation loop) ---

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all non-command messages during an active simulation."""
    if not is_simulation_active(context):
        await update.message.reply_text(
            "I'm not currently in a simulation. Use /create to start one!"
        )
        return

    user_message = update.message.text
    ai_service = get_ai_service(context)

    # Get response from AI
    ai_response = ai_service.get_response(user_message)

    # Send AI response
    await update.message.reply_text(ai_response)

async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fallback for when the user is in a conversation state but sends an unexpected message."""
    await update.message.reply_text("I didn't quite catch that. Please provide a simple text response.")
