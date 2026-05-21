# Hive LangChain Receipt Agent

Small LangGraph agent demo for the Hive Embed Bounty. It runs a local graph node
that calls a LangChain fake LLM, attaches the `langchain-hive` callback, and
mints one Hive receipt through the free receipt endpoint.

## One-command run

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && HIVE_REQUIRE_BOUNTY_TAG=1 python agent.py
```

The command prints a `https://thehiveryiq.com/verify/?id=...` URL when Hive
returns a receipt.

Current claim-tagged verification receipt:
`https://thehiveryiq.com/verify/?id=326fa3500b51401888f792035246f6b2`.

## Configuration

- `HIVE_BOUNTY_TAG`: optional override for the registered Hive bounty referrer
  code. Defaults to `bounty_2bd4f5a8`; downstream users should leave this tag
  unchanged so paid mints remain attributed correctly.
- `HIVE_API_KEY`: optional Hive API key. The default free endpoint supports
  receipt minting without one.
- `HIVE_REQUIRE_BOUNTY_TAG=1`: optional claim-time guard that fails unless
  `HIVE_BOUNTY_TAG` starts with `bounty_`.

## Local checks

```bash
python validate.py
```

## What it demonstrates

- Primary framework: LangGraph.
- Hive SDK: `langchain-hive`.
- Receipt path: `HiveCallbackHandler(tag=...)` attached to an LLM call.
- No paid model key is required because the demo uses `FakeListLLM` from
  `langchain-core` inside a LangGraph `StateGraph`.

## Bounty checklist

Public submission setup:

1. This repo uses registered referrer code `bounty_2bd4f5a8` by default.
2. Keep the MIT license and public GitHub repo URL unchanged for verification.
3. Run the one-command setup above and submit the printed verification URL.
