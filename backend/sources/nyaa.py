import re
from .base import TorrentSource


class NyaaSource(TorrentSource):
    id = "nyaa"
    name = "Nyaa"
    categories = ["anime", "manga", "software", "audio", "video"]
    BASE_URL = "https://nyaa.si"
    CATEGORY_MAP = {
        "anime": "1_0", "manga": "3_0", "audio": "2_0",
        "software": "6_0", "video": "4_0", "all": "0_0",
    }

    async def search(self, session, query, category, limit):
        cat = self.CATEGORY_MAP.get(category, "0_0")
        try:
            params = {"f": 0, "c": cat, "q": query, "p": 1}
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(f"{self.BASE_URL}/?page=rss", params=params, headers=headers, timeout=10) as r:
                text = await r.text()
            return self._parse_rss(text, limit)
        except Exception as e:
            print(f"[Nyaa] error: {e}")
            return []

    def _parse_rss(self, text, limit):
        items = re.findall(r"<item>(.*?)</item>", text, re.DOTALL)
        results = []
        for item in items[:limit]:
            title = re.search(r"<title><!\[CDATA\[(.*?)]]></title>", item)
            magnet = re.search(r"<nyaa:magnetUri><!\[CDATA\[(magnet:\?.*?)]]>", item)
            seeders = re.search(r"<nyaa:seeders>(\d+)</nyaa:seeders>", item)
            leechers = re.search(r"<nyaa:leechers>(\d+)</nyaa:leechers>", item)
            size = re.search(r"<nyaa:size>(.*?)</nyaa:size>", item)
            pub_date = re.search(r"<pubDate>(.*?)</pubDate>", item)
            if title and magnet:
                results.append(self._result(
                    title=title.group(1),
                    magnet=magnet.group(1),
                    size=size.group(1) if size else "",
                    seeders=int(seeders.group(1)) if seeders else 0,
                    leechers=int(leechers.group(1)) if leechers else 0,
                    category="anime",
                    date=pub_date.group(1) if pub_date else "",
                ))
        return results
