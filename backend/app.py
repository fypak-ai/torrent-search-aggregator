from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from sources import get_all_sources

app = Flask(__name__)
CORS(app)

SOURCES = get_all_sources()


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

    results = asyncio.run(_search_all(enabled_sources, query, category, limit))
    return jsonify({"query": query, "total": len(results), "results": results})


async def _search_all(sources, query, category, limit):
    import aiohttp
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [s.search(session, query, category, limit) for s in sources]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in all_results:
            if isinstance(r, list):
                results.extend(r)
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
