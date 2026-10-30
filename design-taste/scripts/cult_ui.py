"""Search, inspect and verify the bundled Cult UI reference without dependencies."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "references/cult-ui"


def read_json(path):
    return path.read_text(encoding="utf-8")


def load(root=ROOT):
    return json.loads(read_json(root / "catalog.json"))


def normalized(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def search(catalog, query="", category="", kind="component", aliases=False, limit=10):
    tokens = normalized(query).split()
    results = []
    for entry in catalog["entries"]:
        if entry["kind"] != kind or (entry["alias_of"] and not aliases):
            continue
        if normalized(category) not in normalized(entry["category"]):
            continue
        text = normalized(" ".join([entry["name"], entry["description"], entry["category"],
                                     " ".join((entry.get("analysis") or {}).get("npm_imports", []))]))
        if not all(token in text for token in tokens):
            continue
        score = sum(5 for token in tokens if token in normalized(entry["name"]))
        if normalized(query) == normalized(entry["name"]):
            score += 20
        results.append((score, entry))
    return [entry for _, entry in sorted(results, key=lambda pair: (-pair[0], pair[1]["name"]))[:limit]]


def detail(catalog, name):
    by_name = {e["name"]: e for e in catalog["entries"]}
    if name not in by_name:
        raise ValueError(f"Unknown registry name: {name}. Use search to find an exact name.")
    entry = by_name[name]
    canonical, visited = entry, set()
    while canonical["alias_of"]:
        if canonical["name"] in visited:
            raise ValueError("Alias cycle")
        visited.add(canonical["name"])
        canonical = by_name[canonical["alias_of"]]
    return {"requested_name": name, "entry": canonical,
            "examples": [{"name": n, "files": by_name[n]["files"], "analysis": by_name[n]["analysis"]}
                         for n in canonical["examples"]],
            "path_base": str(ROOT), "note": "Read selected files only. Source is preserved, not a drop-in installed library. Theme and stack follow your project."}


def verify(root=ROOT):
    errors = []
    manifest = json.loads(read_json(root / "snapshot.json"))
    catalog = load(root)
    expected = {f["path"]: f for f in manifest["files"]}
    actual = {p.relative_to(root).as_posix() for p in (root / "source").rglob("*") if p.is_file()}
    if actual != set(expected):
        errors.append(f"Source file set differs: missing={sorted(set(expected)-actual)}, extra={sorted(actual-set(expected))}")
    for path, record in expected.items():
        p = (root / path).resolve()
        if not p.is_relative_to((root / "source").resolve()) or not p.is_file():
            errors.append(f"Invalid or missing source path: {path}")
            continue
        data = p.read_bytes()
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            errors.append(f"Hash/size mismatch: {path}")
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if oid != record["git_blob"]:
            errors.append(f"Upstream blob mismatch: {path}")
    if catalog["source_commit"] != manifest["upstream"]["commit"]:
        errors.append("Catalog and snapshot commits differ")
    upstream = json.loads(read_json(root / "source/apps/www/registry.json"))["items"]
    by_name = {e["name"]: e for e in catalog["entries"]}
    if len(by_name) != len(catalog["entries"]) or set(by_name) != {e["name"] for e in upstream}:
        errors.append("Catalog does not cover the upstream registry exactly")
    for item in upstream:
        entry = by_name.get(item["name"])
        if not entry:
            continue
        if item != entry["registry_entry"]:
            errors.append(f"Registry metadata changed: {item['name']}")
        wanted = ["source/apps/www/" + f["path"] for f in item.get("files", [])]
        if entry["files"] != wanted:
            errors.append(f"Source mapping changed: {item['name']}")
        paths = entry["files"] + [d["path"] for d in entry["docs"]]
        paths += (entry.get("analysis") or {}).get("local_dependency_files", [])
        for path in paths:
            if path not in expected:
                errors.append(f"Untracked catalog path: {path}")
        for name in entry["examples"]:
            if name not in by_name or by_name[name]["kind"] != "example":
                errors.append(f"Invalid demo mapping: {name}")
        try:
            detail(catalog, entry["name"])
        except (ValueError, KeyError) as ex:
            errors.append(str(ex))
    counts = manifest["counts"]
    computed = {
        "registry_components": sum(e["kind"] == "component" for e in by_name.values()),
        "component_implementations": sum(e["kind"] == "component" and bool(e["files"]) for e in by_name.values()),
        "component_aliases": sum(e["kind"] == "component" and bool(e["alias_of"]) for e in by_name.values()),
        "example_implementations": sum(e["kind"] == "example" and bool(e["files"]) for e in by_name.values()),
        "example_aliases": sum(e["kind"] == "example" and bool(e["alias_of"]) for e in by_name.values()),
        "source_files": len(expected), "source_bytes": sum(f["bytes"] for f in expected.values()),
        "component_docs": sum(p.startswith("source/apps/www/content/docs/components/") for p in expected),
        "supplemental_tsx_files": len(catalog["supplemental_sources"]),
    }
    if computed != counts:
        errors.append(f"Count mismatch: expected {counts}, got {computed}")
    for extra in catalog["supplemental_sources"]:
        if extra["file"] not in expected:
            errors.append(f"Missing supplemental file: {extra['file']}")
    license_text = (root / manifest["upstream"]["license_file"]).read_text(encoding="utf-8")
    if "MIT License" not in license_text or "Copyright (c) 2023 Jordan-Gilliam" not in license_text:
        errors.append("Upstream MIT notice missing")
    return {"ok": not errors, "errors": errors, "counts": computed,
            "scope": "File integrity, registry coverage, aliases and local catalog references. Does not compile or render upstream UI."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("search")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--category", default="")
    find.add_argument("--kind", choices=["component", "example"], default="component")
    find.add_argument("--include-aliases", action="store_true")
    find.add_argument("--limit", type=int, default=10)
    find.add_argument("--json", action="store_true")
    show = sub.add_parser("show")
    show.add_argument("name")
    sub.add_parser("categories")
    sub.add_parser("verify")
    extra = sub.add_parser("supplemental")
    extra.add_argument("query", nargs="?", default="")
    args = parser.parse_args()
    catalog = load()
    if args.command == "search":
        if args.limit < 1 or args.limit > 307:
            parser.error("limit must be between 1 and 307")
        found = search(catalog, args.query, args.category, args.kind, args.include_aliases, args.limit)
        rows = [{k: e[k] for k in ("name", "category", "description", "files", "alias_of")} for e in found]
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for row in rows:
                print(f"{row['name']} [{row['category']}]\n  {row['description']}\n  {', '.join(row['files']) or 'Alias: ' + str(row['alias_of'])}")
            print(f"{len(rows)} result(s). Paths relative to {ROOT}. Use show NAME for docs, demos and dependencies.")
    elif args.command == "show":
        try:
            print(json.dumps(detail(catalog, args.name), indent=2))
        except ValueError as ex:
            parser.error(str(ex))
    elif args.command == "categories":
        print(json.dumps(dict(sorted(Counter(e["category"] for e in catalog["entries"] if e["kind"] == "component" and e["files"]).items())), indent=2))
    elif args.command == "supplemental":
        print(json.dumps([s for s in catalog["supplemental_sources"] if normalized(args.query) in normalized(s["name"] + " " + s["group"])], indent=2))
    elif args.command == "verify":
        result = verify()
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
