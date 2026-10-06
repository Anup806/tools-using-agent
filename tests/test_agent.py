from src.agent import format_search_results, search_web


def test_format_search_results_includes_title_body_and_link():
    results = [
        {
            "title": "Example title",
            "body": "Example summary",
            "href": "https://example.com",
        }
    ]

    formatted = format_search_results(results)

    assert "Example title" in formatted
    assert "Example summary" in formatted
    assert "https://example.com" in formatted


def test_search_web_rejects_empty_query_without_network_call():
    assert search_web.invoke({"query": ""}) == "Error: search query cannot be empty."
