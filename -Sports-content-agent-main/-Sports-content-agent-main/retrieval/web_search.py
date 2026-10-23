
from tavily import TavilyClient


TRUSTED_DOMAINS = {
    "Cricket": [
        "icc-cricket.com",
        "espncricinfo.com",
        "cricbuzz.com"
    ],
    "Football": [
        "fifa.com",
        "uefa.com",
        "espn.com"
    ],
    "Tennis": [
        "atptour.com",
        "wtatennis.com",
        "wimbledon.com"
    ],
    "Badminton": [
        "bwfbadminton.com",
        "olympics.com"
    ],
    "Basketball": [
        "nba.com",
        "fiba.basketball",
        "espn.com"
    ]
}


def search_sports_web(
    api_key,
    sport,
    query=None,
    max_results=5
):

    tavily = TavilyClient(api_key=api_key)

    if query is None:
        query = (
            f"{sport} official latest results records "
            f"statistics tournament outcomes"
        )

    trusted_domains = TRUSTED_DOMAINS.get(sport, [])

    try:
        response = tavily.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_domains=trusted_domains
        )

    except Exception:
        response = tavily.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

    results = []

    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title", "Unknown Source"),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score", 0)
            }
        )

    return results


def format_web_context(results):

    if not results:
        return "No reliable web information retrieved."

    formatted_context = []

    for i, item in enumerate(results, start=1):
        formatted_context.append(
            f"""
SOURCE {i}
Title: {item['title']}
URL: {item['url']}
Information: {item['content']}
"""
        )

    return "\n".join(formatted_context)
