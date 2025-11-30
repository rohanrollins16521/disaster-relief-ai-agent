from typing import Dict, Any
from project.core.a2a_protocol import make_envelope

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate candidate response package and produce final response.
        """
        candidate = envelope["payload"]
        issues = []
        # Simple checks
        if not candidate.get("citations"):
            issues.append("no_citations")
        if "hallucination" in candidate.get("response_text", "").lower():
            issues.append("possible_hallucination")
        confidence = candidate.get("worker_confidence", 0.0)
        if issues:
            confidence = min(confidence, 0.5)
        final = {
            "plan_id": candidate.get("plan_id"),
            "final_text": candidate.get("response_text") + "\n\n-- This response is auto-generated. If you're in immediate danger, call local emergency services.",
            "structured_payload": candidate,
            "confidence_score": confidence,
            "reason_codes": issues,
            "escalation": confidence < 0.4
        }
        out_env = make_envelope(sender="evaluator", recipient="planner", type_="FINAL_RESPONSE", payload=final, session_id=candidate.get("plan_id"))
        return out_env
