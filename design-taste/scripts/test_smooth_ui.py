"""Regression checks for preservation, source mapping and small-context retrieval."""

import unittest

from import_smooth_ui import frontmatter, legacy_aliases, resolve_import, selected
from smooth_ui import ROOT, detail, load, search, verify


class SmoothUICorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load()
        cls.entries = {e["name"]: e for e in cls.catalog["entries"]}

    def test_snapshot_integrity_and_package_coverage(self):
        self.assertEqual(verify(), [])

    def test_legacy_names_resolve_to_canonical_source(self):
        for old, new in self.catalog["legacy_aliases"].items():
            self.assertEqual(detail(self.catalog, old, 0)["entry"]["name"], new)
        self.assertEqual(detail(self.catalog, "ai-input", 0)["entry"]["name"], "morph-surface")
        source = (ROOT / "source/apps/docs/lib/legacy-registry.ts").read_text(encoding="utf-8")
        self.assertEqual(legacy_aliases(source), self.catalog["legacy_aliases"])

    def test_duplicate_docs_and_twins_do_not_add_components(self):
        for name in ("breadcrumb", "pagination"):
            self.assertEqual(self.entries[name]["kind"], "primitive")
            self.assertEqual(len(self.entries[name]["docs"]), 2)
        twins = [e for e in self.entries.values() if all(e["headless_variants"].values())]
        self.assertEqual(len(twins), 26)
        self.assertEqual(self.entries["ai-core"]["kind"], "support")
        self.assertEqual(self.entries["shared"]["kind"], "support")

    def test_search_filters_and_old_names(self):
        self.assertEqual(search(self.catalog, "button", kind="primitive")[0]["name"], "smooth-button")
        self.assertEqual(search(self.catalog, "animated-input")[0]["name"], "float-input")
        self.assertTrue(all(e["kind"] == "block" for e in search(self.catalog, "pricing", kind="block")))
        self.assertEqual(search(self.catalog, "chat", kind="template")[0]["name"], "chat-template")
        self.assertEqual(search(self.catalog, "no-such-reference-123"), [])

    def test_main_demo_first_and_details_bounded(self):
        shown = detail(self.catalog, "smooth-button")
        self.assertGreater(shown["example_count"], len(shown["examples"]))
        self.assertEqual(len(shown["examples"]), 3)
        self.assertEqual(shown["examples"][0]["name"], "smooth-button")
        self.assertEqual(self.entries["cta-1"]["examples"], ["source/apps/docs/examples/cta-1.tsx"])
        self.assertEqual(detail(self.catalog, "chat-template", 0)["examples"], [])
        with self.assertRaises(ValueError):
            detail(self.catalog, "unknown")

    def test_relevant_static_imports_resolve(self):
        for entry in [*self.catalog["entries"], *self.catalog["examples"]]:
            self.assertEqual(entry["analysis"]["unresolved_local_imports"], [], entry["name"])
        chat = self.entries["chat-template"]["analysis"]["local_dependency_files"]
        self.assertIn("source/packages/smoothui/components/ai-prompt-input/index.tsx", chat)

    def test_import_alias_specificity_and_parent_paths(self):
        sources = {"packages/shadcn-ui/components/ui/button.tsx": "",
                   "packages/smoothui/components/dialog/index.tsx": "",
                   "apps/docs/examples/shared/demo.tsx": ""}
        self.assertEqual(resolve_import("apps/docs/examples/foo.tsx", "@/components/ui/button", sources, {}),
                         "packages/shadcn-ui/components/ui/button.tsx")
        self.assertEqual(resolve_import("apps/docs/examples/foo.tsx", "@repo/smoothui/components/dialog", sources, {}),
                         "packages/smoothui/components/dialog/index.tsx")
        self.assertEqual(resolve_import("apps/docs/examples/canvas/a.tsx", "../shared/demo", sources, {}),
                         "apps/docs/examples/shared/demo.tsx")
        self.assertIsNone(resolve_import("a.tsx", "../../outside", sources, {}))

    def test_selection_excludes_agents_media_and_tooling(self):
        for path in (".agents/skills/x/SKILL.md", "packages/cli/src/index.ts", "pnpm-lock.yaml",
                     "apps/docs/public/hero.webp", "apps/docs/app/api/route.ts"):
            self.assertFalse(selected(path), path)
        self.assertTrue(selected("packages/smoothui/components/smooth-button/index.tsx"))
        self.assertEqual(frontmatter('---\ntitle: "Button"\ninstaller: smooth-button\n---\n<Preview />'),
                         {"title": "Button", "installer": "smooth-button"})


if __name__ == "__main__":
    unittest.main()
