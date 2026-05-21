#!/usr/bin/env python3
"""Local checks for the Hive bounty demo repository."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(path: str, *needles: str) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{path} is missing {needle!r}")


def main() -> None:
    require("LICENSE", "MIT License")
    require("requirements.txt", "langgraph", "langchain-hive")
    require(
        "agent.py",
        "StateGraph",
        "FakeListLLM",
        "HiveCallbackHandler",
        "RecordingHiveCallbackHandler",
        "HIVE_BOUNTY_TAG",
        "HIVE_REQUIRE_BOUNTY_TAG",
    )
    require(
        "README.md",
        "One-command run",
        "python3 -m venv .venv",
        "Primary framework: LangGraph",
        "HIVE_BOUNTY_TAG",
        "HIVE_REQUIRE_BOUNTY_TAG",
    )
    print("validate.py passed")


if __name__ == "__main__":
    main()
