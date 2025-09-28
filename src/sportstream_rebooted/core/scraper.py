import asyncio
import json
import logging
from sportstream_rebooted.scrapers.rojadirecta import scrape as scrape_rojadirecta
from sportstream_rebooted.scrapers.daddylive import scrape as scrape_daddylive

logger = logging.getLogger(__name__)
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
    logger.info(f"✅ Total scraped: {len(scraped_links)}")
