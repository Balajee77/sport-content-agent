
from retrieval.router import detect_retrieval_mode
from retrieval.web_search import search_sports_web, format_web_context
from retrieval.chroma_retriever import search_chroma, format_chroma_context


def retrieve_context(
    api_key,
    sport,
    query,
    web_results=4,
    chroma_results=4
):
    mode = detect_retrieval_mode(query)

    web_context = ""
    chroma_context = ""

    if mode in ["web", "hybrid"]:
        web_data = search_sports_web(
            api_key=api_key,
            sport=sport,
            query=query,
            max_results=web_results
        )

        web_context = format_web_context(web_data)

    if mode in ["chroma", "hybrid"]:
        chroma_data = search_chroma(
            sport=sport,
            query=query,
            n_results=chroma_results
        )

        chroma_context = format_chroma_context(chroma_data)

    combined_context = f"""
RETRIEVAL MODE: {mode.upper()}

WEB CONTEXT:
{web_context if web_context else "Not used"}

CHROMADB CONTEXT:
{chroma_context if chroma_context else "Not used"}
"""

    return {
        "mode": mode,
        "context": combined_context
    }
