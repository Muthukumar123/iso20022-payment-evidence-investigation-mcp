#!/usr/bin/env python3
"""Publish ONLY reviewed, synthetic FEI executive content to Gamma AI.

Default is offline dry-run. This tool cannot upload arbitrary paths.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib import request, error

API = "https://public-api.gamma.app/v1.0"
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "finserv" / "GAMMA_EXECUTIVE_DECK.md"


def build_payload() -> dict:
    raw = SOURCE.read_bytes()
    if len(raw) > 70_000:
        raise ValueError("Reviewed Gamma source is too large.")
    narrative = raw.decode("utf-8")
    if narrative.count("\n---\n") != 10:
        raise ValueError("Expected exactly eleven Gamma cards.")
    return {
        "inputText": narrative,
        "textMode": "preserve",
        "format": "presentation",
        "numCards": 11,
        "cardSplit": "inputTextBreaks",
        "imageOptions": {"source": "noImages"},
        "cardOptions": {"dimensions": "16x9"},
        "sharingOptions": {
            "workspaceAccess": "noAccess",
            "externalAccess": "noAccess",
        },
        "additionalInstructions": (
            "Professional banking-architecture deck. Emphasize trust-boundary "
            "diagrams, use-case sequence, actual vs planned tools, guardrails. "
            "Never invent KPIs, production features, safety results or live banks."
        ),
        "exportAs": "pdf",
    }


def api_call(method: str, uri: str, token: str, payload: dict | None = None) -> dict:
    headers = {"X-API-KEY": token, "Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    try:
        with request.urlopen(
            request.Request(uri, headers=headers, data=data, method=method), timeout=30
        ) as response:
            result = json.load(response)
    except error.HTTPError as exc:
        raise RuntimeError(f"Gamma request failed (HTTP {exc.code}).") from None
    except (error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Gamma network failure ({type(exc).__name__}).") from None
    if not isinstance(result, dict):
        raise RuntimeError("Unexpected Gamma response.")
    return result


def publish() -> dict:
    token = os.environ.get("GAMMA_API_KEY")
    if not token:
        raise RuntimeError("GAMMA_API_KEY is missing; use a GitHub Actions secret.")
    created = api_call("POST", f"{API}/generations", token, build_payload())
    generation_id = created.get("generationId")
    if not isinstance(generation_id, str) or not generation_id:
        raise RuntimeError("Gamma did not return a generation ID.")
    for _ in range(48):
        status = api_call("GET", f"{API}/generations/{generation_id}", token)
        if status.get("status") == "completed":
            if not status.get("gammaUrl"):
                raise RuntimeError("Gamma returned no hosted presentation URL.")
            # Do not log any expiring signed export URL.
            return {
                "status": "completed",
                "gammaUrl": status["gammaUrl"],
                "generationId": generation_id,
                "credits": status.get("credits"),
            }
        if status.get("status") in ("failed", "error"):
            raise RuntimeError("Gamma generation failed.")
        time.sleep(5)
    raise RuntimeError("Gamma generation did not finish within the poll limit.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Offline validation (default)")
    modes.add_argument("--publish", action="store_true", help="Send reviewed public text to Gamma")
    parser.add_argument("--confirm-external-generation", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.publish:
            if not args.confirm_external_generation:
                raise ValueError("--publish requires --confirm-external-generation.")
            result = publish()
        else:
            spec = build_payload()
            result = {
                "mode": "offline-dry-run", "cards": 11,
                "source": str(SOURCE.relative_to(ROOT)),
                "content_characters": len(spec["inputText"]),
                "externalAccess": spec["sharingOptions"]["externalAccess"],
                "ready_for_manual_publish": True,
            }
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError, UnicodeError) as exc:
        print(f"Gamma: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
