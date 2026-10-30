"""Regression checks for retrieval, source provenance and scan limitations."""

import unittest

import cult_ui
import import_cult_ui


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = cult_ui.load()

    def test_snapshot_is_complete_and_byte_exact(self):
        result = cult_ui.verify()
        self.assertTrue(result["ok"], result["errors"])

    def test_alias_resolves_to_real_source_and_examples(self):
        result = cult_ui.detail(self.catalog, "animated-button")
        self.assertEqual(result["entry"]["name"], "halo-button")
        self.assertTrue(result["entry"]["files"])
        self.assertIn("halo-button-demo", [e["name"] for e in result["examples"]])

    def test_task_queries_and_category_filter(self):
        for query, expected in [("minimal card", "minimal-card"), ("side panel", "side-panel"),
                                ("halo button", "halo-button"), ("kanban board", "kanban-board")]:
            with self.subTest(query=query):
                self.assertEqual(cult_ui.search(self.catalog, query)[0]["name"], expected)
        cards = cult_ui.search(self.catalog, category="Cards", limit=200)
        self.assertTrue(cards)
        self.assertTrue(all(e["category"] == "Cards" for e in cards))
        self.assertEqual(cult_ui.search(self.catalog, "not-a-real-component-987"), [])

    def test_distinguishes_137_sources_from_17_aliases(self):
        self.assertEqual(len(cult_ui.search(self.catalog, limit=307)), 137)
        self.assertEqual(len(cult_ui.search(self.catalog, aliases=True, limit=307)), 154)
        self.assertEqual(len(cult_ui.search(self.catalog, kind="example", limit=307)), 136)

    def test_import_scan_ignores_embedded_samples_and_comments(self):
        text = '''import { A } from "@/ui/a"
// import B from "fake-comment"
/* import D from "fake-block" */
const sample = `import C from "fake-example"`
import { E } from "motion/react"
const imageUrl = "https://example.com/a.png"
'''
        self.assertEqual(import_cult_ui.import_specifiers(text), ["@/ui/a", "motion/react"])

    def test_resolver_handles_parent_paths_and_unknown_files(self):
        sources = {"apps/www/registry/default/ui/card.tsx": "", "apps/www/lib/utils.ts": ""}
        path = "apps/www/registry/default/example/card-demo.tsx"
        self.assertEqual(import_cult_ui.resolve_import(path, "../ui/card", sources), "apps/www/registry/default/ui/card.tsx")
        self.assertEqual(import_cult_ui.resolve_import(path, "@/lib/utils", sources), "apps/www/lib/utils.ts")
        self.assertIsNone(import_cult_ui.resolve_import(path, "./absent", sources))

    def test_known_mixed_theme_and_dependency_signals(self):
        halo = cult_ui.detail(self.catalog, "halo-button")["entry"]["analysis"]
        self.assertTrue(halo["signals"]["literal_colors"])
        self.assertTrue(halo["signals"]["semantic_color_tokens"])
        self.assertTrue(halo["signals"]["reduced_motion_mentioned"])
        self.assertIn("@base-ui/react", halo["npm_imports"])
        minimal = cult_ui.detail(self.catalog, "minimal-card")["entry"]["analysis"]
        self.assertTrue(minimal["signals"]["next_import"])
        # An import may be unused; the signal is not a portability verdict.


if __name__ == "__main__":
    unittest.main()
