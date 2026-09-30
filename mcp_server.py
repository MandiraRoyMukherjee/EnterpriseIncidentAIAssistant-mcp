# mcp_server.py

from mcp.server.mcpserver import MCPServer


mcp = MCPServer("Incident Server")


# ---------------------------------------
# Tool 1: Get incident status
# ---------------------------------------

@mcp.tool()
def get_incident_status(incident_id: str) -> dict:
    """
    Get the current status and details of an incident.
    """

    incidents = {
        "INC101": {
            "id": "INC101",
            "title": "CERT login issue",
            "status": "In Progress",
            "priority": "High",
            "owner": "Mandira"
        },
        "INC102": {
            "id": "INC102",
            "title": "Database connection issue",
            "status": "Resolved",
            "priority": "Medium",
            "owner": "Rahul"
        }
    }

    incident = incidents.get(incident_id)

    if not incident:
        return {
            "error": "Incident not found"
        }

    return incident


# ---------------------------------------
# Tool 2: Get user information
# ---------------------------------------

@mcp.tool()
def get_user_info(user_id: str) -> dict:
    """
    Get information about a user.
    """

    users = {
        "U101": {
            "id": "U101",
            "name": "Mandira",
            "role": "Developer",
            "team": "CERT"
        },
        "U102": {
            "id": "U102",
            "name": "Rahul",
            "role": "Developer",
            "team": "FLRT"
        }
    }

    user = users.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }

    return user


# ---------------------------------------
# Tool 3: Search incidents
# ---------------------------------------

@mcp.tool()
def search_incidents(keyword: str) -> list:
    """
    Search incidents using a keyword.
    """

    incidents = [
        {
            "id": "INC101",
            "title": "CERT login issue",
            "status": "In Progress",
            "priority": "High"
        },
        {
            "id": "INC102",
            "title": "Database connection issue",
            "status": "Resolved",
            "priority": "Medium"
        },
        {
            "id": "INC103",
            "title": "CERT notification issue",
            "status": "Open",
            "priority": "High"
        }
    ]

    keyword = keyword.lower()

    return [
        incident
        for incident in incidents
        if keyword in incident["title"].lower()
    ]
    
@mcp.tool()
def search_escalation_policy_tool(keyword: str) -> list:
    """
    Search incident escalation policies by keyword.
    """

    policies = [
        {
            "keyword": "high priority",
            "policy": "High priority incidents should be escalated to the incident manager."
        },
        {
            "keyword": "database",
            "policy": "Database incidents should be assigned to the database support team."
        },
        {
            "keyword": "security",
            "policy": "Security-related incidents must be escalated to the security team."
        }
    ]

    kw = keyword.lower()

    return [
        p for p in policies
        if kw in p["keyword"].lower()
    ]

# ---------------------------------------
# Start MCP server
# ---------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")