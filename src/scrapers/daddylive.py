from playwright.async_api import async_playwright

async def scrape():
    filter_keywords = ["internazionale", "chelsea"]
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://daddylivestream.com", timeout=15000)
        await page.wait_for_timeout(2000)

        event_infos = await page.query_selector_all(".event-info")
        print(event_infos)
        for event in event_infos:
            text = (await event.inner_text()).strip().lower()
            if any(team in text for team in filter_keywords):
                try:
                    await event.click()
                    await page.wait_for_timeout(2000)

                    results.append({
                        "match": text.title(),
                        "time": "Unknown",
                        "channels": [],
                        "source": "daddylive"
                    })
                except Exception as e:
                    print(f"[daddylive] Error clicking event: {e}")

        await browser.close()

    return results
