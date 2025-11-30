from typing import Dict, Any
from project.core.a2a_protocol import make_envelope
from project.tools.tools import GeoTool, RoutingTool, DisasterAlertAPI, RAGRetriever, Summarizer

class Worker:
    def __init__(self):
        self.geo = GeoTool()
        self.routing = RoutingTool()
        self.alerts = DisasterAlertAPI()
        self.rag = RAGRetriever()
        self.summarizer = Summarizer()

    def handle_plan(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the plan: call tools, retrieve documents, generate candidate response package.
        """
        plan = envelope["payload"]
        location = plan.get("location")
        # Fetch alerts
        alerts = self.alerts.fetch_alerts(location)
        # Retrieve guidelines
        docs = self.rag.retrieve(plan.get("disaster_type"), region=location)
        summary = self.summarizer.summarize(docs)
        # Create simple candidate response
        candidate = {
            "plan_id": plan["plan_id"],
            "response_text": f"Detected disaster: {plan.get('disaster_type')} | Urgency: {plan.get('urgency')}. Summary: {summary[:300]}",
            "structured_steps": ["Step 1: Stay calm", "Step 2: Move to higher ground if flood"],
            "geojson_routes": None,
            "locations": [],
            "citations": [d.get("source") for d in docs],
            "worker_confidence": 0.8,
            "tool_logs": {"alerts_count": len(alerts)}
        }
        out_env = make_envelope(sender="worker", recipient="evaluator", type_="CANDIDATE_RESPONSE", payload=candidate, session_id=plan.get("session_id"))
        return out_env
