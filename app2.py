# app.py

import json

from llm import client, TOOLS

from tools import (
    get_incident_status,
    get_user_info,
    search_incidents,
    search_escalation_policy
)


# Map tool names to actual Python functions
AVAILABLE_FUNCTIONS = {
    "get_incident_status": get_incident_status,
    "get_user_info": get_user_info,
    "search_incidents": search_incidents,
    "search_escalation_policy": search_escalation_policy
}


def run_assistant(user_message):

    # --------------------------------
    # STEP 1: Send user message to LLM
    # --------------------------------

    response = client.responses.create(
        model="YOUR_MODEL_NAME",

        instructions="""
        You are an enterprise incident assistant.

        You can use tools to investigate incidents.

        If the user's question requires multiple pieces
        of information, use multiple tools as needed.

        Continue investigating until you have enough
        information to answer the user.

        Do not invent information.
        """,

        input=user_message,

        tools=TOOLS
    )


    # --------------------------------
    # STEP 2:
    # Agent loop
    # --------------------------------

    while True:

        tool_outputs = []


        # --------------------------------
        # STEP 3:
        # Check whether LLM requested
        # any tools
        # --------------------------------

        for item in response.output:

            if item.type == "function_call":

                tool_name = item.name

                arguments = json.loads(
                    item.arguments
                )


                print("\n==============================")
                print("Agent decided to use tool:")
                print(tool_name)

                print("\nArguments:")
                print(arguments)


                # --------------------------------
                # STEP 4:
                # Find actual Python function
                # --------------------------------

                function_to_call = AVAILABLE_FUNCTIONS.get(
                    tool_name
                )


                if not function_to_call:

                    raise ValueError(
                        f"Unknown tool: {tool_name}"
                    )


                # --------------------------------
                # STEP 5:
                # Execute the tool
                # --------------------------------

                result = function_to_call(
                    **arguments
                )


                print("\nTool result:")
                print(result)


                # --------------------------------
                # STEP 6:
                # Prepare tool result
                # for the LLM
                # --------------------------------

                tool_outputs.append({

                    "type": "function_call_output",

                    "call_id": item.call_id,

                    "output": json.dumps(result)

                })


        # --------------------------------
        # STEP 7:
        # If no tool was requested,
        # agent is finished
        # --------------------------------

        if not tool_outputs:

            return response.output_text


        # --------------------------------
        # STEP 8:
        # Send tool results back to LLM
        # --------------------------------

        response = client.responses.create(

            model="YOUR_MODEL_NAME",

            instructions="""
            You are an enterprise incident assistant.

            Analyze the tool results carefully.

            If you need additional information,
            call another tool.

            If you have enough information,
            provide the final answer.

            Do not invent information.
            """,

            input=[
                *response.output,
                *tool_outputs
            ],

            tools=TOOLS
        )


# ========================================
# APPLICATION ENTRY POINT
# ========================================

if __name__ == "__main__":

    print("\n====================================")
    print("Enterprise Incident AI Assistant")
    print("====================================")

    user_message = input(
        "\nAsk something: "
    )


    answer = run_assistant(
        user_message
    )


    print("\n====================================")
    print("AI Assistant:")
    print("====================================")

    print(answer)