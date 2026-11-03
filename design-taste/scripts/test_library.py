"""Cross-collection retrieval, integrity failures and bounded MotionSites intake."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import import_motionsites as importer
import library


def temporary_workspace():
    # Keep writable fixtures in this checkout, including on restricted Windows hosts.
    parent = Path(__file__).resolve().parent
    temp = tempfile.TemporaryDirectory(prefix=".library-test-", dir=parent)
    if Path(temp.name).resolve().parent != parent:
        raise ValueError("Temporary fixture escaped the test directory")
    return temp


class LibraryTests(unittest.TestCase):
    def test_all_registered_snapshots_and_image_files_verify(self):
        report = library.verify()
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["files_checked"], 2832)

    def test_explicit_rejection_is_retrievable_and_distinct_from_approved_replacement(self):
        results = library.search("Ronan", source="images")
        self.assertIn("images:R001", {e["id"] for e in results})
        self.assertIn("images:B005-01", {e["id"] for e in results})
        rejected = library.detail("images:R001")
        self.assertEqual(rejected["kind"], "feedback")
        self.assertEqual(rejected["evidence_status"], "explicitly-rejected-entire-design")
        self.assertIsNone(rejected["detail"]["image_path"])
        self.assertTrue(all((library.ROOT / p).is_file() for p in rejected["files"]))
        self.assertEqual(library.detail("images:B005-01")["evidence_status"], "explicitly-approved-implementation")
        self.assertEqual(len(library.search("", source="images", kind="image", limit=100)), 69)

    def test_search_routes_images_components_and_recipes(self):
        self.assertIn("images:B003-05", [e["id"] for e in library.search("booking", source="images")])
        self.assertEqual(library.search("halo button", source="cult-ui")[0]["id"], "cult-ui:halo-button")
        self.assertEqual(library.search("button", source="smooth-ui", kind="primitive")[0]["id"], "smooth-ui:smooth-button")
        self.assertTrue(library.search("mobile menu", source="motionsites", kind="technique"))
        self.assertEqual(library.search("no-such-reference-zzq987"), [])

    def test_namespaced_ids_resolve_and_results_are_bounded(self):
        records = list(library.records())
        self.assertEqual(len(records), len({e["id"] for e in records}))
        for source, name in [("images", "B003-05"), ("cult-ui", "halo-button"),
                             ("smooth-ui", "smooth-button"), ("motionsites", "layout-and-ui-05")]:
            entry = library.detail(source + ":" + name)
            self.assertEqual(entry["source"], source)
            for path in entry["files"]:
                self.assertTrue((library.ROOT / path).is_file())
            self.assertTrue(Path(entry["detail_path_base"]).is_dir())
        results = library.search("", limit=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all("detail" not in e and "description" not in e for e in results))

    def test_invalid_identifiers_do_not_fall_back_to_all_sources(self):
        for identity in ("layout-and-ui-05", "unknown:any", "images:unknown"):
            with self.assertRaises(ValueError):
                library.detail(identity)
        with self.assertRaises(ValueError):
            library.search(source="unknown")
        with self.assertRaises(ValueError):
            library.verify(source="unknown")

    def test_aliases_and_helpers_do_not_inflate_discovery(self):
        entries = list(library.records())
        self.assertTrue(all(not e["detail"].get("alias_of") for e in entries))
        self.assertFalse({"example", "compatibility-shim", "support"} & {e["kind"] for e in entries})
        self.assertNotIn("smooth-ui:ai-core", {e["id"] for e in entries})
        self.assertNotIn("smooth-ui:shared", {e["id"] for e in entries})


class IntegrityFailureTests(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_workspace()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        base = self.root / "references/sample"
        (base / "source").mkdir(parents=True)
        (base / "README.md").write_text("Guide", encoding="utf-8")
        self.data = b"# Shared\n## 1. Recipe\nContent\n"
        (base / "source/recipe.md").write_bytes(self.data)
        self.write("references/collections.json", {"collections": [{
            "id": "sample", "format": "entries", "catalog": "references/sample/catalog.json",
            "snapshot": "references/sample/snapshot.json", "path_base": "references/sample",
            "guide": "references/sample/README.md", "role": "Test reference"}]})
        self.write("references/sample/catalog.json", {"source_commit": "pin", "entries": [{
            "name": "recipe", "kind": "technique", "title": "Recipe", "number": 1,
            "file": "source/recipe.md", "start_line": 2, "end_line": 3}]})
        self.write("references/sample/snapshot.json", {"upstream": {"commit": "pin"}, "files": [{
            "path": "source/recipe.md", "bytes": len(self.data), "sha256": hashlib.sha256(self.data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(self.data)).encode() + b"\0" + self.data).hexdigest()}]})

    def write(self, relative, value):
        (self.root / relative).write_text(json.dumps(value), encoding="utf-8")

    def test_detects_modified_missing_and_unlisted_source_files(self):
        self.assertTrue(library.verify(root=self.root)["ok"])
        source = self.root / "references/sample/source/recipe.md"
        source.write_bytes(b"wrong")
        errors = library.verify(root=self.root)["errors"]
        self.assertTrue(any("Changed:" in e for e in errors))
        self.assertTrue(any("Git blob mismatch:" in e for e in errors))
        source.unlink()
        self.assertTrue(any("Missing:" in e for e in library.verify(root=self.root)["errors"]))
        source.write_bytes(self.data)
        source.with_name("unlisted.txt").write_text("extra", encoding="utf-8")
        self.assertTrue(any("inventory differs" in e for e in library.verify(root=self.root)["errors"]))

    def test_detects_pin_drift_and_bad_recipe_ranges(self):
        self.write("references/sample/catalog.json", {"source_commit": "wrong", "entries": [{
            "name": "recipe", "kind": "technique", "title": "Recipe", "number": 1,
            "file": "source/recipe.md", "start_line": 2, "end_line": 100}]})
        errors = library.verify(root=self.root)["errors"]
        self.assertTrue(any("commits differ" in e for e in errors))
        self.assertTrue(any("Invalid line range" in e for e in errors))

    def test_rejects_paths_outside_collection(self):
        with self.assertRaises(ValueError):
            library.inside(self.root, "../outside")
        self.write("references/sample/catalog.json", {"entries": [{
            "name": "bad", "kind": "component", "file": "../outside"}]})
        with self.assertRaises(ValueError):
            list(library.records(self.root))


class MotionSitesImportTests(unittest.TestCase):
    def test_parser_ignores_fenced_fake_headings_and_keeps_section_boundaries(self):
        source = "# Preamble\n## 1. First\n```md\n## 99. Fake\n```\ntext\n## 2. Second\n~~~~md\n## 80. Fake\n~~~\n## 81. Still fenced\n~~~~\nend\n"
        sections = importer.numbered_sections(source)
        self.assertEqual([(e["number"], e["title"], e["start_line"], e["end_line"]) for e in sections],
                         [(1, "First", 2, 6), (2, "Second", 7, 13)])

    def test_archive_covers_all_allowed_files_and_excludes_restricted_collections(self):
        root = library.ROOT / "references/motionsites"
        manifest = library.read_json(root / "snapshot.json")
        self.assertEqual({f["upstream_path"] for f in manifest["files"]}, importer.ALLOWED)
        self.assertEqual(len(manifest["files"]), 20)
        self.assertEqual(manifest["upstream"]["commit"], importer.COMMIT)
        recipes = [e for e in library.records(source="motionsites") if e["kind"] == "technique"]
        self.assertEqual(len(recipes), 58)
        self.assertEqual({e["category"] for e in recipes}, set(importer.CATEGORIES))
        self.assertTrue(all(e["shared_preamble"]["end_line"] < e["start_line"] for e in recipes))
        for path in importer.ALLOWED:
            self.assertNotIn("/examples/", path)
            self.assertNotIn("/media/", path)
            self.assertNotEqual(path, "preview-media.jpg")
        self.assertTrue(any("/examples/" in e["upstream_path"] for e in manifest["excluded"]))
        self.assertTrue(any("/media/" in e["upstream_path"] for e in manifest["excluded"]))

    def test_rebuild_uses_exact_blobs_and_is_reproducible_without_upstream_execution(self):
        # Simulate Git from the shipped archive, so tests need no network/research checkout.
        source = library.ROOT / "references/motionsites/source"
        blobs = {p: (source / p).read_bytes() for p in importer.ALLOWED}
        excluded = importer.PREFIX + "examples/do-not-copy.md"
        blobs[excluded] = b"Restricted fixture; must not be copied."
        ids = {p: hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
               for p, data in blobs.items()}
        by_id = {ids[p]: data for p, data in blobs.items()}
        tree = b"".join(f"100644 blob {ids[p]}\t{p}\0".encode() for p in sorted(blobs))

        def fake_git(args):
            operation = args[3:]
            if operation == ["rev-parse", "HEAD"]:
                return importer.COMMIT.encode() + b"\n"
            if operation == ["ls-tree", "-rz", importer.COMMIT]:
                return tree
            if operation[:2] == ["cat-file", "blob"]:
                return by_id[operation[2]]
            raise AssertionError("Unexpected subprocess: " + repr(args))

        with temporary_workspace() as temp, patch.object(importer.subprocess, "check_output", side_effect=fake_git):
            dest = Path(temp) / "archive"
            report = importer.build(Path("unused"), dest)
            self.assertEqual(report["techniques"], 58)
            before = {p.relative_to(dest): p.read_bytes() for p in dest.rglob("*") if p.is_file()}
            importer.build(Path("unused"), dest)
            self.assertEqual(before, {p.relative_to(dest): p.read_bytes() for p in dest.rglob("*") if p.is_file()})
            self.assertFalse((dest / "source" / excluded).exists())
            for path in importer.ALLOWED:
                self.assertEqual((dest / "source" / path).read_bytes(), blobs[path])
            self.assertEqual(library.read_json(dest / "catalog.json"),
                             library.read_json(library.ROOT / "references/motionsites/catalog.json"))

    def test_unreviewed_commit_and_changed_license_fail_before_writing(self):
        with temporary_workspace() as temp:
            dest = Path(temp) / "archive"
            with patch.object(importer.subprocess, "check_output", return_value=b"other-pin\n"):
                with self.assertRaisesRegex(ValueError, "reviewed commit"):
                    importer.build(Path("unused"), dest)
            self.assertFalse(dest.exists())
            wrong_license_tree = b"100644 blob wrong-license\tLICENSE\0"
            with patch.object(importer.subprocess, "check_output", side_effect=[importer.COMMIT.encode(), wrong_license_tree]):
                with self.assertRaisesRegex(ValueError, "License changed"):
                    importer.build(Path("unused"), dest)
            self.assertFalse(dest.exists())


if __name__ == "__main__":
    unittest.main()
