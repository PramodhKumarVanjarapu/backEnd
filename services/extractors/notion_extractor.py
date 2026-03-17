import requests
from bs4 import BeautifulSoup

def extract_text_from_notion(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ValueError("Could not fetch Notion page. Make sure it is public.")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all visible text blocks
    blocks = soup.find_all(["p", "h1", "h2", "h3", "li"])
    text = "\n".join([block.get_text() for block in blocks if block.get_text().strip()])

    if not text:
        raise ValueError("No readable content found. Make sure the Notion page is public.")

    return text.strip()