"""Live tests — hit the real govdata.de CKAN API. Cautious: few requests.

Run:  pytest tests/test_live.py -v
Skip: pytest -m "not live"  (or set GOVDATA_SKIP_LIVE=1)
"""
import json
import os
import pathlib
import sys
import unittest

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from govdata_mcp import server as srv

pytestmark = pytest.mark.live
SKIP = os.environ.get("GOVDATA_SKIP_LIVE") == "1"


@pytest.mark.skipif(SKIP, reason="GOVDATA_SKIP_LIVE=1")
class TestLive(unittest.TestCase):
    def test_search_live(self):
        out = json.loads(srv.govdata_search_datasets("berlin", limit=2))
        self.assertNotIn("error", out)
        self.assertGreater(out["total_results"], 5000)
        print(f"\nLIVE search 'berlin': {out['total_results']} total")

    def test_dataset_live(self):
        out = json.loads(srv.govdata_get_dataset("wohnatlas-berlin"))
        self.assertNotIn("error", out)
        self.assertEqual(out["title"], "Wohnatlas Berlin")
        self.assertGreaterEqual(out["num_resources"], 1)

    def test_publishers_live(self):
        out = json.loads(srv.govdata_list_publishers(limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE publishers: {out['total_results']} — top: {out['items'][0]['title']}")

    def test_recent_live(self):
        out = json.loads(srv.govdata_recent_datasets(limit=2))
        self.assertNotIn("error", out)
        self.assertGreater(out["total_results"], 100000)

    def test_resource_live(self):
        out = json.loads(srv.govdata_get_resource(
            "a5a2390f-e22f-47b3-ad48-07ba155956de"))
        self.assertNotIn("error", out)
        self.assertEqual(out["format"], "HTML")

    def test_health_live(self):
        out = json.loads(srv.govdata_health())
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["http_status"], 200)
