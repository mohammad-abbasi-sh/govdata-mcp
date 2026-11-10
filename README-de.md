# govdata-mcp 🗃️

mcp-name: io.github.mohammad-abbasi-sh/govdata-mcp

Inoffizieller **nur lesender** MCP-Server für **[govdata.de](https://www.govdata.de)** — Deutschlands nationales Open-Data-Portal govdata.de über die offizielle CKAN-API: über 163.000 Datensätze durchsuchen, Datensatzdetails, Herausgeber, neueste Datensätze und Ressourcendetails. Kein Schlüssel, kein Login. Kein Schlüssel, keine Anmeldung.

> Gebaut von Mohammad Abbasi als Teil der "Germany MCP factory". Nicht mit govdata.de verbunden.

## Für KI-Agenten

Zur MCP-Client-Konfiguration hinzufügen (stdio):

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

Oder lokal starten: `python -m govdata_mcp.server` (benötigt `mcp<2`, `httpx`).

## Tools

| Tool | Beschreibung |
|------|-------------|
| `govdata_search_datasets` | Datensätze auf govdata.de suchen |
| `govdata_get_dataset` | Vollständige Details eines Datensatzes |
| `govdata_list_publishers` | Herausgeber, nach Datensatzzahl sortiert |
| `govdata_recent_datasets` | Zuletzt aktualisierte Datensätze |
| `govdata_get_resource` | Details einer Datensatz-Ressource |
| `govdata_health` | Erreichbarkeitsprüfung (ok / blocked / error) — eine höfliche Anfrage |

## Entwicklung

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## Lizenz

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
