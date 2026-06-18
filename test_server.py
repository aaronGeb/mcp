"""A simple test client for the MCP server."""

import asyncio

from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:3000/sse") as client:
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])

        result = await client.call_tool("add", {"a": 5, "b": 3})
        print("add(5,3):", result.content[0].text)

        result = await client.call_tool("get_current_time", {})
        print("time:", result.content[0].text)

        result = await client.call_tool("get_current_weather", {"city": "Addis Ababa"})
        print("weather:", result.content[0].text)


asyncio.run(main())
