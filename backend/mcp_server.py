import os
from mcp.server import Server
import mcp.server.stdio
from mcp.types import Tool

# Initialize the MCP Server
app = Server("aura-gateway")

# Mock Enterprise Data
MOCK_AWS_STATE = {
    "user-data-bucket": {"type": "S3", "encrypted": False, "public_access": True},
    "finance-db": {"type": "RDS", "encrypted": True, "public_access": False}
}

MOCK_JIRA_TICKETS = []

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Expose the tools available to the AI Swarm via the MCP protocol.
    This acts as a strict boundary - the AI cannot do anything not listed here.
    """
    return [
        Tool(
            name="get_aws_resource_status",
            description="Fetches the current configuration state of an AWS resource.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_id": {"type": "string", "description": "The ID of the AWS resource (e.g. 'user-data-bucket')"}
                },
                "required": ["resource_id"]
            }
        ),
        Tool(
            name="create_jira_ticket",
            description="Creates a Jira ticket for compliance remediation tracking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the Jira ticket"},
                    "description": {"type": "string", "description": "Detailed remediation instructions"}
                },
                "required": ["title", "description"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """
    Handle the execution of the tools requested by the AI.
    """
    if name == "get_aws_resource_status":
        resource_id = arguments.get("resource_id")
        if resource_id in MOCK_AWS_STATE:
            # In a real app, this would use boto3 to hit AWS API securely
            return [{"type": "text", "text": str(MOCK_AWS_STATE[resource_id])}]
        return [{"type": "text", "text": "Resource not found"}]
        
    elif name == "create_jira_ticket":
        # In a real app, this hits Jira's REST API
        ticket = {
            "id": f"AURA-{len(MOCK_JIRA_TICKETS) + 1}",
            "title": arguments.get("title"),
            "description": arguments.get("description"),
            "status": "OPEN"
        }
        MOCK_JIRA_TICKETS.append(ticket)
        return [{"type": "text", "text": f"Ticket created successfully: {ticket['id']}"}]
        
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    # Run the MCP server over stdio (standard protocol for local agent communication)
    asyncio.run(mcp.server.stdio.stdio_server(app))
