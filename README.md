# govdata-mcp 🗃️

mcp-name: io.github.mohammad-abbasi-sh/govdata-mcp

Unofficial **read-only** MCP server for **[govdata.de](https://www.govdata.de)** — Germany's national open-data portal govdata.de via its official CKAN API: search 163,000+ datasets, dataset details, publishers, recent datasets and resource details. No key, no login. No key, no login.

> Built by Mohammad Abbasi as part of the "Germany MCP factory". Not affiliated with govdata.de.

## For AI agents

Add to your MCP client config (stdio):

```json
{
  "mcpServers": {
    "govdata": {
      "command": "uvx",
      "args": ["govdata-mcp==0.1.0"]
    }
  }
}
```

Or run locally: `python -m govdata_mcp.server` (needs `mcp<2`, `httpx`).

## Tools

| Tool | Description |
|------|-------------|
| `govdata_search_datasets` | Search govdata.de datasets — `query`, `limit` 1..50, `sort` (relevance/recent) |
| `govdata_get_dataset` | Full details of one dataset — `dataset_id` (id or name, e.g. "wohnatlas-berlin") |
| `govdata_list_publishers` | Publishing organisations on govdata.de, most datasets first — `limit` 1..50 |
| `govdata_recent_datasets` | Most recently updated datasets — `limit` 1..50 |
| `govdata_get_resource` | Details of one dataset resource (file/API link) — `resource_id` |
| `govdata_health` | Reachability probe (ok / blocked / error) — one polite request |

## Notes

- All data comes from the **govdata.de CKAN API** (free, no key, no login) — 163,247 datasets at last check.
- Competition note: pipeworx-io/mcp-govdata-de (★0, 2026-11-09) covers the same portal but only ships 2 tools (`list_organizations`, `list_groups`) behind a commercial gateway and has no dataset search; this server adds search, dataset/resource details, recency and tests.

Tests: 19/19 green (13 offline + 6 live, 2026-11-10).

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## License

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
