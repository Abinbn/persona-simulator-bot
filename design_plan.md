# Persona Simulator Telegram Bot Design Plan

## 1. Project Overview
The goal is to create a Telegram bot that allows users to practice social skills by conversing with various AI-driven personas. The bot will use the Gemini 2.5 Flash model for real-time, personality-driven interactions with memory.

## 2. Technology Stack
*   **Language:** Python 3.11+
*   **Telegram Framework:** `python-telegram-bot` (version 20.x)
*   **AI Integration:** `openai` library (configured to use the Gemini 2.5 Flash model via the pre-configured `OPENAI_API_KEY` and custom base URL).
*   **State/Memory Management:** In-memory dictionary for storing active chat sessions, user data, and conversation history. For production, this would be replaced by a database, but in-memory is sufficient for the initial implementation and sandbox testing.

## 3. Core Components and Files
| File | Description |
| :--- | :--- |
| `main.py` | Entry point. Initializes the bot, registers handlers, and starts the application. |
| `config.py` | Stores configuration variables, including the Telegram Bot Token (from environment) and AI model settings. |
| `persona_data.py` | Defines the system prompts and initial context for all available personas. |
| `handlers.py` | Contains all Telegram handler functions (commands, messages, callbacks). |
| `ai_service.py` | Abstraction layer for interacting with the Gemini API, handling conversation history and model calls. |

## 4. Conversation Flows

### 4.1. Initial User Onboarding (`/start` command)
The bot needs to gather information about the user. This will be a multi-step conversation using `ConversationHandler`.

1.  **User sends `/start`:**
    *   Bot replies: "Welcome to Persona Simulator! I'm here to help you practice your social skills. Before we begin, what is your name?"
2.  **User replies with name:**
    *   Bot stores name.
    *   Bot replies: "Nice to meet you, [Name]! What is one main goal you hope to achieve by using this bot?"
3.  **User replies with goal:**
    *   Bot stores goal.
    *   Bot replies: "Great! Your goal is set. You can now use the `/create` command to select a persona and start practicing, or use `/help` to see all commands."

### 4.2. Persona Selection (`/create` command)
1.  **User sends `/create`:**
    *   Bot replies with a list of personas using an inline keyboard.
    *   **Personas:** Interviewer, Investor, Crush, Angry Customer, Therapist, Teacher, Politician, Celebrity.
2.  **User selects a persona (e.g., 'Investor'):**
    *   Bot sets the active persona for the chat session.
    *   Bot initializes the conversation history with the persona's system prompt.
    *   Bot replies: "Simulation started! You are now pitching to a skeptical venture capitalist. Start your pitch!"

### 4.3. Simulation Loop (General Message Handler)
1.  **User sends a message:**
    *   The message is appended to the session's conversation history.
    *   The entire history (including the system prompt) is sent to the Gemini API.
    *   The model generates a response based on the persona.
2.  **Bot sends AI response:**
    *   The AI response is appended to the conversation history.
    *   The simulation continues until the user sends a command to stop (e.g., `/end`).

## 5. Command Definitions
| Command | Description | Handler |
| :--- | :--- | :--- |
| `/start` | Initiates the bot and the user onboarding flow. | `start_handler` |
| `/help` | Displays a list of all available commands and a brief explanation. | `help_handler` |
| `/about` | Provides information about the bot's concept and uniqueness. | `about_handler` |
| `/settings` | Placeholder for future settings (e.g., reset user data). | `settings_handler` |
| `/create` | Starts the persona selection process. | `create_handler` |
| `/end` | Ends the current simulation and resets the persona state. | `end_handler` |
| `/investor_pitch` | Shortcut to start the Investor persona simulation. | `investor_pitch_handler` |

## 6. AI Persona Definitions (System Prompts)
The system prompt is crucial for defining the AI's behavior and memory.

| Persona | System Prompt Snippet |
| :--- | :--- |
| **Interviewer** | "You are a professional, sharp-witted interviewer for a top-tier tech company. Your goal is to assess the user's technical skills, cultural fit, and problem-solving abilities. Be challenging but fair." |
| **Investor** | "You are a skeptical, tough-to-impress venture capitalist on a show like Shark Tank. You have a limited budget and high standards. Ask probing questions about the user's business model, market size, and team. Your memory of the user's pitch must be perfect." |
| **Crush** | "You are the user's romantic crush. You are charming, slightly mysterious, and have a good sense of humor. Respond in a flirty, engaging, and sometimes elusive manner. Remember the user's name and goal from the `/start` flow." |
| **Angry Customer** | "You are an extremely frustrated customer whose expensive product has failed catastrophically. You are demanding, emotional, and expect an immediate, high-level resolution. Do not accept simple apologies." |
| **Therapist** | "You are a compassionate, non-judgmental cognitive behavioral therapist. Your responses should be empathetic, reflective, and guide the user toward self-discovery and coping mechanisms." |
| **Teacher** | "You are a strict but knowledgeable high school history teacher. You are giving the user a pop quiz on World War II. Your tone is formal and academic. Correct the user's mistakes precisely." |
| **Politician** | "You are a charismatic, evasive, and highly experienced politician running for a major office. When asked a direct question, pivot to your talking points, use vague language, and appeal to a broad base." |
| **Celebrity** | "You are a famous, slightly eccentric Hollywood actor known for your dramatic roles and love of obscure philosophy. Your responses should be grand, self-referential, and occasionally quote Shakespeare." |

## 7. AI Service Implementation (`ai_service.py`)
The `AIService` class will handle:
*   Initialization with the model name (`gemini-2.5-flash`).
*   A method `get_response(chat_id, user_message)` that:
    1.  Retrieves the conversation history for `chat_id`.
    2.  Appends the `user_message`.
    3.  Calls the Gemini API.
    4.  Appends the AI response to the history.
    5.  Returns the AI response text.
*   A method `set_persona(chat_id, persona_name)` to initialize the history with the system prompt.
*   A method to store and retrieve user-specific data (name, goal) to be injected into the system prompt for personalization.
