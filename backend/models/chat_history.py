_history_store = {}

def get_history_for_user(user_id: str):
    return _history_store.get(user_id, [])

def append_user_message(user_id: str, role: str, content: str):
    if user_id not in _history_store:
        _history_store[user_id] = []
    _history_store[user_id].append({'role': role, 'content': content})
