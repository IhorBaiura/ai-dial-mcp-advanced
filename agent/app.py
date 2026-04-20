import asyncio
import json
import os
from typing import Any

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role

DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv('DIAL_API_KEY', '')
MCP_SERVER_URLS = [
    "http://localhost:8006/mcp",
    "https://remote.mcpservers.org/fetch/mcp"
]

async def main():
    tools: list[dict[str, Any]] = []
    tool_name_client_map: dict[str, MCPClient | CustomMCPClient] = {}

    for url in MCP_SERVER_URLS:
        try:
            client = await MCPClient.create(url)
            client_tools = await client.get_tools()
            print(f"{json.dumps(client_tools, indent=2)}")
            tools.extend(client_tools)
            for tool in client_tools:
                tool_name = tool["function"]["name"]
                tool_name_client_map[tool_name] = client
        except Exception as e:
            print(f"Failed to connect to MCP server at {url}: {e}")

    dial_client = DialClient(
        api_key=API_KEY,
        endpoint=DIAL_ENDPOINT,
        tools=tools,
        tool_name_client_map=tool_name_client_map
    )

    messages = [
        Message(
            role=Role.SYSTEM,
            content="You are an assistant that helps to handle user requests by calling appropriate tools."
        )
    ]

    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting chat.")
            break

        messages.append(Message(role=Role.USER, content=user_input))

        ai_response = await dial_client.get_completion(messages)
        print(f"AI: {ai_response.content}")
        messages.append(ai_response)

if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him