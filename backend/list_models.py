import google.generativeai as genai
from config import Config

# Configure the API
genai.configure(api_key=Config.GEMINI_API_KEY)

print("\n" + "="*60)
print("Available Gemini Models:")
print("="*60 + "\n")

try:
    # List all available models
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print("-" * 60)
except Exception as e:
    print(f"Error listing models: {e}")

print("\n" + "="*60)