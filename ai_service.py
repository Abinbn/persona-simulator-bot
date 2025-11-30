from openai import OpenAI
from config import GEMINI_MODEL, USER_DATA_HISTORY
from persona_data import PERSONAS

# Initialize the OpenAI client, which is pre-configured to use the Gemini API
# The base_url and api_key are automatically handled by the sandbox environment
client = OpenAI()

class AIService:
    """
    Handles all interactions with the Gemini API, managing conversation history
    and persona-specific system prompts.
    """

    def __init__(self, user_data):
        """
        Initializes the service with the user_data dictionary from the Telegram context.
        This allows the service to manage the conversation history stored in user_data.
        """
        self.user_data = user_data

    def _get_history(self):
        """Retrieves or initializes the conversation history for the current chat."""
        if USER_DATA_HISTORY not in self.user_data:
            self.user_data[USER_DATA_HISTORY] = []
        return self.user_data[USER_DATA_HISTORY]

    def set_persona(self, persona_name, user_name, user_goal):
        """
        Sets the active persona and initializes the conversation history
        with the persona's system prompt, personalized with user data.
        """
        if persona_name not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona_name}")

        # 1. Format the system prompt with user-specific data
        raw_prompt = PERSONAS[persona_name]["prompt"]
        system_prompt = raw_prompt.format(user_name=user_name, user_goal=user_goal)

        # 2. Initialize the history with the system prompt
        # The Gemini API expects the system prompt as the first message in the history
        # with the 'role' set to 'system' or 'user' for the initial instruction.
        # We will use the 'user' role for the initial instruction to the model.
        self.user_data[USER_DATA_HISTORY] = [
            {"role": "user", "content": system_prompt}
        ]

        # 3. Get the AI's first message to start the conversation
        # We send an empty message to prompt the AI to start the conversation based on the system prompt
        # This is a common pattern to get the AI to speak first.
        try:
            response = client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=self.user_data[USER_DATA_HISTORY],
                temperature=0.7,
            )
            ai_response = response.choices[0].message.content
            self.user_data[USER_DATA_HISTORY].append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            print(f"Error setting persona and getting first response: {e}")
            return "Sorry, I ran into an error starting the simulation. Please try again."


    def get_response(self, user_message):
        """
        Appends the user message, calls the Gemini API with the full history,
        and appends the AI response.
        """
        history = self._get_history()

        # 1. Append user message
        history.append({"role": "user", "content": user_message})

        # 2. Call the API
        try:
            response = client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=history,
                temperature=0.7,
            )
            ai_response = response.choices[0].message.content

            # 3. Append AI response
            history.append({"role": "assistant", "content": ai_response})

            return ai_response
        except Exception as e:
            print(f"Error getting AI response: {e}")
            # Remove the last user message to prevent history corruption
            history.pop()
            return "Sorry, I ran into an error processing your message. Please try again."

    def reset_history(self):
        """Clears the conversation history."""
        if USER_DATA_HISTORY in self.user_data:
            del self.user_data[USER_DATA_HISTORY]
