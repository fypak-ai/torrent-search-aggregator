import urllib.parse
from bs4 import BeautifulSoup
from .base import TorrentSource


class TorrentGalaxySource(TorrentSource):
    id = "tgx"
    name = "Torrent Galaxy"
    categories = ["movies", "tv", "music", "games", "software", "anime", "books"]
    MIRRORS = ["https://torrentgalaxy.to", "https://tgx.rs"]
    CAT_MAP = {
        "movies": "c3=1", "tv": "c5=1", "music": "c22=1",
        "games": "c10=1", "software": "c18=1", "anime": "c28=1", "books": "c13=1",
    }

    async def search(self, session, query, category, limit):
        cat_param = self.CAT_MAP.get(category, "")
        q = urllib.parse.quote(query)
        for mirror in self.MIRRORS:
            try:
                url = f"{mirror}/torrents.php?search={q}&lang=0&nox=2&{cat_param}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(url, headers=headers, timeout=12) as r:
                    if r.status != 200:
                        continue
                    html = await r.text()
                results = self._parse(html, limit)
                if results:
                    return results
            except Exception as e:
                print(f"[TGX] {mirror} error: {e}")
        return []

    def _parse(self, html, limit):
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("div.tgxtablerow")[:limit]
        results = []
        for row in rows:
            try:
                name_tag = row.select_one("div.tgxtablecell:nth-child(4) a")
                magnet_tag = row.find("a", href=lambda h: h and h.startswith("magnet:"))
                if not name_tag or not magnet_tag:
                    continue
                seeders_tag = row.select_one("span.tgxtableseeds")
                leechers_tag = row.select_one("span.tgxtableleechers")
                size_tag = row.select_one("span.badge-secondary")
                results.append(self._result(
                    title=name_tag.get_text(strip=True),
                    magnet=magnet_tag["href"],
                    size=size_tag.get_text(strip=True) if size_tag else "",
                    seeders=seeders_tag.get_text(strip=True) if seeders_tag else 0,
                    leechers=leechers_tag.get_text(strip=True) if leechers_tag else 0,
                    category="general",
                ))
            except Exception:
                continue
        return results
