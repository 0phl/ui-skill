"""Preserve and index the MIT portion of the reviewed MotionSites skill.

Standard library only. Reads Git blobs, never runs upstream scripts. The exact
allowlist and license hash deliberately require review before a future upgrade.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

REPOSITORY = "https://github.com/Motionsites-AI/claude-skill"
COMMIT = "faa30d512e3973e58675c72101a7ef42ed37ae83"
LICENSE_BLOB = "a3d8ddfaa8798fbd4d12b91b10701e4da1124ac4"
PREFIX = "plugins/motionsites-web-builder/skills/motionsites-web-builder/"
DEST = Path(__file__).resolve().parents[1] / "references/motionsites"
CATEGORIES = ("3d-and-webgl", "depth-and-interaction", "layout-and-ui", "scroll",
              "surfaces-and-buttons", "type-and-text-motion", "video-and-media")
GUIDES = ("assets", "builders", "craft", "review", "spec-template")
ALLOWED = {"LICENSE", "README.md", ".gitignore", ".claude-plugin/marketplace.json",
           "plugins/motionsites-web-builder/.claude-plugin/plugin.json",
           PREFIX + "SKILL.md", PREFIX + "scripts/shoot.py",
           PREFIX + "references/techniques/INDEX.md"}
ALLOWED.update(PREFIX + "references/" + name + ".md" for name in GUIDES)
ALLOWED.update(PREFIX + "references/techniques/" + name + ".md" for name in CATEGORIES)


def numbered_sections(text):
    """Find real Markdown recipe headings, ignoring headings inside code fences."""
    lines, starts, fence = text.splitlines(), [], None
    for n, line in enumerate(lines, 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        heading = re.match(r"^## (\d+)\. (.+)$", line) if fence is None else None
        if heading:
            starts.append((n, int(heading[1]), heading[2]))
    return [{"start_line": n, "end_line": starts[i + 1][0] - 1 if i + 1 < len(starts) else len(lines),
             "number": number, "title": title}
            for i, (n, number, title) in enumerate(starts)]


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def build(checkout, dest=DEST):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(checkout), *args])
    if git("rev-parse", "HEAD").decode().strip() != COMMIT:
        raise ValueError("Checkout must match the reviewed commit: " + COMMIT)
    if (dest / "snapshot.json").exists():
        old = json.loads((dest / "snapshot.json").read_text(encoding="utf-8"))
        if old["upstream"]["commit"] != COMMIT:
            raise ValueError("Review upgrades in a separate copy; do not overwrite another pin.")
    tree = {}
    for record in git("ls-tree", "-rz", COMMIT).split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            if kind == "blob":
                tree[path.decode()] = (mode, oid)
    if tree.get("LICENSE", (None, None))[1] != LICENSE_BLOB:
        raise ValueError("License changed; review reuse scope first.")
    if not ALLOWED <= tree.keys():
        raise ValueError("Expected reusable resources missing.")
    sources, records, entries = {}, [], []
    for path in sorted(ALLOWED):
        mode, oid = tree[path]
        if mode not in {"100644", "100755"}:
            raise ValueError("Not a regular file: " + path)
        data = git("cat-file", "blob", oid)
        if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != oid:
            raise ValueError("Blob hash mismatch: " + path)
        sources[path] = data.decode("utf-8")
        records.append({"path": "source/" + path, "upstream_path": path, "git_blob": oid,
                        "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    # Read and validate all inputs before creating the archive.
    for category in CATEGORIES:
        path = PREFIX + "references/techniques/" + category + ".md"
        sections = numbered_sections(sources[path])
        for section in sections:
            entry = {"name": f"{category}-{section['number']:02d}", "kind": "technique",
                     "category": category, "file": "source/" + path, **section,
                     "shared_preamble": {"start_line": 1, "end_line": sections[0]["start_line"] - 1},
                     "source_url": f"{REPOSITORY}/blob/{COMMIT}/{path}#L{section['start_line']}",
                     "verification": "Source reference; recipe runtime and accessibility not independently verified."}
            entries.append(entry)
    for path, content in sources.items():
        if path in {PREFIX + "references/techniques/" + c + ".md" for c in CATEGORIES}:
            continue
        title = next((line[2:] for line in content.splitlines() if line.startswith("# ")), Path(path).name)
        entries.append({"name": path.removeprefix(PREFIX), "kind": "guide" if path.endswith(".md") else "support",
                        "title": title, "category": "workflow", "file": "source/" + path,
                        "source_url": f"{REPOSITORY}/blob/{COMMIT}/{path}"})
    if sum(e["kind"] == "technique" for e in entries) != 58:
        raise ValueError("Recipe inventory changed; review the parser and source.")
    dest.mkdir(parents=True, exist_ok=True)
    for record in records:
        target = dest / record["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(sources[record["upstream_path"]].encode("utf-8"))
    snapshot = {"schema_version": 1, "upstream": {"repository": REPOSITORY, "commit": COMMIT},
                "license": {"file": "source/LICENSE", "scope": "MIT instructions, references, scripts and packaging text only"},
                "file_count": len(records), "bytes": sum(r["bytes"] for r in records),
                "excluded": [{"upstream_path": p, "reason": "Restricted prompt/media collection; link upstream only"
                              if "/examples/" in p or "/media/" in p else "Preview artwork; not needed for code reuse"}
                             for p in sorted(tree.keys() - ALLOWED)], "files": records}
    catalog = {"schema_version": 1, "source_commit": COMMIT, "path_base": "references/motionsites",
               "analysis_method": "Numbered Markdown headings outside code fences; line ranges include recipes, not dependency closure.",
               "entries": entries}
    dump(dest / "snapshot.json", snapshot)
    dump(dest / "catalog.json", catalog)
    index = ["# MotionSites reusable resource index", "", "Read [adaptation and license scope](README.md) first. These are optional techniques, not global design rules.", "",
             "58 recipe sections in 7 files. Read each file's shared preamble and named cross-references alongside the selected section. Runtime claims are upstream claims.", ""]
    for category in (*CATEGORIES, "workflow"):
        index += ["## " + category, "", "| ID | Resource | Lines |", "| --- | --- | --- |"]
        for entry in entries:
            if entry["category"] == category:
                lines = f"{entry['start_line']}–{entry['end_line']}" if "start_line" in entry else "whole file"
                index.append(f"| `{entry['name']}` | [{entry['title'].replace('|', '/')}](<{entry['file']}>) | {lines} |")
        index.append("")
    (dest / "INDEX.md").write_text("\n".join(index), encoding="utf-8", newline="\n")
    return {"files": len(records), "techniques": 58, "bytes": snapshot["bytes"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.checkout)))
