import random
import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def deep_process(user_query):
    print(f"[DeepThink] Searching multiple sources for: '{user_query}'...")
    try:
        search_results = _search_google(user_query, num_results=10)
        if not search_results:
            search_results = _duckduckgo_search(user_query, num_results=10)

        if not search_results:
            return None, "No search results found. Please try again with a different query."

        other_sources = [
            url for url in search_results if "wikipedia.org" not in url]
        top_url = other_sources[0] if other_sources else search_results[0]

        print(f"[DeepThink] Reading content from source: {top_url}")

        paragraphs = _fetch_page_paragraphs(top_url)
        if not paragraphs:
            return None, "No detailed content found at this source."

        return {"data": paragraphs, "url": top_url}, None

    except Exception as e:
        return None, f"Error: {str(e)}"


def _search_google(user_query, num_results=10):
    try:
        from googlesearch import search as google_search
    except ImportError:
        return []

    try:
        results = list(google_search(
            user_query, num_results=num_results, lang="vi"))
        if results:
            return results
        return list(google_search(user_query, num_results=num_results))
    except TypeError:
        try:
            return list(google_search(user_query, num=num_results, lang="vi"))
        except Exception:
            return []
    except Exception:
        return []


def _duckduckgo_search(user_query, num_results=10):
    try:
        resp = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": user_query},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for a in soup.select("a.result__a, a[data-testid='result-title-a']"):
            href = a.get("href")
            if href and href.startswith("http"):
                results.append(href)
                if len(results) >= num_results:
                    break

        if not results:
            for a in soup.select("a"):
                href = a.get("href")
                if href and href.startswith("http") and "duckduckgo.com" not in href:
                    results.append(href)
                    if len(results) >= num_results:
                        break

        return results
    except Exception:
        return []


def _fetch_page_paragraphs(url):
    try:
        resp = requests.get(
            url, headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer", "aside"]):
            tag.extract()

        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text(separator=" ", strip=True)
            if len(text) >= 80:
                paragraphs.append(_normalize_text(text))

        if not paragraphs:
            text = soup.get_text(separator="\n", strip=True)
            for line in text.splitlines():
                clean_line = line.strip()
                if len(clean_line) >= 100:
                    paragraphs.append(_normalize_text(clean_line))
                    if len(paragraphs) >= 10:
                        break

        return paragraphs[:20]
    except Exception:
        return []


def _normalize_text(text):
    return " ".join(text.split())
