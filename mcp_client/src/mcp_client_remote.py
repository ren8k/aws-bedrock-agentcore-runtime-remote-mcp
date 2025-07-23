import asyncio
import os
import sys

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def get_mcp_endpoint(agent_arn: str, region: str = "us-west-2") -> str:
    encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
    return f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"


async def connect_to_server(mcp_endpoint: str, headers: dict) -> None:
    try:
        async with streamablehttp_client(
            mcp_endpoint, headers, timeout=120, terminate_on_close=False
        ) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                print("\n🔄 Initializing MCP session...")
                await session.initialize()
                print("✓ MCP session initialized")

                print("\n🔄 Listing available tools...")
                tool_result = await session.list_tools()

                print("\n📋 Available MCP Tools:")
                print("=" * 50)
                for tool in tool_result.tools:
                    print(f"🔧 {tool.name}")
                    print(f"   Description: {tool.description}")
                    if hasattr(tool, "inputSchema") and tool.inputSchema:
                        properties = tool.inputSchema.get("properties", {})
                        if properties:
                            print(f"   Parameters: {list(properties.keys())}")
                    print()

                print("✅ Successfully connected to MCP server!")
                print(f"Found {len(tool_result.tools)} tools available.")

    except Exception as e:
        print(f"❌ Error connecting to MCP server: {e}")
        sys.exit(1)


async def main():
    load_dotenv()
    agent_arn = os.getenv("AGENT_ARN")
    bearer_token = os.getenv("COGNITO_ACCESS_TOKEN")
    if not (agent_arn and bearer_token):
        raise ValueError(
            "Required environment variables AGENT_ARN and COGNITO_ACCESS_TOKEN are not set."
        )

    mcp_endpoint = get_mcp_endpoint(agent_arn)
    headers = {
        "authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    print(f"\nConnect to: {mcp_endpoint}")
    await connect_to_server(mcp_endpoint, headers)


if __name__ == "__main__":
    asyncio.run(main())
