from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import nest_asyncio
from sources import get_all_sources

nest_asyncio.apply()

app = Flask(__name__)
CORS(app)

SOURCES = get_all_sources()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


@app.route("/api/search")
def search():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    sources_param = request.args.get("sources", "all")
    limit = int(request.args.get("limit", 30))

    if not query:
        return jsonify({"error": "query required"}), 400

    enabled_sources = SOURCES if sources_param == "all" else [
        s for s in SOURCES if s.id in sources_param.split(",")
    ]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(_search_all(enabled_sources, query, category, limit))
    return jsonify({"query": query, "total": len(results), "results": results})


async def _search_all(sources, query, category, limit):
    import aiohttp
    results = []
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(
        connector=connector,
        headers=HEADERS
    ) as session:
        tasks = [s.search(session, query, category, limit) for s in sources]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        for s, r in zip(sources, all_results):
            if isinstance(r, list):
                print(f"[OK] {s.name}: {len(r)} results")
                results.extend(r)
            else:
                print(f"[FAIL] {s.name}: {r}")
    results.sort(key=lambda x: x.get("seeders", 0), reverse=True)
    return results[:limit * len(sources)]


@app.route("/api/sources")
def list_sources():
    return jsonify([{
        "id": s.id, "name": s.name,
        "categories": s.categories, "enabled": True
    } for s in SOURCES])


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os
    app.run(
        debug=os.getenv("FLASK_ENV") == "development",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
