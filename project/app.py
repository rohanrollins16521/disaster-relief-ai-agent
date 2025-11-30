from fastapi import FastAPI
from pydantic import BaseModel
from project.main_agent import run_agent

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/query")
def query(q: Query):
    resp = run_agent(q.text)
    return {"response": resp}
