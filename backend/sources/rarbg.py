import urllib.parse
from bs4 import BeautifulSoup
from .base import TorrentSource


class RARBGSource(TorrentSource):
    id = "rarbg"
    name = "RARBG Mirror"
    categories = ["movies", "tv", "games", "music", "software", "anime"]
    MIRRORS = [
        "https://rarbgprx.org",
        "https://rarbgaccess.org",
        "https://proxyrarbg.org",
    ]

    async def search(self, session, query, category, limit):
        for mirror in self.MIRRORS:
            try:
                url = f"{mirror}/search/?search={urllib.parse.quote(query)}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(url, headers=headers, timeout=10) as r:
                    if r.status != 200:
                        continue
                    html = await r.text()
                results = self._parse(html, limit)
                if results:
                    return results
            except Exception as e:
                print(f"[RARBG] {mirror} error: {e}")
        return []

    def _parse(self, html, limit):
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table.lista2t tr.lista2")[:limit]
        results = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            name_el = cols[1].find("a")
            magnet_el = row.find("a", href=lambda h: h and h.startswith("magnet:"))
            if not name_el or not magnet_el:
                continue
            results.append(self._result(
                title=name_el.text.strip(),
                magnet=magnet_el["href"],
                size=cols[3].text.strip() if len(cols) > 3 else "",
                seeders=cols[4].text.strip() if len(cols) > 4 else "0",
                leechers=cols[5].text.strip() if len(cols) > 5 else "0",
                category="general",
            ))
        return results
