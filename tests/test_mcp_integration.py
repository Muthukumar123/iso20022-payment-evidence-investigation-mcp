"""Exercise MCP initialize, tools/list and tools/call through stdio."""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _exercise_mcp():
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "iso20022_mcp.server"]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            names = {tool.name for tool in listed.tools}
            assert {
                "parse_message", "validate_message", "explain_message",
                "lookup_code", "generate_test_message",
            }.issubset(names)
            result = await session.call_tool("lookup_code", {"code": "AC04"})
            assert not result.is_error
            assert result.content


def test_stdio_tool_discovery_and_invocation():
    asyncio.run(_exercise_mcp())
