import urllib.request
import urllib.parse
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive",
}

def clean_html(html: str) -> str:
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<style[\s\S]*?</style>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&amp;', '&', html)
    html = re.sub(r'&lt;', '<', html)
    html = re.sub(r'&gt;', '>', html)
    html = re.sub(r'&#[0-9]+;', '', html)
    html = re.sub(r'\s+', ' ', html).strip()
    lines = [l.strip() for l in html.split('.') if len(l.strip()) > 40]
    return '. '.join(lines[:120])

def search_web(query: str) -> str:
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore")
        titles   = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        clean    = lambda t: re.sub(r'<[^>]+>', '', t).strip()
        results  = []
        for i, (t, s) in enumerate(zip(titles[:8], snippets[:8])):
            ct = clean(t)
            cs = clean(s)
            if ct and cs:
                results.append(f"Result {i+1}: {ct}\n{cs}")
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search error: {e}"

def browse_url(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore")
        return clean_html(html)[:3000]
    except Exception as e:
        return f"Could not browse {url}: {e}"

def search_and_browse(query: str) -> str:
    """Search and also fetch top result page for richer content."""
    search_results = search_web(query)
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore")
        # get all real URLs from results
        all_urls = re.findall(r'href="(https?://(?!.*duckduckgo)[^"&]+)"', html)
        # skip ad and tracker URLs
        skip = ["duckduckgo","duck.com","microsoft","bing","yahoo","doubleclick","googlesyndication"]
        real_urls = [u for u in all_urls if not any(s in u.lower() for s in skip)]
        if real_urls:
            page_content = browse_url(real_urls[0])
            return f"=== SEARCH RESULTS ===\n{search_results}\n\n=== PAGE CONTENT (top result) ===\n{page_content}"
    except:
        pass
    return search_results