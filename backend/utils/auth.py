from flask import request, jsonify, g
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth as fb_auth
from config import Config
from utils.logger import logger

def init_auth(app):
    cred_path = Config.FIREBASE_CRED_PATH
    if not cred_path:
        logger.error("FIREBASE_CRED_PATH is not set.")
        raise RuntimeError("FIREBASE_CRED_PATH が設定されていません。")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    logger.info("Firebase Auth initialized with credential: %s", cred_path)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"error": "Unauthorized"}), 401
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error": "Invalid header"}), 401
        id_token = parts[1]
        try:
            decoded = fb_auth.verify_id_token(id_token)
            g.user_id = decoded.get("uid")
        except Exception as e:
            logger.error("Failed to verify Firebase ID token: %s", e)
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper
