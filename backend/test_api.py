import requests
import json

url = "http://localhost:5000/api/chat/message"
payload = {"message": "こんにちは、Geminiさん！"}
headers = {"Content-Type": "application/json"}

print("Sending request to Gemini API...")
response = requests.post(url, json=payload, headers=headers)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")