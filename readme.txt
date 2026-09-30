What we're building

User
  ↓
Python application
  ↓
LLM
  ↓
LLM says: call get_incident_status
  ↓
Python executes get_incident_status()
  ↓
Tool result
  ↓
LLM
  ↓
Final natural-language answer

LLM
The LLM doesn't know your Python function automatically.

You have to tell the model:

These tools are available:

get_incident_status
get_user_info
search_incidents

And describe their parameters.

Available tools:

get_incident_status
    ↓
    incident_id: string

get_user_info
    ↓
    user_id: string

search_incidents
    ↓
    keyword: string

The model can then decide:

"For this question, I need get_incident_status."    

User
 │
 │ "Check INC101"
 ↓
LLM
 │
 │ tool call:
 │ get_incident_status("INC101")
 ↓
Python application
 │
 │ executes function
 ↓
get_incident_status()
 │
 │ result
 ↓
Python application
 │
 │ sends result back
 ↓
LLM
 │
 │ "INC101 is currently In Progress..."
 ↓
User

1. Tool definition
What tools are available?
2. Tool call
LLM → "Call get_incident_status with INC101"
3. Tool execution
Application → actually runs Python/API/DB operation

enterprise-ai-assistant/
│
├── app.py        # controls the complete tool-calling flow
├── llm.py        # talks to the LLM + defines tool schemas
├── tools.py      # actual Python business functions
├── .env
└── requirements.txt

How does function calling work?

Your answer should be approximately:

"The model decides that it needs external information and returns a structured tool call containing the tool name and arguments. The application receives that request, executes the corresponding function or API, sends the tool result back to the model, and the model generates the final response."
Normal tool calling:
User
 ↓
LLM
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Answer

Agent:
User
 ↓
Agent/LLM
 ↓
Think/decide
 ↓
Tool 1
 ↓
Observe result
 ↓
Decide again
 ↓
Tool 2
 ↓
Observe result
 ↓
Decide
 ↓
Final answer

1. get_incident_status("INC101")
             ↓
       High priority
             ↓
2. search policy("high priority escalation")
             ↓
       Policy says...
             ↓
3. Final answer

Tool calling

The model requests a tool.

Agent

The system can decide what tool to use, use it, inspect the result, and decide what to do next.

Now we want:

User
 ↓
LLM
 ↓
Tool 1
 ↓
Result
 ↓
LLM
 ↓
Tool 2
 ↓
Result
 ↓
LLM
 ↓
Final answer

After receiving Tool 1's result, the LLM gets another opportunity to decide what to do next.

That's the agent loop.

THIS is your Agent
                  USER
                    ↓
                   LLM
                    ↓
             ┌──── DECIDE ────┐
             ↓                 ↓
           TOOL 1              │
             ↓                 │
          RESULT                │
             ↓                 │
             └────→ LLM ←──────┘
                    ↓
                  DECIDE
                    ↓
                  TOOL 2
                    ↓
                  RESULT
                    ↓
                   LLM
                    ↓
               DECIDE AGAIN
                    ↓
              No more tools
                    ↓
              FINAL ANSWER

enterprise-ai-assistant/
│
├── app.py
├── llm.py
├── tools.py
│
├── mcp_server.py       ← NEW
├── mcp_client.py       ← later
│
├── .env
└── requirements.txt


AI Application
      ↓
MCP Client
      ↓
MCP Server
      ↓
Incident tools


nderstand @mcp.tool()

This is the most important line:

@mcp.tool()
def get_incident_status(incident_id: str) -> dict:

Before MCP, you had:

def get_incident_status(incident_id):

Now:

@mcp.tool()

means:

Expose this Python function as an MCP tool.

So MCP knows:

Tool name:
get_incident_status

Input:
incident_id → string

Description:
Get the current status and details of an incident.

Conceptually:

Python function
       ↓
@mcp.tool()
       ↓
MCP tool
       ↓
Available to MCP clients


This is the next important concept.

You currently have:

MCP Server
   ↓
Tools

But normally:

AI Application
      ↓
MCP Client
      ↓
MCP Server
      ↓
