# backend/services/gemini_service.py
import os
import sys
import logging
import traceback
from pathlib import Path

# config.pyをインポートするためにbackendディレクトリをパスに追加
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

try:
    from config import Config
except ImportError as e:
    print(f"--- [CRITICAL] Could not import Config. Ensure backend/config.py exists and the script is run from a valid location. Error: {e} ---")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='--- [%(levelname)s] %(message)s ---')

try:
    from google.generativeai.client import configure
    from google.generativeai.generative_models import GenerativeModel
    from google.api_core.exceptions import ResourceExhausted
except ImportError as e:
    print(f"--- [ERROR] Failed to import from google.generativeai: {e} ---")
    print("--- [INFO] Please install: pip install google-generativeai ---")
    logging.critical(f"Failed to import from google.generativeai: {e}")
    logging.info("Please install: pip install google-generativeai")
    raise


class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    Initializes the model on creation and provides a method to chat.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initializes the Gemini client and model."""
        self.model = None
        try:
            # Get the API key from config
            api_key = Config.GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY is not set in .env file")

            # Clean the key just in case
            api_key = api_key.strip().strip('"').strip("'")

            logging.info("Attempting to configure Gemini API key...")
            configure(api_key=api_key)
            logging.info("Gemini API key configured successfully.")

            # Get model name from config, but override with supported model
            model_name = "gemini-2.5-flash"  # Use supported model instead of deprecated gemini-1.5-flash
            logging.info(f"Using Gemini Model: {model_name}")

            self.model = GenerativeModel(model_name)
            logging.info("Gemini model initialized successfully.")

        except AttributeError as e:
            logging.critical(f"AttributeError during initialization: {e}")
            logging.info("This might be due to an incorrect google-generativeai version. Try: pip install --upgrade google-generativeai")
            raise
        except Exception as e:
            logging.critical(f"Failed to initialize Gemini Service: {e}")
            logging.critical(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            raise

    def chat(self, user_message: str) -> str | None:
        """
        Sends a user message to the Gemini API and returns the response.

        Args:
            user_message (str): The message from the user.

        Returns:
            str | None: The response text from Gemini, or None if an error occurs.
        """
        if not self.model:
            logging.error("Model is not initialized. Cannot send message.")
            return None

        if not user_message or not user_message.strip():
            logging.warning("Empty message provided. Not sending to API.")
            return None

        try:
            logging.info(f"Sending message to Gemini: '{user_message[:70]}...'")
            response = self.model.generate_content(user_message)

            # The response object might not have a 'text' attribute if generation fails
            # (e.g., due to safety settings). The SDK handles this by raising an exception
            # or by providing a prompt_feedback attribute. A simple check for text is good.

            response_text = response.text if hasattr(response, 'text') else None

            if not response_text:
                logging.warning("Received an empty response from Gemini.")
                logging.debug(f"Full response object: {response}")
                return None

            logging.info("Response received successfully.")
            return response_text

        except ResourceExhausted as e:
            logging.error(f"Gemini API quota exceeded: {e}")
            return "I'm sorry, but I've reached my usage limit for now. Please try again later or contact support if this persists."
        except Exception as e:
            logging.error(f"An error occurred while calling the Gemini API: {e}")
            logging.error(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            return None


# Create a single, reusable instance of the service
gemini_service = GeminiService()

# For backward compatibility or direct invocation, you can keep a function wrapper
def chat_with_gemini(user_message: str) -> str | None:
    """
    ユーザーメッセージをGemini APIに送信し、応答を返す関数。

    Args:
        user_message (str): ユーザーからのメッセージ

    Returns:
        str | None: Geminiからの応答テキスト、またはエラー時はNone
    """
    return gemini_service.chat(user_message)
