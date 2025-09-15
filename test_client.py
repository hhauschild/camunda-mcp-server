#!/usr/bin/env python3
"""
Test client for Camunda MCP Server
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the Camunda MCP server by listing available tools."""
    
    # Server parameters
    server_params = StdioServerParameters(
        command="C:/Users/hhaus/AppData/Local/Programs/Python/Python312/python.exe",
        args=["-m", "src.server"],
        cwd="C:\\code\\pythia\\camunda_mcp_server"
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                print("Initializing connection...")
                await session.initialize()
                
                # List available tools
                print("Listing available tools...")
                tools_result = await session.list_tools()
                
                print(f"\nFound {len(tools_result.tools)} tools:")
                for tool in tools_result.tools:
                    print(f"- {tool.name}: {tool.description}")
                
                # Try to call a simple tool (health check style)
                print("\nTesting list_tasks tool...")
                try:
                    result = await session.call_tool("list_tasks", {})
                    content = result.content[0] if result.content else None
                    if content and hasattr(content, 'text'):
                        print(f"Result: {content.text}")
                    else:
                        print("No text content in result")
                except Exception as e:
                    print(f"Tool call failed (expected if no Camunda server): {e}")
                
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_server())