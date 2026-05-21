#!/usr/bin/env python3
"""Mint a Hive receipt from a minimal LangChain LLM run."""

from __future__ import annotations

import os
import time
from typing import TypedDict

from langchain_core.language_models.fake import FakeListLLM
from langchain_hive import HiveCallbackHandler
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    prompt: str
    response: str


def main() -> None:
    tag = os.environ.get("HIVE_BOUNTY_TAG", "local-demo")
    callback = HiveCallbackHandler(tag=tag, verbose=True, timeout=10.0)
    llm = FakeListLLM(
        responses=[
            "Hive receipt demo complete: LangChain callback executed successfully."
        ],
        callbacks=[callback],
    )

    def call_model(state: AgentState) -> AgentState:
        result = llm.invoke(state["prompt"])
        return {"prompt": state["prompt"], "response": result}

    graph = StateGraph(AgentState)
    graph.add_node("call_model", call_model)
    graph.add_edge(START, "call_model")
    graph.add_edge("call_model", END)
    app = graph.compile()

    final_state = app.invoke(
        {
            "prompt": (
                "Return one short sentence confirming that this LangGraph run "
                "can mint a Hive receipt."
            ),
            "response": "",
        }
    )
    print(f"Agent response: {final_state['response']}")

    # langchain-hive posts receipts on a background thread so agent latency is
    # not blocked. Give the receipt request time to finish and print its URL.
    time.sleep(3)


if __name__ == "__main__":
    main()
