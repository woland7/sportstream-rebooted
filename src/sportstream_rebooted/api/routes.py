import json
import re
from collections import defaultdict

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sportstream_rebooted.core.scraper import scraped_links, scrape_links

router = APIRouter()
templates = Jinja2Templates(directory="sportstream_rebooted/templates")

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return set(text.split())


def similarity(a, b):
    tokens_a = tokenize(a)
    tokens_b = tokenize(b)
    common = tokens_a & tokens_b
    return len(common) / max(len(tokens_a), len(tokens_b))


def group_matches_by_similarity(matches, threshold=0.6):
    groups = []

    for match in matches:
        added = False
        for group in groups:
            group_name, items = group
            if similarity(match['match'], group_name) >= threshold:
                items.append(match)
                added = True
                break
        if not added:
            groups.append([match['match'], [match]])
    return groups


# --- Build final grouped dict for Jinja2 ---
def build_grouped_matches(groups):
    grouped_matches = defaultdict(list)
    for group_name, items in groups:
        for item in items:
            for ch in item["channels"]:
                grouped_matches[group_name].append({
                    "channel_name": ch["name"],
                    "url": ch["url"],
                    "time": item.get("time"),
                    "source": item.get("source"),
                })
    return grouped_matches

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print(json.dumps(scraped_links, indent=2))
    groups = group_matches_by_similarity(scraped_links)
    grouped_matches = build_grouped_matches(groups)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "grouped_matches": grouped_matches
    })

# Optional: Manual refresh route
@router.post("/refresh")
async def refresh_data():
    print("[REFRESH] Manually scraping links...")
    scrape_links()
    return RedirectResponse(url="/", status_code=302)
