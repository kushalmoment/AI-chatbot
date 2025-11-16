from waitress import serve
from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server with Waitress on port {port}...")
    print(f"--- [INFO] Serving on http://0.0.0.0:{port} ---")
    serve(app, host='0.0.0.0', port=port)
