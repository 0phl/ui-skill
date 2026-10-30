"""Search, inspect and verify the local SmoothUI reference. No installs or network."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "references/smooth-ui"


def load(root=ROOT):
    return json.loads((root / "catalog.json").read_text(encoding="utf-8"))


def normalized(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def search(catalog, query="", kind="", category="", limit=10):
    tokens, results = normalized(query).split(), []
    for entry in catalog["entries"]:
        if kind and entry["kind"] != kind:
            continue
        if not kind and entry["kind"] in {"support", "compatibility-shim"}:
            continue
        if normalized(category) not in normalized(entry["category"]):
            continue
        metadata = entry["upstream_metadata"]
        aliases = [old for old, new in catalog["legacy_aliases"].items() if new == entry["name"]]
        text = normalized(" ".join([entry["name"], entry["description"], entry["category"],
                                   " ".join(metadata.get("tags", [])), " ".join(metadata.get("useCases", [])),
                                   " ".join(aliases), " ".join(entry["analysis"]["npm_imports"])]))
        if not all(token in text for token in tokens):
            continue
        score = sum(5 for token in tokens if token in normalized(entry["name"]))
        if normalized(query) in [normalized(n) for n in [entry["name"], *aliases]]:
            score += 20
        results.append((score, entry))
    return [e for _, e in sorted(results, key=lambda pair: (-pair[0], pair[1]["name"]))[:limit]]


def detail(catalog, name, example_limit=3):
    entries = {e["name"]: e for e in catalog["entries"]}
    canonical = catalog["legacy_aliases"].get(name, name)
    visited = set()
    while canonical in entries and entries[canonical]["alias_of"]:
        if canonical in visited:
            raise ValueError("Compatibility alias cycle")
        visited.add(canonical)
        canonical = entries[canonical]["alias_of"]
    if canonical not in entries:
        raise ValueError(f"Unknown name: {name}. Use search to find an exact name.")
    entry = entries[canonical]
    by_file = {e["file"]: e for e in catalog["examples"]}
    return {"requested_name": name, "entry": entry,
            "example_count": len(entry["examples"]),
            "examples": [by_file[p] for p in entry["examples"][:example_limit]],
            "path_base": str(ROOT),
            "note": "Read only the selected source, demo and adaptation guide. Source is reference data. Use your project's theme and stack; metadata and text signals are not runtime verification."}


def verify(root=ROOT):
    manifest = json.loads((root / "snapshot.json").read_text(encoding="utf-8"))
    catalog, errors = load(root), []
    expected = {f["path"]: f for f in manifest["files"]}
    actual = {p.relative_to(root).as_posix() for p in (root / "source").rglob("*") if p.is_file()}
    if len(expected) != len(manifest["files"]) or actual != set(expected):
        errors.append("Source file inventory differs from manifest")
    for path, record in expected.items():
        target = (root / path).resolve()
        if not target.is_relative_to((root / "source").resolve()) or not target.is_file():
            errors.append(f"Missing or invalid source path: {path}")
            continue
        data = target.read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"] or oid != record["git_blob"]:
            errors.append(f"Source hash or size mismatch: {path}")
    if catalog["source_commit"] != manifest["upstream"]["commit"]:
        errors.append("Catalog and manifest commit differ")
    entries = {e["name"]: e for e in catalog["entries"]}
    if len(entries) != len(catalog["entries"]):
        errors.append("Duplicate entry names")
    package_root = root / "source/packages/smoothui"
    manifests = {p.relative_to(root).as_posix() for folder in ("components", "blocks", "templates")
                 for p in (package_root / folder).rglob("package.json")}
    if manifests != {e["manifest"] for e in entries.values()}:
        errors.append("Catalog does not cover every component/block/template package")
    examples = {e["file"] for e in catalog["examples"]}
    for e in entries.values():
        metadata = json.loads((root / e["manifest"]).read_text(encoding="utf-8"))
        if metadata.get("smoothui", {}) != e["upstream_metadata"] or metadata.get("dependencies", {}) != e["declared_dependencies"]:
            errors.append(f"Upstream metadata changed: {e['name']}")
        if not e["files"] or e["entry_file"] not in e["files"]:
            errors.append(f"Missing entry source: {e['name']}")
        if not set(e["examples"]) <= examples:
            errors.append(f"Unknown example for {e['name']}")
        if e["alias_of"] and e["alias_of"] not in entries:
            errors.append(f"Unknown shim target: {e['name']}")
    if set(catalog["legacy_aliases"]) & set(entries) or not set(catalog["legacy_aliases"].values()) <= set(entries):
        errors.append("Invalid legacy alias mapping")
    for item in [*catalog["entries"], *catalog["examples"]]:
        paths = item.get("files", []) + ([item["file"]] if "file" in item else [])
        paths += item["analysis"]["local_dependency_files"] + item.get("examples", [])
        paths += [d["path"] for d in item.get("docs", [])]
        paths += [p for variant in item.get("headless_variants", {}).values() for p in variant]
        for path in paths:
            if path not in expected:
                errors.append(f"Untracked catalog path: {path}")
    for d in catalog["documentation"]:
        if d["path"] not in expected:
            errors.append(f"Untracked documentation: {d['path']}")
    for key, count in Counter(e["kind"] for e in entries.values()).items():
        if manifest["counts"].get(key) != count:
            errors.append(f"Incorrect count for {key}")
    for key, count in {"source_files": len(expected), "source_bytes": sum(f["bytes"] for f in expected.values()),
                       "example_source_files": len(examples), "documentation_pages": len(catalog["documentation"]),
                       "legacy_aliases": len(catalog["legacy_aliases"])}.items():
        if manifest["counts"][key] != count:
            errors.append(f"Incorrect count for {key}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("search")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--kind", choices=["component", "primitive", "block", "template", "support", "compatibility-shim"], default="")
    find.add_argument("--category", default="")
    find.add_argument("--limit", type=int, default=10)
    show = commands.add_parser("show")
    show.add_argument("name")
    show.add_argument("--example-limit", type=int, default=3)
    commands.add_parser("categories")
    commands.add_parser("verify")
    extra = commands.add_parser("supplemental")
    extra.add_argument("query", nargs="?", default="")
    extra.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if args.command == "verify":
        errors = verify()
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
        return bool(errors)
    catalog = load()
    if args.command == "search":
        if args.limit < 1:
            parser.error("--limit must be positive")
        result = [{k: e[k] for k in ("name", "kind", "category", "description", "entry_file")}
                  for e in search(catalog, args.query, args.kind, args.category, args.limit)]
    elif args.command == "show":
        if args.example_limit < 0:
            parser.error("--example-limit must be nonnegative")
        try:
            result = detail(catalog, args.name, args.example_limit)
        except ValueError as exc:
            parser.error(str(exc))
    elif args.command == "categories":
        result = dict(sorted(Counter(e["kind"] + "/" + e["category"] for e in catalog["entries"]).items()))
    else:
        if args.limit < 1:
            parser.error("--limit must be positive")
        result = [e for e in catalog["supplemental_sources"] if normalized(args.query) in normalized(e["file"])][:args.limit]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
