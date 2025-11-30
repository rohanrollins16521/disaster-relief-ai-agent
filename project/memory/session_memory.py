from typing import Dict, Any
import time

class SessionMemory:
    def __init__(self):
        self.store = {}

    def get(self, session_id: str) -> Dict[str, Any]:
        return self.store.get(session_id, {})

    def put(self, session_id: str, key: str, value: Any, ttl: int = 3600):
        entry = {"value": value, "expires_at": time.time() + ttl}
        self.store.setdefault(session_id, {})[key] = entry

    def cleanup(self):
        now = time.time()
        for sid in list(self.store.keys()):
            for k, v in list(self.store[sid].items()):
                if v.get("expires_at", 0) < now:
                    del self.store[sid][k]
            if not self.store[sid]:
                del self.store[sid]
