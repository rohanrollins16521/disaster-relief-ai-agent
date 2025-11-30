from typing import Dict, Any

PLANNER_PROMPT = """You are Planner. Create a structured plan for the Worker."""

WORKER_PROMPT = """You are Worker. Use tools and retrieved documents to assemble a candidate response."""

EVALUATOR_PROMPT = """You are Evaluator. Validate candidate response, check citations and safety."""
