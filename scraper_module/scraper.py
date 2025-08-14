import time
import json
import requests
from urllib.parse import urljoin, urldefrag, urlparse
from collections import deque
from bs4 import BeautifulSoup

# Crawl settings
ALLOWED_NETLOCS = {"theinventorymaster.com", "www.theinventorymaster.com"}
HEADERS = {
    "User-Agent": "InventoryMasterBot/1.0 (bot@example.com)"
}

def normalize_url(base, link):
    return urldefrag(urljoin(base, link)).url

def is_allowed_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and parsed.netloc.lower() in ALLOWED_NETLOCS
    except Exception:
        return False

def fetch_with_retries(url, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=15, headers=HEADERS)
            if resp.status_code == 200:
                return resp
            else:
                print(f"[WARN] {url} returned {resp.status_code}")
        except Exception as ex:
            print(f"[ERROR] {url}: {ex}")
        time.sleep(backoff)
    print(f"[FAIL] {url} after {retries} retries")
    return None

def extract_content_structured(soup):
    content = {
        "title": soup.title.string.strip() if soup.title and soup.title.string else "",
        "sections": [],
    }
    content["full_text"] = soup.get_text(separator="\n", strip=True)

    headers = soup.find_all(["h1", "h2", "h3"])
    for h in headers:
        heading = h.get_text(strip=True)
        if not heading:
            continue

        section = {"heading": heading}
        paragraphs = []
        list_items = []
        table_rows = []

        for sib in h.find_next_siblings():
            if sib.name in ["h1", "h2", "h3"]:
                break

            if sib.name == "p":
                text = sib.get_text(strip=True)
                if text:
                    paragraphs.append(text)

            elif sib.name in ["ul", "ol"]:
                items = [li.get_text(" ", strip=True) for li in sib.find_all("li")]
                list_items.extend([item for item in items if item])

            elif sib.name == "table":
                for row in sib.find_all("tr"):
                    cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                    if cells:
                        table_rows.append(cells)

            elif sib.name in ["div", "span", "section"]:
                text = sib.get_text(separator=" ", strip=True)
                if text and len(text.split()) >= 2:
                    paragraphs.append(text)

            elif sib.name in ["strong", "b", "em", "i"]:
                text = sib.get_text(strip=True)
                if text:
                    paragraphs.append(text)

        # Only add fields if they contain data
        if paragraphs:
            section["paragraphs"] = paragraphs
        if list_items:
            section["list_items"] = list_items
        if table_rows:
            section["table_rows"] = table_rows

        content["sections"].append(section)

    return content


def extract_links(soup, base_url):
    links = []
    for a in soup.find_all("a", href=True):
        href = normalize_url(base_url, a["href"])
        if is_allowed_domain(href):
            links.append((href, a.get_text(strip=True)))
    return links

def crawl(start_url, max_pages=100, delay=1):
    visited = set()
    results = []
    pq = deque([start_url])
    sq = deque()

    def is_prefixed(u):
        # e.g. crawl POS category pages first
        return "/tracking-identification-technologies/" in urlparse(u).path \
               or "/inventory-management-software-systems-point-of-sale-systems-pos/" in urlparse(u).path

    while (pq or sq) and len(visited) < max_pages:
        url = pq.popleft() if pq else sq.popleft()
        if url in visited:
            continue
        visited.add(url)
        print(f"[Crawl] {url}")

        resp = fetch_with_retries(url)
        if not resp:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove site‑wide nav/footer
        for nav_blk in soup.find_all(["nav", "footer"]):
            nav_blk.decompose()

        # Extract structured page content
        content = extract_content_structured(soup)
        content["url"] = url
        results.append(content)

        # Extract links
        content_links = extract_links(soup, url)
        for href, _ in content_links:
            if href not in visited:
                if is_prefixed(url) or is_prefixed(href):
                    pq.append(href)
                else:
                    sq.append(href)

        time.sleep(delay)

    return results

def save_results_to_json(data, filename="scraped_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


