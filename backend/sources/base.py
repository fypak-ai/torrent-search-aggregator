from abc import ABC, abstractmethod
from typing import List, Dict


class TorrentSource(ABC):
    id: str = ""
    name: str = ""
    categories: List[str] = []

    @abstractmethod
    async def search(self, session, query: str, category: str, limit: int) -> List[Dict]:
        pass

    def _result(self, title, magnet, size="", seeders=0, leechers=0, category="", date="", extra=None):
        r = {
            "title": title,
            "magnet": magnet,
            "size": size,
            "seeders": int(seeders) if seeders else 0,
            "leechers": int(leechers) if leechers else 0,
            "source": self.name,
            "source_id": self.id,
            "category": category,
            "date": date,
        }
        if extra:
            r.update(extra)
        return r
