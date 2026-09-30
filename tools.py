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


def get_incident_status(incident_id: str):
    """Get incident information."""

    incident = incidents.get(incident_id)

    if not incident:
        return {
            "error": "Incident not found"
        }

    return incident


def get_user_info(user_id: str):
    """Get information about a user."""

    user = users.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }

    return user


def search_incidents(keyword: str):
    """Search incidents by keyword."""

    keyword = keyword.lower()

    results = [
        incident
        for incident in incidents.values()
        if keyword in incident["title"].lower()
    ]

    return results

def search_escalation_policy(keyword: str):
    """Search the incident escalation policy."""

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

    keyword = keyword.lower()

    results = [
        policy
        for policy in policies
        if keyword in policy["keyword"].lower()
    ]

    return results