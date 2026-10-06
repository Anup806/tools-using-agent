from __future__ import annotations

import os
import time
from datetime import date
from typing import Any

from ddgs import DDGS
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()


def format_search_results(results: list[dict[str, Any]]) -> str:
    """Format raw search results as compact text for the model."""
    lines = []

    for result in results:
        title = result.get("title", "")
        body = result.get("body", "")
        href = result.get("href", "")
        lines.append(f"{title}: {body[:300]} ({href})")

    return "\n".join(lines)


@tool
def search_web(query: str) -> str:
    """Search the web and return the top results with summaries and links."""
    if not query.strip():
        return "Error: search query cannot be empty."

    for attempt in range(2):
        try:
            results = DDGS().text(query, max_results=3)

            if not results:
                return f"Error: no results found for {query}."

            return format_search_results(results)
        except Exception as error:
            if attempt == 1:
                return f"Error: search failed: {type(error).__name__}: {error}"

            time.sleep(2)

    return "Error: search failed."


def build_agent():
    """Create the research agent without making an API call."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from the .env file.")

    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    thinking = "low" if model_name.startswith("openai/gpt-oss") else None

    llm = ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0.3,
        reasoning_effort=thinking,
    )

    system_prompt = (
        "You are a helpful research assistant. "
        f"Today's date is {date.today()}. "
        "Use search_web for current information and never guess. "
        "Base your answer only on search results. "
        "Write links as plain text and answer in two or three short sentences."
    )

    return create_agent(
        model=llm,
        tools=[search_web],
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )


def main() -> None:
    agent = build_agent()
    config = {
        "configurable": {"thread_id": "local-user"},
        "recursion_limit": 10,
    }

    print("Research agent ready. Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        try:
            result = agent.invoke({"messages": [("user", question)]}, config)
            print("\nAgent:", result["messages"][-1].content)
        except Exception as error:
            print(f"\nAgent error: {error}")


if __name__ == "__main__":
    main()
