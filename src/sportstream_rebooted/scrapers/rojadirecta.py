import requests
from bs4 import BeautifulSoup
from sportstream_rebooted.core.config import settings

def scrape():
    url = "https://www.rojadirectaenvivo.pl/programacion.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    filtered_matches = []

    for match_li in soup.select("ul.menu > li"):
        title_element = match_li.find("a")
        if not title_element:
            continue

        title_text = title_element.get_text(separator=" ", strip=True).lower()
        print(settings.teams)
        # Filter by team names: example is 'milan' or 'inter'
        if not any(t.lower() in title_text.lower() for t in settings.teams):
            continue
        print(title_text)

        match_name = title_element.contents[0].strip()
        time_span = title_element.find("span", class_="t")
        match_time = time_span.get_text(strip=True) if time_span else "Unknown"

        channels = []
        for ch in match_li.select("ul > li.subitem1 > a"):
            channels.append({
                "name": ch.get_text(strip=True),
                "url": ch.get("href")
            })

        filtered_matches.append({
            "match": match_name,
            "time": match_time,
            "channels": channels,
            "source": "rojadirecta"  # optional for reference
        })

    print(f"rojadirecta: Scraped {len(filtered_matches)} matches")
    return filtered_matches
