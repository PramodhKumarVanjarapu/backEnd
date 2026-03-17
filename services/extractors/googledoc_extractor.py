import requests
import re
from bs4 import BeautifulSoup

def extract_text_from_googledoc(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("Invalid Google Doc URL")

    doc_id = match.group(1)
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    response = requests.get(export_url, timeout=10)
    if response.status_code != 200:
        raise ValueError("Could not fetch Google Doc. Make sure it is set to public.")

    return response.text.strip()