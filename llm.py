import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_incident_status",
            "description": "Get the status and details of an incident",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string",
                        "description": "Incident ID such as INC101"
                    }
                },
                "required": ["incident_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_info",
            "description": "Get information about a user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID such as U101"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_incidents",
            "description": "Search incidents using a keyword",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_escalation_policy",
            "description": "Search the incident escalation policy using a keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword such as high priority, database, or security"
                    }
                },
                "required": ["keyword"]
            }
        }
    }
]

def convert_mcp_tools_to_llm_tools(mcp_tools):

    tools = []

    for tool in mcp_tools:

        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema
            }
        })

    return tools
