from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from swarm import aura_swarm
from langchain_core.messages import HumanMessage

app = FastAPI(
    title="Aura API", 
    description="Autonomous Unified Risk & Audit System Gateway", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CloudEvent(BaseModel):
    event_type: str
    resource_id: str
    timestamp: str
    custom_state: Optional[dict] = None

@app.get("/")
def read_root():
    return {
        "status": "Aura API is running", 
        "description": "Ready to process cloud webhooks."
    }

@app.post("/webhook/aws")
async def handle_aws_event(event: CloudEvent):
    """
    Simulates a webhook from AWS EventBridge when infrastructure changes.
    This triggers the LangGraph Swarm.
    """
    
    # Initialize the state for the LangGraph Swarm
    initial_state = {
        "messages": [HumanMessage(content=f"Triggered by event {event.event_type} on {event.resource_id}")],
        "resource_id": event.resource_id,
        # Pass the custom state if provided by the UI, otherwise empty
        "resource_state": event.custom_state if event.custom_state else {},
        "applicable_policies": [],
        "compliance_passed": True,
        "remediation_code": "",
        "jira_ticket_id": ""
    }
    
    # Run the swarm
    final_state = aura_swarm.invoke(initial_state)
    
    # Return the thought process to the frontend
    agent_logs = [msg.content for msg in final_state["messages"]]
    
    return {
        "status": "Audit Complete",
        "resource_id": final_state["resource_id"],
        "compliance_passed": final_state["compliance_passed"],
        "remediation_code": final_state.get("remediation_code"),
        "ticket_created": final_state.get("jira_ticket_id"),
        "agent_logs": agent_logs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)