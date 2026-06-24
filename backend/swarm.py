from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

# Define the Swarm's State
class AuditState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    resource_id: str
    resource_state: dict
    applicable_policies: list
    compliance_passed: bool
    remediation_code: str
    jira_ticket_id: str

# Node 1: The Investigator (Queries MCP for Infra State)
def investigator_agent(state: AuditState):
    resource_id = state.get("resource_id")
    # Simulation of AI calling the MCP Tool 'get_aws_resource_status'
    # In full implementation, we wrap this via mcp-client
    mock_state = {"type": "S3", "encrypted": False, "public_access": True}
    
    return {
        "messages": [AIMessage(content=f"Investigated {resource_id}. State: {mock_state}")],
        "resource_state": mock_state
    }

# Node 2: The Compliance Officer (Queries GraphRAG)
def compliance_agent(state: AuditState):
    # Simulation of querying Neo4j + pgvector
    # Real code would use the neo4j_client and pgvector_client we wrote
    policies = ["SOC2: All PII S3 buckets must be encrypted (encryption=True) and private (public_access=False)."]
    
    is_compliant = state["resource_state"].get("encrypted") is True and state["resource_state"].get("public_access") is False
    
    msg = "Compliance Check Passed." if is_compliant else f"Compliance Violation Detected against: {policies[0]}"
    
    return {
        "messages": [AIMessage(content=msg)],
        "applicable_policies": policies,
        "compliance_passed": is_compliant
    }

# Conditional Router
def route_after_compliance(state: AuditState):
    if state.get("compliance_passed"):
        return END
    return "remediation_agent"

# Node 3: The Remediation Engineer (Drafts Fix)
def remediation_agent(state: AuditState):
    # AI drafts the fix
    terraform_fix = f"""
resource "aws_s3_bucket" "fixed_{state['resource_id']}" {{
  bucket = "{state['resource_id']}"
}}
resource "aws_s3_bucket_server_side_encryption_configuration" "fix" {{
  bucket = aws_s3_bucket.fixed_{state['resource_id']}.id
  rule {{
    apply_server_side_encryption_by_default {{
      sse_algorithm = "AES256"
    }}
  }}
}}
resource "aws_s3_bucket_public_access_block" "fix" {{
  bucket = aws_s3_bucket.fixed_{state['resource_id']}.id
  block_public_acls       = true
  block_public_policy     = true
}}
"""
    return {
        "messages": [AIMessage(content="Generated Terraform remediation script.")],
        "remediation_code": terraform_fix
    }

# Node 4: The Reporter (Uses MCP to create Jira Ticket)
def reporter_agent(state: AuditState):
    # Simulation of AI calling the MCP Tool 'create_jira_ticket'
    ticket_id = "AURA-1"
    
    return {
        "messages": [AIMessage(content=f"Created Jira Ticket {ticket_id} with remediation instructions.")],
        "jira_ticket_id": ticket_id
    }

# Build the LangGraph Swarm
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
