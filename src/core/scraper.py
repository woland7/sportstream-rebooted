import asyncio

from src.scrapers.rojadirecta import scrape as scrape_rojadirecta
from src.scrapers.daddylive import scrape as scrape_daddylive

scraped_links = []

scrapers = {
    "rojadirecta": scrape_rojadirecta,
    "daddylive": scrape_daddylive,
}

async def scrape_links():
    global scraped_links
    all_matches = []

    for name, scraper_func in scrapers.items():
        try:
            print(f"Scraping {name}...")

            # Check if scraper_func is coroutine (async def)
            if asyncio.iscoroutinefunction(scraper_func):
                matches = await scraper_func()
            else:
                matches = scraper_func()

            all_matches.extend(matches)
        except Exception as e:
            print(f"[ERROR] Failed scraping {name}: {e}")

    scraped_links.clear()
    scraped_links.extend(all_matches)
    print(f"✅ Total scraped: {len(scraped_links)}")
