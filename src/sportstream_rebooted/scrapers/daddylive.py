from unittest.mock import mock_open

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from sportstream_rebooted.core.config import settings


async def scrape():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # set to True for headless mode
        page = await browser.new_page()
        await page.goto("https://daddylivestream.com", timeout=15000)
        await page.wait_for_timeout(2000)

        event_infos = await page.query_selector_all(".event-info")
        matching = []

        for event in event_infos:
            text = (await event.inner_text()).strip().lower()
            if any(team in text for team in settings.teams):
                matching.append((event, text))

        for event, text in matching:
            if any(t in text.lower() for t in ['soccer', 'romania', 'nfl']):
                continue
            try:
                parent = await event.evaluate_handle("e => e.parentElement")
                await parent.dispatch_event("click")

                print(f"Clicked: {text}")
                await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"[Warning] Click issue (ignored): {e}")

        # Wait a bit to ensure all content is loaded
        await page.wait_for_timeout(3000)

        from urllib.parse import urljoin

        BASE_URL = "https://daddylivestream.com"

# Parse the final HTML content
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Save dump if needed
        with open("daddylive_dump.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        rows = soup.select("tr.event-row")

        for row in rows:
            match_name_el = row.select_one(".event-info")
            match_time_el = row.select_one(".event-time strong")

            match_name = match_name_el.get_text(strip=True) if match_name_el else "Unknown"
            if "soccer" in match_name:
                print("skipping")
                continue
            match_time = match_time_el.get_text(strip=True) if match_time_el else "Unknown"

            # Check if it's a match we filtered earlier
            if not any(team in match_name.lower() for team in settings.teams):
                continue

            # The channel row is the next sibling
            channel_row = row.find_next_sibling("tr", class_="channel-row")
            channels = []

            if channel_row:
                links = channel_row.select("a.channel-button-small")
                for link in links:
                    channel_name = link.get_text(strip=True)
                    channel_url = urljoin(BASE_URL, link.get("href"))
                    channels.append({
                        "name": channel_name,
                        "url": channel_url
                    })

            results.append({
                "match": match_name,
                "time": match_time,
                "channels": channels,
                "source": "daddylive"
            })


        await browser.close()

    return results
