import os
from pathlib import Path
from dotenv import load_dotenv

# config.py がある場所を基準に .env ファイルを探す
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Gemini API 設定
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GENERATIVE_MODEL = os.getenv("GENERATIVE_MODEL", "gemini-2.0-flash")

    # Firebase 関連設定
    FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
