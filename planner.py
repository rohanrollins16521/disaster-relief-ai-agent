from typing import Dict, Any
import uuid
from project.core.a2a_protocol import make_envelope

class Planner:
    def __init__(self):
        pass

    def create_plan(self, user_input: str, session_id: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Parse user input and produce a plan JSON.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        # naive parsing (placeholder)
        disaster_type = "unknown"
        urgency = "normal"
        if "flood" in user_input.lower():
            disaster_type = "flood"
        if "help" in user_input.lower() or "now" in user_input.lower():
            urgency = "immediate"
        plan = {
            "plan_id": str(uuid.uuid4()),
            "session_id": session_id,
            "disaster_type": disaster_type,
            "urgency": urgency,
            "location": metadata.get("location") if metadata else None,
            "language": metadata.get("language") if metadata else "en",
            "required_outputs": ["actions", "routes", "shelters", "contacts"],
            "constraints": {"no_medical_advice": True, "require_citations": True}
        }
        envelope = make_envelope(sender="planner", recipient="worker", type_="PLAN", payload=plan, session_id=session_id)
        return envelope
