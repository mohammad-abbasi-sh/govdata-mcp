# govdata-mcp 🗃️

mcp-name: io.github.mohammad-abbasi-sh/govdata-mcp

سرور MCP غیررسمی و **فقط‌خواندنی** برای **[govdata.de](https://www.govdata.de)** — پورتال ملی داده‌های باز آلمان govdata.de از طریق API رسمی CKAN: جست‌وجو در بیش از ۱۶۳٬۰۰۰ مجموعه‌داده، جزئیات مجموعه‌داده، ناشران، تازه‌ترین مجموعه‌داده‌ها و جزئیات منبع. بدون کلید، بدون ورود. بدون کلید، بدون ورود.

> ساختهٔ محمد عباسی، بخشی از «کارخانهٔ MCP آلمان». وابسته به govdata.de نیست.

## برای ایجنت‌های هوش مصنوعی

به پیکربندی MCP کلاینت اضافه کنید (stdio):

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

یا به‌صورت محلی اجرا کنید: `python -m govdata_mcp.server` (نیازمند `mcp<2` و `httpx`).

## ابزارها

| ابزار | توضیح |
|------|-------|
| `govdata_search_datasets` | جست‌وجوی مجموعه‌داده‌ها در govdata.de |
| `govdata_get_dataset` | جزئیات کامل یک مجموعه‌داده |
| `govdata_list_publishers` | ناشران، به ترتیب بیشترین مجموعه‌داده |
| `govdata_recent_datasets` | تازه‌ترین مجموعه‌داده‌های به‌روز شده |
| `govdata_get_resource` | جزئیات یک منبع مجموعه‌داده |
| `govdata_health` | بررسی دسترس‌پذیری (ok / blocked / error) — یک درخواست مؤدبانه |

## توسعه

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## لایسنس

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
