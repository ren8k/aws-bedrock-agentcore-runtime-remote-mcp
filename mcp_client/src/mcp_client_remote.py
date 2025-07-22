import asyncio
import os
import sys

from boto3.session import Session
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()


async def main():
    boto_session = Session()
    region = boto_session.region_name
    agent_arn = os.getenv("AGENT_ARN")
    bearer_token = os.getenv("COGNITO_ACCESS_TOKEN")

    encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
    mcp_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
    headers = {
        "authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    print(f"\nConnecting to: {mcp_url}")

    try:
        async with streamablehttp_client(
            mcp_url, headers, timeout=120, terminate_on_close=False
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


if __name__ == "__main__":
    asyncio.run(main())
