from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from graphrag.neo4j_client import neo4j_client

class AuditState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    resource_id: str
    resource_type: str
    resource_state: dict
    applicable_policies: list
    compliance_passed: bool
    remediation_code: str
    jira_ticket_id: str

MOCK_AWS_STATE = {
    "user-data-bucket": {"type": "S3", "encrypted": False, "public_access": True},
    "finance-db": {"type": "RDS", "encrypted": True, "public_access": False}
}

def investigator_agent(state: AuditState):
    resource_id = state.get("resource_id")
    
    # Check if the user sent a custom state from the UI via the webhook
    custom_state = state.get("resource_state", {})
    if custom_state and len(custom_state) > 0:
        resource_state = custom_state
    else:
        # Fallback to the mock data
        resource_state = MOCK_AWS_STATE.get(resource_id, {"type": "Unknown", "encrypted": False, "public_access": True})
    
    return {
        "messages": [AIMessage(content=f"Investigated {resource_id} via MCP Gateway. Current State: {resource_state}")],
        "resource_state": resource_state,
        "resource_type": resource_state.get("type")
    }

def compliance_agent(state: AuditState):
    resource_id = state.get("resource_id")
    resource_state = state.get("resource_state")
    
    neo4j_policies = neo4j_client.get_policies_for_resource(resource_id)
    
    if not neo4j_policies:
        return {
            "messages": [AIMessage(content="No governance policies found for this resource in the Knowledge Graph. Passed by default.")],
            "applicable_policies": [],
            "compliance_passed": True
        }
    
    policy_texts = [f"{p['policy_id']}: {p['description']}" for p in neo4j_policies]
    
    is_compliant = True
    violation_msg = ""
    
    if resource_state.get("encrypted") is False:
        is_compliant = False
        violation_msg += "Resource is not encrypted at rest. "
    if resource_state.get("public_access") is True:
        is_compliant = False
        violation_msg += "Resource has public access enabled. "
        
    if is_compliant:
        msg = f"Compliance Check Passed against policies: {', '.join([p['policy_id'] for p in neo4j_policies])}."
    else:
        msg = f"Compliance Violation Detected against {', '.join([p['policy_id'] for p in neo4j_policies])}. Issues: {violation_msg}"
    
    return {
        "messages": [AIMessage(content=msg)],
        "applicable_policies": policy_texts,
        "compliance_passed": is_compliant
    }

def route_after_compliance(state: AuditState):
    if state.get("compliance_passed"):
        return END
    return "remediation_agent"

def remediation_agent(state: AuditState):
    resource_type = state.get("resource_type")
    resource_id = state.get("resource_id")
    
    if resource_type == "S3":
        terraform_fix = f"""resource "aws_s3_bucket" "fixed_{resource_id}" {{
  bucket = "{resource_id}"
}}

resource "aws_s3_bucket_server_side_encryption_configuration" "fix" {{
  bucket = aws_s3_bucket.fixed_{resource_id}.id
  rule {{
    apply_server_side_encryption_by_default {{
      sse_algorithm = "AES256"
    }}
  }}
}}

resource "aws_s3_bucket_public_access_block" "fix" {{
  bucket = aws_s3_bucket.fixed_{resource_id}.id
  block_public_acls       = true
  block_public_policy     = true
}}"""
    elif resource_type == "RDS":
        terraform_fix = f"""resource "aws_db_instance" "fixed_{resource_id}" {{
  identifier          = "{resource_id}"
  storage_encrypted   = true
  publicly_accessible = false
}}"""
    else:
        terraform_fix = "# Manual intervention required for unknown resource type."

    return {
        "messages": [AIMessage(content=f"Generated Terraform remediation script for {resource_type} violation.")],
        "remediation_code": terraform_fix
    }

def reporter_agent(state: AuditState):
    ticket_id = f"AURA-SEC-{hash(state['resource_id']) % 10000}"
    return {
        "messages": [AIMessage(content=f"Created Jira Ticket {ticket_id} with remediation instructions.")],
        "jira_ticket_id": ticket_id
    }

workflow = StateGraph(AuditState)
workflow.add_node("investigator_agent", investigator_agent)
workflow.add_node("compliance_agent", compliance_agent)
workflow.add_node("remediation_agent", remediation_agent)
workflow.add_node("reporter_agent", reporter_agent)

workflow.set_entry_point("investigator_agent")
workflow.add_edge("investigator_agent", "compliance_agent")
workflow.add_conditional_edges("compliance_agent", route_after_compliance)
workflow.add_edge("remediation_agent", "reporter_agent")
workflow.add_edge("reporter_agent", END)

aura_swarm = workflow.compile()
