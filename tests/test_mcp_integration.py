"""Verify the actual MCP stdio handshake and all six public tools.

This is the same protocol-level tool discovery a source registry such as Glama
performs; a static README count is not sufficient evidence of functionality.
"""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from iso20022_mcp import generate, parser


EXPECTED_TOOLS = {
    "parse_message",
    "validate_message",
    "explain_message",
    "lookup_code",
    "generate_test_message",
    "investigate_payment",
}


async def _exercise_mcp():
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "iso20022_mcp.server"]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            names = {tool.name for tool in listed.tools}
            assert len(listed.tools) == len(EXPECTED_TOOLS), (
                f"Expected exactly six public tools; saw: {sorted(names)}"
            )
            assert names == EXPECTED_TOOLS, (
                f"Missing: {sorted(EXPECTED_TOOLS - names)}; "
                f"Unexpected: {sorted(names - EXPECTED_TOOLS)}"
            )

            looked_up = await session.call_tool("lookup_code", {"code": "AC04"})
            assert not looked_up.is_error
            assert looked_up.content

            # Verify the sixth tool can actually be invoked over stdio MCP.
            payment_xml = generate.generate_pacs008()
            original = parser.parse_message(payment_xml)
            status_xml = generate.generate_pacs002(
                reason_code="AC04",
                original_msg_id=original["msg_id"],
                end_to_end_id=original["transactions"][0]["end_to_end_id"],
            )
            investigation = await session.call_tool(
                "investigate_payment",
                {"pacs008_xml": payment_xml, "pacs002_xml": status_xml},
            )
            assert not investigation.is_error
            assert investigation.content


def test_stdio_tool_discovery_and_invocation():
    asyncio.run(_exercise_mcp())
