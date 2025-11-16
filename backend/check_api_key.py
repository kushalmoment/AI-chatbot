from config import Config

print("="*60)
print("API Key Check")
print("="*60)

api_key = Config.GEMINI_API_KEY

print(f"\nAPI Key exists: {api_key is not None}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key type: {type(api_key)}")

if api_key:
    print(f"First 10 chars: {api_key[:10]}")
    print(f"Last 10 chars: {api_key[-10:]}")
    print(f"Contains quotes: {'"' in api_key or "'" in api_key}")
    print(f"Contains spaces: {' ' in api_key}")
    
    # Check for hidden characters
    print(f"\nAPI Key (repr): {repr(api_key)}")
else:
    print("\nERROR: API Key is None or empty!")

print("="*60)