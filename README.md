# Hive LangChain Receipt Agent

Small LangGraph agent demo for the Hive Embed Bounty. It runs a local graph node
that calls a LangChain fake LLM, attaches the `langchain-hive` callback, and
mints one Hive receipt through the free receipt endpoint.

## One-command run

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && python agent.py
```

The command prints a `https://thehiveryiq.com/verify/?id=...` URL when Hive
returns a receipt.

## Configuration

- `HIVE_BOUNTY_TAG`: optional referrer code from Hive bounty registration.
  Defaults to `local-demo`.
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

Before public submission:

1. Register on the bounty page and replace `local-demo` with the returned
   referrer code through `HIVE_BOUNTY_TAG`.
2. Push this repository publicly with the MIT license.
3. Run `HIVE_REQUIRE_BOUNTY_TAG=1 HIVE_BOUNTY_TAG=bounty_xxxx python agent.py`
   and submit the printed verification URL.
