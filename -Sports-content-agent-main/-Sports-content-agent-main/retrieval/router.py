
RECENT_KEYWORDS = [
    "latest",
    "recent",
    "today",
    "yesterday",
    "current",
    "this week",
    "this month",
    "this season",
    "transfer",
    "transfers",
    "live",
    "result",
    "results",
    "2026"
]


def detect_retrieval_mode(query: str):
    query_lower = query.lower()

    for keyword in RECENT_KEYWORDS:
        if keyword in query_lower:
            return "web"

    historical_keywords = [
        "history",
        "historical",
        "first",
        "won the",
        "world cup",
        "record",
        "rules",
        "invented",
        "founded"
    ]

    for keyword in historical_keywords:
        if keyword in query_lower:
            return "chroma"

    return "hybrid"
