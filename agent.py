#!/usr/bin/env python3
"""Mint a Hive receipt from a minimal LangChain LLM run."""

from __future__ import annotations

import os
import threading
from typing import TypedDict

import httpx
from langchain_core.language_models.fake import FakeListLLM
from langchain_hive import HiveCallbackHandler
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    prompt: str
    response: str


class RecordingHiveCallbackHandler(HiveCallbackHandler):
    """Hive callback that records the receipt URL for deterministic demos."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.receipt_url: str | None = None
        self.error: str | None = None
        self._receipt_event = threading.Event()

    def _post(self, body: dict[str, object]) -> None:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(self.endpoint, json=body, headers=headers)
            response.raise_for_status()
            data = response.json()
            receipt_id = data.get("receipt_id") or data.get("id")
            if not receipt_id:
                self.error = "Hive response did not include a receipt_id"
                return
            self.receipt_url = f"https://thehiveryiq.com/verify/?id={receipt_id}"
        except Exception as exc:  # pragma: no cover - network edge case
            self.error = str(exc)
        finally:
            self._receipt_event.set()

    def wait_for_receipt(self, timeout: float = 15.0) -> str:
        if not self._receipt_event.wait(timeout):
            raise TimeoutError("Timed out waiting for Hive receipt")
        if self.error:
            raise RuntimeError(f"Hive receipt minting failed: {self.error}")
        if not self.receipt_url:
            raise RuntimeError("Hive receipt minting finished without a verify URL")
        return self.receipt_url


def main() -> None:
    tag = os.environ.get("HIVE_BOUNTY_TAG", "local-demo")
    require_bounty_tag = os.environ.get("HIVE_REQUIRE_BOUNTY_TAG") == "1"
    if require_bounty_tag and not tag.startswith("bounty_"):
        raise SystemExit("Set HIVE_BOUNTY_TAG=bounty_... before claim validation")

    callback = RecordingHiveCallbackHandler(tag=tag, timeout=10.0)
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
    print(f"Hive verify URL: {callback.wait_for_receipt()}")


if __name__ == "__main__":
    main()
