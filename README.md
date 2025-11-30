# Persona Simulator – AI Social Practice Bot

## Concept
The Persona Simulator is a Telegram bot designed to help users practice social and professional interactions with various AI-driven characters. It's an excellent tool for soft skills training, mental resilience, and general communication practice.

## Unique Features
*   **Real-time AI Personas:** Practice talking to interviewers, investors, a crush, angry customers, therapists, and more.
*   **Personality and Memory:** Powered by **Gemini 2.5 Flash**, the AI characters maintain a consistent personality and remember the context of your conversation.
*   **Personalized Experience:** The bot asks for your name and goal during the `/start` process, which is then used to tailor the AI's system prompt for a more relevant simulation.

## Available Personas
*   Interviewer
*   Investor (Shortcut: `/investor_pitch`)
*   Crush
*   Angry Customer
*   Therapist
*   Teacher
*   Politician
*   Celebrity

## Commands
| Command | Description |
| :--- | :--- |
| `/start` | Initiates the bot and the user onboarding flow. |
| `/create` | Select a persona to start a new conversation simulation. |
| `/end` | End the current simulation and clear the conversation history. |
| `/help` | Displays a list of all available commands. |
| `/about` | Provides information about the bot's concept. |
| `/settings` | View your current user settings (name, goal). |
| `/investor_pitch` | Shortcut to start the Investor persona simulation. |

## Setup and Running Locally

### Prerequisites
1.  **Python 3.11+**
2.  **Telegram Bot Token:** Get one from BotFather on Telegram.
3.  **Gemini API Key:** The bot uses the `openai` library configured to use the Gemini API. The sandbox environment handles this automatically, but for local deployment, you would typically set the `OPENAI_API_KEY` environment variable.

### Installation
1.  Clone the repository:
    ```bash
    git clone [REPO_URL]
    cd persona_simulator_bot
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Bot
1.  Set your Telegram Bot Token as an environment variable:
    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
    ```
2.  Run the main script:
    ```bash
    python3 main.py
    ```

The bot will start polling for updates.

## Project Structure
```
persona_simulator_bot/
├── main.py             # Main entry point, sets up the bot and handlers
├── handlers.py         # Contains all Telegram command and message handlers
├── ai_service.py       # Abstraction layer for Gemini API interaction and history management
├── persona_data.py     # Defines all AI personas, system prompts, and the selection keyboard
├── config.py           # Configuration variables and constants
└── README.md           # This file
```
