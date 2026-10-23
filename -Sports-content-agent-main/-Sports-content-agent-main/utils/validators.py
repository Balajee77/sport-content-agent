
import re


def clean_source_url(url):
    """
    Convert markdown-style URLs like:
    [https://example.com](https://example.com)
    into:
    https://example.com
    """

    if not url:
        return None

    url = str(url).strip()

    match = re.match(
        r"\[(https?://[^\]]+)\]\((https?://[^)]+)\)",
        url
    )

    if match:
        return match.group(2)

    return url
