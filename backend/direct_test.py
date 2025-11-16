import sys
from pathlib import Path

# backend ディレクトリをパスに追加
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from services.gemini_service import chat_with_gemini

print("\n" + "="*50)
print("Direct test of gemini_service.py")
print("="*50 + "\n")

test_message = "こんにちは、元気ですか？"
print(f"Sending message: {test_message}\n")

response = chat_with_gemini(test_message)

print("\n" + "="*50)
if response:
    print("SUCCESS! Response received:")
    print(response)
else:
    print("FAILED: No response received")
print("="*50)