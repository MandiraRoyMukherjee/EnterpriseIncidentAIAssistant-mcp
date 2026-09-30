# app.py

import asyncio
import json

from llm import client, MODEL, convert_mcp_tools_to_llm_tools

from mcp.client import Client
from mcp_server import mcp

SYSTEM_PROMPT = """
You are an enterprise incident assistant.
You have access to incident management tools through MCP.
Use the tools when necessary.
Continue using tools until you have enough information to answer the user's question.
Do not invent information.
"""


async def run_agent(user_message):

    # --------------------------------
    # STEP 1: Connect to MCP server
    # --------------------------------

    async with Client(mcp) as mcp_client:

        print("\nConnected to MCP server")

        # --------------------------------
        # STEP 2: Discover MCP tools
        # --------------------------------

        mcp_tool_result = await mcp_client.list_tools()
        mcp_tools = mcp_tool_result.tools

        print("\nMCP tools discovered:")
        for tool in mcp_tools:
            print(f"  - {tool.name}")

        # --------------------------------
        # STEP 3: Convert MCP tools to
        # LLM tool definitions
        # --------------------------------

        llm_tools = convert_mcp_tools_to_llm_tools(mcp_tools)

        # --------------------------------
        # STEP 4: Agent loop
        # --------------------------------

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ]

        while True:

            # Send messages to LLM
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=llm_tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # --------------------------------
            # STEP 5: No tool calls → done
            # --------------------------------

            if not tool_calls:
                return response_message.content

            # Append assistant turn to history
            messages.append(response_message)

            # --------------------------------
            # STEP 6: Execute each MCP tool
            # --------------------------------

            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"\nAgent selected MCP tool: {tool_name}")
                print(f"Arguments: {arguments}")

                # Call MCP server
                result = await mcp_client.call_tool(tool_name, arguments)

                # Extract text from content blocks
                tool_output = " ".join(
                    block.text for block in result.content
                    if hasattr(block, "text")
                )

                print(f"\nMCP result: {tool_output}")

                # --------------------------------
                # STEP 7: Append tool result
                # --------------------------------

                messages.append({
                    "role":         "tool",
                    "tool_call_id": tool_call.id,
                    "content":      tool_output
                })

            # Loop back — LLM will call another tool or give final answer


async def main():

    print("\n====================================")
    print("Enterprise Incident AI Assistant")
    print("====================================")

    user_message = input("\nAsk something: ")

    answer = await run_agent(user_message)

    print("\n====================================")
    print("AI Assistant:")
    print("====================================")
    print(answer)


if __name__ == "__main__":

    asyncio.run(main())
