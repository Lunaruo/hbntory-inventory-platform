#!/usr/bin/env python3
"""
Test client for the Product MCP Server (HTTP mode).
Run this while server.py is running on http://127.0.0.1:8001
"""

import asyncio
from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:8001/mcp") as client:
        print("Connected to MCP server.\n")

        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        print("Calling list_products_tool...")
        result = await client.call_tool("list_products_tool", {})
        print(result)
        print()

        print("Calling get_product_details_tool for HB-LAP-1001...")
        result = await client.call_tool(
            "get_product_details_tool", {"product_id": "HB-LAP-1001"}
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())