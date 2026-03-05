import urllib.parse
from bs4 import BeautifulSoup
from .base import TorrentSource


class X1337Source(TorrentSource):
    id = "1337x"
    name = "1337x"
    categories = ["movies", "tv", "games", "music", "apps", "anime"]
    MIRRORS = ["https://1337x.to", "https://1337x.st", "https://x1337x.ws"]
    CAT_MAP = {
        "movies": "Movies", "tv": "TV", "games": "Games",
        "music": "Music", "apps": "Apps", "anime": "Anime",
    }

    async def search(self, session, query, category, limit):
        cat_path = (
            f"category-search/{urllib.parse.quote(query)}/{self.CAT_MAP[category]}/1/"
            if category in self.CAT_MAP
            else f"search/{urllib.parse.quote(query)}/1/"
        )
        for mirror in self.MIRRORS:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(f"{mirror}/{cat_path}", headers=headers, timeout=10) as r:
                    if r.status != 200:
                        continue
                    html = await r.text()
                results = await self._parse_and_fetch(session, mirror, html, limit)
                if results:
                    return results
            except Exception as e:
                print(f"[1337x] {mirror} error: {e}")
        return []

    async def _parse_and_fetch(self, session, mirror, html, limit):
        import asyncio
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table.table-list tbody tr")[:limit]
        tasks = [self._fetch_magnet(session, mirror, row) for row in rows]
        magnets = await asyncio.gather(*tasks, return_exceptions=True)
        results = []
        for row, magnet in zip(rows, magnets):
            if isinstance(magnet, Exception) or not magnet:
                continue
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            name = cols[0].find("a", href=lambda h: h and "/torrent/" in h)
            seeders = cols[1].text.strip()
            leechers = cols[2].text.strip()
            size = cols[4].text.strip() if len(cols) > 4 else ""
            results.append(self._result(
                title=name.text.strip() if name else "Unknown",
                magnet=magnet, size=size,
                seeders=seeders, leechers=leechers, category="general",
            ))
        return results

    async def _fetch_magnet(self, session, mirror, row):
        link = row.find("a", href=lambda h: h and "/torrent/" in h)
        if not link:
            return None
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            async with session.get(f"{mirror}{link['href']}", headers=headers, timeout=8) as r:
                html = await r.text()
            soup = BeautifulSoup(html, "html.parser")
            magnet = soup.find("a", href=lambda h: h and h.startswith("magnet:"))
            return magnet["href"] if magnet else None
        except Exception:
            return None
