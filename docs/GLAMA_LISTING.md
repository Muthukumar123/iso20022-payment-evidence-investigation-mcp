# Glama MCP server listing — maintainer-approved copy

**Status:** The GitHub repository is public and was renamed to `iso20022-payment-evidence-investigation-mcp` on 15 November 2026. Glama previously indexed the repository under its former name, `iso20022-mcp`. The requested display name and updated URL are **not confirmed live** on Glama; the maintainer must review the existing listing and save the updates.

## Listing fields

| Field | Recommended value |
| --- | --- |
| Display name | **ISO 20022 Payment Evidence & Investigation MCP** |
| Short name | Payment Evidence MCP |
| GitHub repository | https://github.com/Muthukumar123/iso20022-payment-evidence-investigation-mcp |
| Categories | Finance; Payments & Billing |
| Implementation | Python MCP server (local stdio) |
| License | MIT |

**Short description — paste into Glama:**

> Read-only MCP tools for ISO 20022 payment validation and evidence-backed rejection investigation. Correlates pacs.008 with pacs.002, explains bank-reported rejection codes with source evidence, and helps AI agents avoid unsupported payment conclusions.

**Expanded description:**

> ISO 20022 Payment Evidence & Investigation MCP is a Python Model Context Protocol server that gives AI clients deterministic tools to parse, validate, explain and investigate financial payment messages. The `investigate_payment` tool correlates original pacs.008 payments with pacs.002 status reports by original message and transaction identifiers, returns field-level provenance, retains unknown rejection codes as unknown, and recommends human review without performing payment mutations. The six existing tools are `parse_message`, `validate_message`, `explain_message`, `lookup_code`, `generate_test_message` and `investigate_payment`. The current implementation accepts supplied XML over local stdio. Remote banking connections, enterprise MCP gateway and live account-status verification are **not implemented**.

## Maintainer steps to change the Glama listing

1. Sign in at https://glama.ai with the GitHub account `Muthukumar123`.
2. Search Glama for both `iso20022-mcp` (previous repository name) and `iso20022-payment-evidence-investigation-mcp` (new name). Open the listing associated with GitHub user `Muthukumar123`; avoid creating a duplicate.
3. Choose **Claim ownership**, if necessary, and use GitHub verification. The root `glama.json` already specifies `Muthukumar123` as a maintainer.
4. Open the listing's **Manage/Edit** settings, update its GitHub repository URL to the new URL above (if editable), and paste the display name and description above.
5. Save, then open the listing as a signed-out visitor to verify its public title, tool count, and repository URL. If ownership or edit controls are unavailable, contact Glama support rather than creating an unverified duplicate.

Glama's current published `https://glama.ai/mcp/schemas/server.json` schema defines the `maintainers` field; it does **not** formally define a display-name field. Therefore do **not** assume changing repository `glama.json` will rename the live listing.

This document is a copy source for human review, **not** proof of an applied Glama dashboard update. GitHub documentation changes do not establish a new Glama server or deployed Streamable HTTP endpoint.

## Scope and safety

This is **ISO 20022 payment analysis**, not an Open Banking account-connectivity API. It provides read-only local XML tools, not live bank integration. No real payment/customer data should be used with a public demo or third-party hosted MCP service without a formal privacy and security assessment.
