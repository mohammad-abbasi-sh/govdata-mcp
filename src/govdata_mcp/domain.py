"""Domain logic: shape govdata.de CKAN API responses into compact
dicts (stdlib only).

Data source: the official CKAN API of Germany's national open-data
portal (https://www.govdata.de/ckan/api/3/action/...) — free, no key,
no login. Actions used: package_search, package_show,
organization_list, resource_show.
"""
from __future__ import annotations

import json
import urllib.parse

BASE = "https://www.govdata.de/ckan/api/3/action"


def validate_limit(limit: int) -> int:
    if not 1 <= limit <= 50:
        raise ValueError(f"limit out of range: {limit} (expected 1..50)")
    return limit


def search_url(query: str, rows: int, sort: str) -> str:
    params = {"q": query, "rows": str(rows)}
    if sort == "recent":
        params["sort"] = "metadata_modified desc"
    return BASE + "/package_search?" + urllib.parse.urlencode(params)


def recent_url(rows: int) -> str:
    params = {"rows": str(rows), "sort": "metadata_modified desc"}
    return BASE + "/package_search?" + urllib.parse.urlencode(params)


def dataset_url(dataset_id: str) -> str:
    return BASE + "/package_show?" + urllib.parse.urlencode({"id": dataset_id})


def publishers_url(limit: int) -> str:
    params = {"all_fields": "true", "limit": str(limit)}
    return BASE + "/organization_list?" + urllib.parse.urlencode(params)


def resource_url(resource_id: str) -> str:
    return BASE + "/resource_show?" + urllib.parse.urlencode({"id": resource_id})


def _load(text: str, what: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid {what}: {e}") from e
    if not data.get("success"):
        err = data.get("error") or {}
        raise ValueError(f"govdata.de error: {err.get('message') or err}")
    return data["result"]


def _compact_dataset(pkg: dict) -> dict:
    org = pkg.get("organization") or {}
    return {
        "id": pkg.get("id") or "",
        "name": pkg.get("name") or "",
        "title": pkg.get("title") or "",
        "notes": (pkg.get("notes") or "")[:400],
        "organization": org.get("title") or org.get("name") or "",
        "license": pkg.get("license_title") or "",
        "num_resources": pkg.get("num_resources") or 0,
        "tags": [t.get("name") for t in (pkg.get("tags") or [])[:5]],
        "metadata_modified": pkg.get("metadata_modified") or "",
        "resources": [
            {"id": r.get("id") or "", "name": r.get("name") or "",
             "format": r.get("format") or "", "url": r.get("url") or ""}
            for r in (pkg.get("resources") or [])[:10]
        ],
    }


def parse_search(text: str) -> dict:
    result = _load(text, "package_search response")
    return {
        "total_results": result.get("count") or 0,
        "items": [_compact_dataset(p) for p in result.get("results") or []],
    }


def parse_dataset(text: str) -> dict:
    return _compact_dataset(_load(text, "package_show response"))


def parse_publishers(text: str) -> list[dict]:
    result = _load(text, "organization_list response")
    orgs = [{
        "id": o.get("id") or "",
        "name": o.get("name") or "",
        "title": o.get("title") or "",
        "package_count": o.get("package_count") or 0,
        "description": (o.get("description") or "")[:200],
    } for o in result]
    orgs.sort(key=lambda o: o["package_count"], reverse=True)
    return orgs


def parse_resource(text: str) -> dict:
    r = _load(text, "resource_show response")
    return {
        "id": r.get("id") or "",
        "name": r.get("name") or "",
        "format": r.get("format") or "",
        "url": r.get("url") or r.get("download_url") or "",
        "description": (r.get("description") or "")[:400],
        "size": r.get("size"),
        "mimetype": r.get("mimetype") or "",
        "created": r.get("created") or "",
        "last_modified": r.get("last_modified") or "",
        "package_id": r.get("package_id") or "",
    }
