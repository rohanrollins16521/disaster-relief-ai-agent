from typing import Dict, Any
import time
import uuid

def make_envelope(sender: str, recipient: str, type_: str, payload: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
    if session_id is None:
        session_id = str(uuid.uuid4())
    return {
        "message_id": str(uuid.uuid4()),
        "session_id": session_id,
        "sender": sender,
        "recipient": recipient,
        "type": type_,
        "payload": payload,
        "meta": {
            "timestamp": time.time()
        }
    }
