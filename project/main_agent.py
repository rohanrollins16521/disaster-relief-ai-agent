from typing import Dict, Any
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import SessionMemory
from project.core.observability import log_event

class MainAgent:
    def __init__(self):
        self.planner = Planner()
        self.worker = Worker()
        self.evaluator = Evaluator()
        self.memory = SessionMemory()

    def handle_message(self, user_input: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        # Planner creates plan envelope
        plan_env = self.planner.create_plan(user_input, metadata=metadata or {})
        log_event({"event": "plan_created", "plan": plan_env})
        # Worker handles the plan
        candidate_env = self.worker.handle_plan(plan_env)
        log_event({"event": "worker_completed", "candidate": candidate_env})
        # Evaluator validates
        final_env = self.evaluator.evaluate(candidate_env)
        log_event({"event": "evaluator_completed", "final": final_env})
        # store session memory simple
        session_id = plan_env.get("session_id")
        if session_id:
            self.memory.put(session_id, "last_query", user_input)
        return {"response": final_env["payload"]["final_text"], "confidence": final_env["payload"]["confidence_score"]}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
