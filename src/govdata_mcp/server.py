"""MCP server: unofficial read-only access to Germany's national
open-data portal govdata.de via its official CKAN API. No key, no
login."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from . import domain as _dom
from . import http as _http

INSTRUCTIONS = """\
Unofficial read-only MCP server for Germany's national open-data \
portal govdata.de via its official CKAN API (no key, no login): \
search 163,000+ datasets, full dataset details, publishing \
organisations, most recently updated datasets and resource details. \
Built by Mohammad Abbasi (mohammad-abbasi-sh) — \
https://almanibama.ir · https://mabbasi.ir — Germany MCP factory.\
"""

_SOURCE = "govdata.de"
_DISCLAIMER = "Unofficial read-only data from the govdata.de CKAN API; verify on the site before acting on it."


def _envelope() -> dict:
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": _SOURCE,
        "disclaimer": _DISCLAIMER,
    }


def _ok(payload: dict) -> str:
    return json.dumps({**_envelope(), **payload}, ensure_ascii=False)


def _err(e: Exception) -> str:
    return _ok({"error": str(e)})


mcp = FastMCP("govdata-mcp", instructions=INSTRUCTIONS)


@mcp.tool()
def govdata_search_datasets(query: str, limit: int = 10,
                            sort: str = "relevance") -> str:
    """Search govdata.de datasets. query: keyword or phrase, e.g.
    "berlin". limit: 1..50 (default 10). sort: "relevance" or "recent"."""
    try:
        q = (query or "").strip()
        if not q:
            raise ValueError("query must not be empty")
        lim = _dom.validate_limit(limit)
        s = (sort or "relevance").strip().lower()
        if s not in ("relevance", "recent"):
            raise ValueError(f"unsupported sort: {sort!r} (relevance/recent)")
        parsed = _dom.parse_search(
            _http.fetch_text(_dom.search_url(q, lim, s)))
    except (_http.GovdataMcpError, ValueError) as e:
        return _err(e)
    return _ok({"query": q, "sort": s,
                "total_results": parsed["total_results"],
                "count": len(parsed["items"]), "items": parsed["items"]})


@mcp.tool()
def govdata_get_dataset(dataset_id: str) -> str:
    """Full details of one dataset. dataset_id: the dataset id (UUID)
    or name, e.g. "wohnatlas-berlin"."""
    try:
        did = (dataset_id or "").strip()
        if not did:
            raise ValueError("dataset_id must not be empty")
        out = _dom.parse_dataset(_http.fetch_text(_dom.dataset_url(did)))
    except (_http.GovdataMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def govdata_list_publishers(limit: int = 10) -> str:
    """Publishing organisations on govdata.de, most datasets first.
    limit: 1..50 (default 10)."""
    try:
        lim = _dom.validate_limit(limit)
        orgs = _dom.parse_publishers(
            _http.fetch_text(_dom.publishers_url(50)))
    except (_http.GovdataMcpError, ValueError) as e:
        return _err(e)
    return _ok({"total_results": len(orgs),
                "count": min(lim, len(orgs)), "items": orgs[:lim]})


@mcp.tool()
def govdata_recent_datasets(limit: int = 10) -> str:
    """Most recently updated datasets on govdata.de.
    limit: 1..50 (default 10)."""
    try:
        lim = _dom.validate_limit(limit)
        parsed = _dom.parse_search(
            _http.fetch_text(_dom.recent_url(lim)))
    except (_http.GovdataMcpError, ValueError) as e:
        return _err(e)
    return _ok({"total_results": parsed["total_results"],
                "count": len(parsed["items"]), "items": parsed["items"]})


@mcp.tool()
def govdata_get_resource(resource_id: str) -> str:
    """Details of one dataset resource (file/API download link).
    resource_id: the resource UUID, shown on dataset resources."""
    try:
        rid = (resource_id or "").strip()
        if not rid:
            raise ValueError("resource_id must not be empty")
        out = _dom.parse_resource(_http.fetch_text(_dom.resource_url(rid)))
    except (_http.GovdataMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def govdata_health() -> str:
    """Check whether govdata.de is reachable right now.

    Returns status ok (HTTP 200), blocked (HTTP 403/429 — bot wall or
    rate limit) or error, plus the HTTP status and the probed URL.
    One polite request; it does not fetch any listings."""
    return _ok(_http.health_check())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    sys.exit(main())
