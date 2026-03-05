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
        def _int(v):
            try:
                return int(str(v).strip().replace(',', ''))
            except Exception:
                return 0

        r = {
            "title": title,
            "magnet": magnet,
            "size": str(size).strip(),
            "seeders": _int(seeders),
            "leechers": _int(leechers),
            "source": self.name,
            "source_id": self.id,
            "category": category,
            "date": date,
        }
        if extra:
            r.update(extra)
        return r