Tools

The current Python SDK also provides a Client for connecting to MCP servers. A client can connect over Streamable HTTP, launch a local server through stdio, or connect in-process for testing

The SDK's current client API uses list_tools() to discover tools and call_tool() to invoke them.

             MCP CLIENT
                  │
                  │ list_tools()
                  ↓
             MCP SERVER
                  │
                  ↓
              discovers
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
     Tool 1     Tool 2    Tool 3
        │         │         │
        ↓         ↓         ↓
    Incident    User     Search

    MCP Client
    │
    │ call_tool()
    ↓
MCP Server
    │
    ↓
get_incident_status()
    │
    ↓
Result
    │
    ↓
MCP Client


                         USER
                           ↓
                        React
                           ↓
                       FastAPI
                           ↓
                      Agent Loop
                           ↓
                           LLM
                           ↓
                     MCP Client
                           ↓
                    MCP Protocol
                           ↓
                  Incident MCP Server
                    /       |       \
                   ↓        ↓        ↓
             Incident API  User API  Search
                   │
                   ↓
                Database

                           Agent
                          /     \
                         ↓       ↓
                       RAG      MCP
                        ↓         ↓
                    Vector DB   APIs/DB


I built an enterprise incident assistant where the LLM acts as the reasoning component. For knowledge retrieval, I use RAG, while live operational capabilities are exposed through an MCP server. The agent uses an MCP client to discover and invoke tools such as incident status and user information. The MCP server acts as an AI-facing integration layer over existing enterprise APIs.

                 HOST
          (AI Application)
                  │
                  │
             MCP CLIENT
                  │
            MCP Protocol
                  │
             MCP SERVER
          ┌───────┼───────┐
          ↓       ↓       ↓
        TOOLS  RESOURCES PROMPTS



 Host

The application that wants to use MCP.

Examples:

your own AI application
an IDE
an AI desktop application
Client

The component that communicates with an MCP server.

Server

Exposes capabilities.

Tools

Do something.

create_ticket()
get_incident()
update_incident()

Resources

Provide/read information.

incident://INC101
Prompts

Reusable interaction templates.       

stdio              → local server
Streamable HTTP    → deployed/server-to-server use
SSE                → older transport

The flow is now:

USER
 │
 │ "Check INC101"
 ↓
LLM
 │
 │ "I need get_incident_status_tool"
 ↓
MCP CLIENT
 │
 │ call_tool()
 ↓
MCP SERVER
 │
 ↓
get_incident_status_tool()
 │
 ↓
tools.py
 │
 ↓
Incident data
 │
 ↓
MCP SERVER
 │
 ↓
MCP CLIENT
 │
 ↓
LLM
 │
 ↓
Final answer

Check INC101 and tell me whether it needs escalation.

                         USER
                           ↓
                          LLM
                           ↓
                get_incident_status
                           ↓
                      MCP Client
                           ↓
                      MCP Server
                           ↓
                     Incident API
                           ↓
                     High Priority
                           ↓
                          LLM
                           ↓
                Need escalation policy
                           ↓
                       MCP tool
                           ↓
                         Result
                           ↓
                          LLM
                           ↓
                     Final Answer

Your Part 1 was:

LLM
 ↓
AVAILABLE_FUNCTIONS
 ↓
Python function

Your Part 2 was:

LLM
 ↓
Agent loop
 ↓
AVAILABLE_FUNCTIONS
 ↓
Python function

Now:

LLM
 ↓
Agent
 ↓
MCP Client
 ↓
MCP Protocol
 ↓
MCP Server
 ↓
MCP Tool
 ↓
Business API / DB

"I built an incident-management MCP server exposing tools such as get_incident_status, get_user_info, and search_incidents. My AI application acts as the MCP host and uses an MCP client to discover the available tools through list_tools. The tool definitions are provided to the LLM, which decides when a tool is required. When the model returns a tool call, the application invokes the corresponding MCP tool through the MCP client. The MCP server executes the underlying business logic or, in a production system, would call an existing REST API or database. The result is returned to the LLM, and the agent can either call another tool or produce the final response."