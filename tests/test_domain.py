"""Offline tests — parse real captured govdata.de CKAN responses, no network."""
import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from govdata_mcp import domain as dom
from govdata_mcp import server as srv

FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def _read(name):
    return (FIX / name).read_text(encoding="utf-8")


class TestValidation(unittest.TestCase):
    def test_limit(self):
        self.assertEqual(dom.validate_limit(10), 10)
        with self.assertRaises(ValueError):
            dom.validate_limit(0)
        with self.assertRaises(ValueError):
            dom.validate_limit(51)


class TestFixtures(unittest.TestCase):
    def test_search_berlin(self):
        out = dom.parse_search(_read("search-berlin.json"))
        self.assertEqual(out["total_results"], 5563)
        self.assertEqual(len(out["items"]), 2)
        first = out["items"][0]
        self.assertEqual(first["name"], "wohnatlas-berlin")
        self.assertEqual(first["title"], "Wohnatlas Berlin")
        self.assertEqual(first["organization"], "GDI-DE")
        self.assertEqual(first["num_resources"], 11)
        self.assertEqual(len(first["resources"]), 10)

    def test_dataset(self):
        out = dom.parse_dataset(_read("dataset-wohnatlas-berlin.json"))
        self.assertEqual(out["name"], "wohnatlas-berlin")
        self.assertEqual(out["num_resources"], 11)
        self.assertTrue(out["notes"].startswith("Der Wohnatlas Berlin"))

    def test_publishers_sorted(self):
        orgs = dom.parse_publishers(_read("publishers.json"))
        self.assertEqual(len(orgs), 3)
        counts = [o["package_count"] for o in orgs]
        self.assertEqual(counts, sorted(counts, reverse=True))
        self.assertEqual(orgs[0]["name"], "berlin-open-data")
        self.assertEqual(orgs[0]["package_count"], 1000)

    def test_recent(self):
        out = dom.parse_search(_read("recent.json"))
        self.assertEqual(out["total_results"], 163247)
        self.assertEqual(len(out["items"]), 2)

    def test_resource(self):
        out = dom.parse_resource(_read("resource.json"))
        self.assertEqual(out["id"], "a5a2390f-e22f-47b3-ad48-07ba155956de")
        self.assertEqual(out["format"], "HTML")
        self.assertTrue(out["url"].startswith("https://gdi.berlin.de/"))

    def test_error_raises(self):
        with self.assertRaises(ValueError):
            dom.parse_search('{"success": false, "error": {"message": "Not found"}}')

    def test_bad_json(self):
        with self.assertRaises(ValueError):
            dom.parse_search("<html>nope</html>")


class TestServerOffline(unittest.TestCase):
    def test_search_mock(self):
        with mock.patch("govdata_mcp.http.fetch_text",
                        return_value=_read("search-berlin.json")):
            out = json.loads(srv.govdata_search_datasets("berlin", limit=2))
        self.assertEqual(out["total_results"], 5563)
        self.assertEqual(out["count"], 2)
        self.assertIn("fetched_at", out)
        self.assertEqual(out["source"], "govdata.de")

    def test_bad_sort(self):
        out = json.loads(srv.govdata_search_datasets("berlin", sort="weird"))
        self.assertIn("error", out)

    def test_empty_query(self):
        out = json.loads(srv.govdata_search_datasets("", limit=3))
        self.assertIn("error", out)

    def test_dataset_mock(self):
        with mock.patch("govdata_mcp.http.fetch_text",
                        return_value=_read("dataset-wohnatlas-berlin.json")):
            out = json.loads(srv.govdata_get_dataset("wohnatlas-berlin"))
        self.assertEqual(out["title"], "Wohnatlas Berlin")

    def test_resource_mock(self):
        with mock.patch("govdata_mcp.http.fetch_text",
                        return_value=_read("resource.json")):
            out = json.loads(srv.govdata_get_resource(
                "a5a2390f-e22f-47b3-ad48-07ba155956de"))
        self.assertEqual(out["format"], "HTML")


if __name__ == "__main__":
    unittest.main()
