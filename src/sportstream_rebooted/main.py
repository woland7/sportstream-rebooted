from fastapi import FastAPI
from contextlib import asynccontextmanager
from sportstream_rebooted.core.scraper import scrape_links, scraped_links
from sportstream_rebooted.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Scraping at startup...")
    await scrape_links()
    print(f"✅ Scraped {len(scraped_links)} matches.")
    yield
    print("👋 App shutting down.")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
