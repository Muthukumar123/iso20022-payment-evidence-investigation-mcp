# iso20022-mcp

An MCP server that lets AI agents **parse, validate, explain and test ISO 20022 payment messages** — safely.

Agents handling payments fail in predictable ways: they invent reject codes, miss IBAN checksum errors, and
follow instructions hidden in free-text fields like remittance information. This server gives them
deterministic tools for the parts that must be exact, and treats message free text as untrusted data.

## Tools

| Tool | What it does |
|---|---|
| `parse_message` | pacs.008 / pacs.002 XML → structured JSON (namespace-agnostic, XXE-safe) |
| `validate_message` | IBAN mod-97, BIC format, amounts and currency decimals, required parties, counts, free-text limits, prompt-injection patterns — each issue mapped to its likely reject code |
| `explain_message` | Deterministic plain-language summary: who pays whom, how much, status and reasons |
| `lookup_code` | Status reason / transaction status / charge bearer codes — returns `found: false` instead of guessing |
| `generate_test_message` | Synthetic valid and defective messages for testing (no real customer data) |

## Quick start

```bash
pip install -e ".[dev]"
pytest -q
iso20022-mcp            # runs the server over stdio
```

Claude Desktop / any MCP client config:

```json
{ "mcpServers": { "iso20022": { "command": "iso20022-mcp" } } }
```

## Security design

- Free-text fields are returned with an `_UNTRUSTED` suffix and the server instructions tell agents to treat them as data.
- `validate_message` flags instruction-like content in free text (severity `security`).
- XML parsing disables entity resolution and network access.
- Only synthetic data and public example IBANs/BICs are used anywhere in this repo.

## Benchmark

`evals/` contains a generator for a banking-agent task set (`python evals/make_tasks.py`) covering validation, rejection investigation and prompt injection, plus a
deterministic scorer. Results across model families: _coming soon_.

## Roadmap

- Official XSD validation · pain.001 and camt.053 · MT103 → pacs.008 (subset) · remote HTTP deployment with auth and OpenTelemetry

## Disclaimer

Not affiliated with ISO, SWIFT or any bank. Code sets here are a curated subset; consult the official ISO 20022 external code sets for production use.
