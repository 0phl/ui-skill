"""Search the registered visual and code collections without external packages.

Paths in output are relative to the skill root, also returned as an absolute path.
This is metadata search, not image similarity or a recommendation score.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def inside(root, path):
    result = (root / path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError("Path outside collection: " + str(path))
    return result


def collections(root=ROOT):
    return read_json(root / "references/collections.json")["collections"]


def records(root=ROOT, source=""):
    sources = collections(root)
    if source and source not in {c["id"] for c in sources}:
        raise ValueError("Unknown source: " + source)
    for collection in sources:
        if source and collection["id"] != source:
            continue
        data = read_json(inside(root, collection["catalog"]))
        base = inside(root, collection["path_base"])
        if collection["format"] == "images":
            for entry in data["references"]:
                yield {"id": collection["id"] + ":" + entry["id"], "source": collection["id"], "name": entry["id"],
                       "title": entry["title"], "kind": "image", "category": entry["visual_family"],
                       "description": " ".join(entry["tags"]) + " " + json.dumps(entry["observations"], ensure_ascii=False),
                       "files": [entry["image_path"]], "guide": collection["guide"], "role": collection["role"],
                       "evidence_status": entry.get("user_feedback", {}).get("overall", "unspecified"),
                       "detail": entry}
            for entry in data.get("implementation_feedback", []):
                yield {"id": collection["id"] + ":" + entry["id"], "source": collection["id"],
                       "name": entry["id"], "title": entry["title"], "kind": "feedback",
                       "category": entry["kind"],
                       "description": " ".join(entry["tags"]) + " " + json.dumps(entry["user_feedback"], ensure_ascii=False),
                       "files": [entry["analysis_path"]], "guide": collection["guide"], "role": collection["role"],
                       "evidence_status": entry["user_feedback"]["overall"], "detail": entry}
        elif collection["format"] == "entries":
            for entry in data["entries"]:
                if entry.get("alias_of") or entry["kind"] in {"example", "compatibility-shim", "support"}:
                    continue
                paths = entry.get("files") or [entry.get("file")]
                paths = [str(inside(base, p).relative_to(root.resolve())).replace("\\", "/") for p in paths if p]
                metadata = entry.get("upstream_metadata", {})
                yield {"id": collection["id"] + ":" + entry["name"], "source": collection["id"],
                       "name": entry["name"], "title": entry.get("title", entry["name"]),
                       "kind": entry["kind"], "category": entry.get("category", ""),
                       "description": entry.get("description", "") + " " + json.dumps(metadata, ensure_ascii=False),
                       "files": paths, "guide": collection["guide"], "role": collection["role"],
                       **{k: entry[k] for k in ("start_line", "end_line", "shared_preamble") if k in entry},
                       "detail": entry}
        else:
            raise ValueError("Unknown catalog format: " + collection["format"])


def normalized(value):
    return re.sub(r"[^\w]+", " ", value.casefold()).strip()


def search(query="", source="", kind="", limit=10, root=ROOT):
    tokens, ranked = normalized(query).split(), []
    for entry in records(root, source):
        if kind and entry["kind"] != kind:
            continue
        identity = normalized(entry["name"] + " " + entry["title"])
        body = normalized(identity + " " + entry["category"] + " " + entry["description"])
        if all(t in body for t in tokens):
            score = sum(4 for t in tokens if t in identity)
            if normalized(query) in {normalized(entry["name"]), normalized(entry["title"])}:
                score += 20
            ranked.append((score, entry))
    return [{k: v for k, v in entry.items() if k not in {"detail", "description"}}
            for _, entry in sorted(ranked, key=lambda x: (-x[0], x[1]["id"]))[:limit]]


def detail(identity, root=ROOT):
    if ":" not in identity:
        raise ValueError("Use a namespaced ID from search, for example images:B003-14.")
    source = identity.split(":", 1)[0]
    for entry in records(root, source):
        if entry["id"] == identity:
            # Collection-specific details retain original paths; make their base explicit.
            collection = next(c for c in collections(root) if c["id"] == source)
            return {**entry, "detail_path_base": str(inside(root, collection["path_base"]))}
    raise ValueError("Unknown ID (aliases use each collection's specialized lookup): " + identity)


def verify(source="", root=ROOT):
    errors, checked = [], 0
    sources = collections(root)
    if source and source not in {c["id"] for c in sources}:
        raise ValueError("Unknown source: " + source)
    for c in sources:
        if source and source != c["id"]:
            continue
        catalog = read_json(inside(root, c["catalog"]))
        if c["format"] == "images":
            expected = [{"path": e["image_path"], **e["file_metadata"]} for e in catalog["references"]]
            base = root
        else:
            manifest = read_json(inside(root, c["snapshot"]))
            expected, base = manifest["files"], inside(root, c["path_base"])
            if catalog["source_commit"] != manifest["upstream"]["commit"]:
                errors.append(c["id"] + ": catalog and snapshot commits differ")
            expected_paths = {e["path"] for e in expected}
            actual_paths = {p.relative_to(base).as_posix() for p in (base / "source").rglob("*") if p.is_file()}
            if actual_paths != expected_paths:
                errors.append(c["id"] + ": source file inventory differs from snapshot")
        for record in expected:
            path = inside(base, record["path"])
            if not path.is_file():
                errors.append("Missing: " + str(path))
                continue
            data = path.read_bytes()
            if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
                errors.append("Changed: " + str(path))
            if record.get("git_blob") and hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != record["git_blob"]:
                errors.append("Git blob mismatch: " + str(path))
            checked += 1
    for entry in records(root, source):
        for path in entry["files"] + [entry["guide"]]:
            if not inside(root, path).is_file():
                errors.append("Broken catalog path: " + path)
        if "start_line" in entry:
            path = inside(root, entry["files"][0])
            if path.is_file():
                lines = path.read_text(encoding="utf-8").splitlines()
                if not (1 <= entry["start_line"] <= entry["end_line"] <= len(lines)):
                    errors.append("Invalid line range: " + entry["id"])
                elif lines[entry["start_line"] - 1] != f"## {entry['detail']['number']}. {entry['title']}":
                    errors.append("Recipe heading differs: " + entry["id"])
    return {"ok": not errors, "files_checked": checked, "errors": errors,
            "scope": "Preservation and catalog paths; not runtime or visual verification."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("search")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--source", default="")
    find.add_argument("--kind", default="")
    find.add_argument("--limit", type=int, default=10)
    show = commands.add_parser("show")
    show.add_argument("id")
    commands.add_parser("sources")
    check = commands.add_parser("verify")
    check.add_argument("--source", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "search":
            if args.limit < 1:
                raise ValueError("limit must be positive")
            result = search(args.query, args.source, args.kind, args.limit)
        elif args.command == "show":
            result = detail(args.id)
        elif args.command == "sources":
            result = collections()
        else:
            result = verify(args.source)
        print(json.dumps({"skill_root": str(ROOT), "result": result}, indent=2, ensure_ascii=False))
        return 1 if args.command == "verify" and not result["ok"] else 0
    except (ValueError, OSError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
