# mcp_client.py

import asyncio

from mcp.client import Client

from mcp_server import mcp


async def main():

    async with Client(mcp) as client:

        # --------------------------------
        # Discover available tools
        # --------------------------------

        tools = await client.list_tools()

        print("\nAvailable MCP tools:\n")

        for tool in tools.tools:

            print(
                f"- {tool.name}: {tool.description}"
            )


        # --------------------------------
        # Call get_incident_status
        # --------------------------------

        result = await client.call_tool(
            "get_incident_status",
            {
                "incident_id": "INC101"
            }
        )

        print("\nIncident result:")

        # result.content is a list of content blocks
        for block in result.content:
            print(block.text if hasattr(block, "text") else block)


if __name__ == "__main__":

    asyncio.run(main())
