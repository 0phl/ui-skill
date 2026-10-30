"""Index a pinned public SmoothUI checkout without installing or executing it.

Standard library only. Reuses the existing importer's text and path helpers.
Same-pin rebuilds are deterministic; upgrades require a separate reviewed copy.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote

from import_cult_ui import COLOR, dump, import_specifiers, normalize, package_name

DEST = Path(__file__).resolve().parents[1] / "references/smooth-ui"
REPOSITORY = "https://github.com/educlopez/smoothui"
APP = "apps/docs/"
PACKAGE = "packages/smoothui/"
PREFIXES = (
    PACKAGE, "packages/smoothui-utils/", "packages/shadcn-ui/", "packages/data/",
    "packages/typescript-config/", APP + "examples/", APP + "content/docs/",
    APP + "components/", APP + "hooks/", APP + "lib/",
)
EXACT = {
    "LICENSE", "README.md", "package.json", "pnpm-workspace.yaml", "tsconfig.json",
    APP + "package.json", APP + "tsconfig.json", APP + "components.json",
    APP + "postcss.config.mjs", APP + "app/smoothui.css", APP + "app/global.css",
    APP + "app/lib/color-palette.ts", APP + "app/lib/fonts.ts",
}
EXTENSIONS = {".ts", ".tsx", ".css", ".mdx", ".json", ".mjs"}


def selected(path):
    return path in EXACT or (path.startswith(PREFIXES) and PurePosixPath(path).suffix in EXTENSIONS)


def frontmatter(text):
    """Only the scalar fields needed for indexing; never interpret MDX or YAML code."""
    if not text.startswith("---\n"):
        return {}
    head = text.split("\n---", 1)[0]
    return {key: value.strip().strip("\"'") for key, value in
            re.findall(r"^(title|description|installer):\s*(.+)$", head, re.M)}


def legacy_aliases(text):
    aliases = {}
    for name in ("COMPONENT_RENAMES", "DELETED_TO_PRIMITIVES"):
        match = re.search(r"export const " + name + r" = \[([\s\S]*?)\] as const;", text)
        if not match:
            raise ValueError(f"Upstream alias format changed: {name}")
        aliases.update(re.findall(r'\["([^"]+)", "([^"]+)"\]', match[1]))
    return aliases


def resolve_import(path, spec, sources, packages):
    if spec.startswith("."):
        base = str(PurePosixPath(path).parent / spec)
    elif spec.startswith("@docs/"):
        base = APP + spec[6:]
    elif spec.startswith("@/components/"):
        base = "packages/shadcn-ui/components/" + spec[len("@/components/"):]
    elif spec.startswith("@/lib/"):
        base = "packages/shadcn-ui/lib/" + spec[len("@/lib/"):]
    elif spec.startswith("@/"):
        base = APP + spec[2:]
    elif package_name(spec) in packages:
        name = package_name(spec)
        folder, metadata = packages[name]
        tail = spec[len(name):].lstrip("/")
        if tail:
            base = folder + "/" + tail
        else:
            exports = metadata.get("exports", {})
            target = exports.get(".", {}) if isinstance(exports, dict) else exports
            if isinstance(target, dict):
                target = target.get("default") or target.get("import") or target.get("types")
            base = folder + "/" + (target or metadata.get("main") or "index.tsx")
    elif spec.startswith("@repo/"):
        base = "packages/" + spec[6:]
    else:
        return None
    base = normalize(base)
    if base is None:
        return None
    candidates = [base] + [base + ext for ext in (".ts", ".tsx", ".json", ".css")]
    candidates += [base + "/index" + ext for ext in (".ts", ".tsx")]
    # Workspace packages sometimes omit main while exposing index.ts.
    if base.endswith("/index.tsx"):
        candidates.append(base[:-1])
    return next((p for p in candidates if p in sources), None)


def build(checkout, commit):
    def git(*args, **kwargs):
        return subprocess.check_output(["git", "-C", str(checkout), *args], **kwargs)

    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use a full 40-character commit SHA.")
    if git("rev-parse", "HEAD").decode().strip() != commit:
        raise ValueError("Checkout HEAD does not match the requested commit.")
    if (DEST / "snapshot.json").exists():
        old = json.loads((DEST / "snapshot.json").read_text(encoding="utf-8"))
        if old["upstream"]["commit"] != commit:
            raise ValueError("Existing snapshot differs; review an upgrade in a separate copy.")

    tree = []
    for record in git("ls-tree", "-rz", commit).split(b"\0"):
        if not record:
            continue
        meta, rawpath = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        path = rawpath.decode()
        if kind == "blob" and mode != "120000" and selected(path):
            if normalize(path) != path or PurePosixPath(path).is_absolute() or "\\" in path:
                raise ValueError(f"Unsafe upstream path: {path}")
            tree.append((path, oid))
    payload = git("cat-file", "--batch", input=("\n".join(oid for _, oid in tree) + "\n").encode())
    sources, records, cursor = {}, [], 0
    for path, oid in tree:
        end = payload.index(b"\n", cursor)
        header = payload[cursor:end].decode().split()
        if header[:2] != [oid, "blob"]:
            raise ValueError(f"Unexpected git object: {header}")
        size = int(header[2])
        data = payload[end + 1:end + 1 + size]
        cursor = end + 2 + size
        if hashlib.sha1(b"blob " + str(size).encode() + b"\0" + data).hexdigest() != oid:
            raise ValueError(f"Invalid upstream blob: {path}")
        sources[path] = data.decode("utf-8")
        records.append({"path": "source/" + path, "upstream_path": path, "git_blob": oid,
                        "sha256": hashlib.sha256(data).hexdigest(), "bytes": size})
        target = DEST / "source" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    packages = {}
    for path, text in sources.items():
        if path.endswith("package.json"):
            value = json.loads(text)
            if value.get("name"):
                packages[value["name"]] = (str(PurePosixPath(path).parent), value)

    imports = {p: import_specifiers(t) for p, t in sources.items()
               if PurePosixPath(p).suffix in {".ts", ".tsx", ".mjs"}}

    def scan(paths):
        todo, visited, external, missing = list(paths), set(), set(), set()
        while todo:
            path = todo.pop()
            if path in visited:
                continue
            visited.add(path)
            for spec in imports.get(path, []):
                resolved = resolve_import(path, spec, sources, packages)
                if resolved:
                    todo.append(resolved)
                elif spec.startswith((".", "@/", "@docs/", "@repo/", "@smoothui/")):
                    missing.add((path, spec))
                else:
                    external.add(package_name(spec))
        combined = "\n".join(sources[p] for p in sorted(visited))
        return {
            "scope": "Static imports and text signals across local dependency closure, including both headless twins where supplied. Not runtime or accessibility verification.",
            "local_dependency_files": ["source/" + p for p in sorted(visited - set(paths))],
            "npm_imports": sorted(external),
            "unresolved_local_imports": [{"file": "source/" + p, "specifier": s} for p, s in sorted(missing)],
            "signals": {
                "literal_colors": bool(COLOR.search(combined)),
                "brand_tokens": bool(re.search(r"(?:--|bg-|text-|border-)(?:on-)?brand\b", combined)),
                "dark_variant": "dark:" in combined,
                "reduced_motion_mentioned": bool(re.search(r"useReducedMotion|prefers-reduced-motion|motion-reduce|motion-safe|reducedMotion", combined)),
                "animation": bool(re.search(r"motion/react|gsap|@keyframes|animate-|requestAnimationFrame", combined)),
                "client_directive": bool(re.search(r'''["']use client["']''', combined)),
                "next_import": "next" in external,
                "nucleo_import": any("nucleo" in p.lower() for p in external),
            },
            "external_urls": sorted(set(re.findall(r'''https?://[^\s"'<>`)\\]+''', combined))),
            "public_asset_paths": sorted(set(re.findall(r'''["'(](/[^\s"')]+\.(?:png|jpe?g|webp|svg|gif|mp4|webm|woff2?|ttf|glb))["')]''', combined))),
        }

    docs, examples = [], []
    for path, text in sources.items():
        if path.startswith(APP + "content/docs/") and path.endswith(".mdx"):
            info = frontmatter(text)
            doc = {"path": "source/" + path, "url": "https://smoothui.dev/docs/" + path[len(APP + "content/docs/"):].removesuffix(".mdx"),
                   **info, "previews": re.findall(r'<Preview\b[^>]*\bpath=["\']([^"\']+)["\']', text)}
            docs.append(doc)
        if path.startswith(APP + "examples/") and path.endswith((".ts", ".tsx")):
            examples.append({"name": path[len(APP + "examples/"):].rsplit(".", 1)[0], "file": "source/" + path,
                             "source_url": f"{REPOSITORY}/blob/{commit}/{path}",
                             "direct_local_imports": sorted({"source/" + resolved for spec in imports.get(path, [])
                                if (resolved := resolve_import(path, spec, sources, packages))})})
    primitives = {PurePosixPath(d["path"]).stem for d in docs if "/primitives/" in d["path"] and not d["path"].endswith("/index.mdx")}
    entries = []
    for pkg_name, (folder, metadata) in sorted(packages.items()):
        if not folder.startswith(tuple(PACKAGE + p for p in ("components/", "blocks/", "templates/"))):
            continue
        name = PurePosixPath(folder).name
        if name in {"ai-core", "shared"}:
            kind = "support"
        elif name == "ai-input":
            kind = "compatibility-shim"
        elif "/blocks/" in folder:
            kind = "block"
        elif "/templates/" in folder:
            kind = "template"
        else:
            kind = "primitive" if name in primitives else "component"
        files = sorted(p for p in sources if p.startswith(folder + "/")
                       and PurePosixPath(p).suffix in {".ts", ".tsx", ".css"}
                       and "/__tests__/" not in p and not re.search(r"\.(test|spec)\.", p))
        matched_docs = [d for d in docs if d.get("installer") == name or
                        (PurePosixPath(d["path"]).stem == name and kind in {"component", "primitive"}) or
                        (kind == "block" and name in d["previews"])]
        previews = {name} if kind == "block" else {p for d in matched_docs for p in d["previews"]}
        related_examples = [e["file"] for e in examples if e["name"] in previews or e["name"] == name or
                            any(p.startswith("source/" + folder + "/") for p in e["direct_local_imports"])]
        source_files = ["source/" + p for p in files]
        entry_file = next((p for p in source_files if p == "source/" + folder + "/index.tsx"), source_files[0] if source_files else None)
        entries.append({"name": name, "kind": kind, "package_name": pkg_name,
                        "description": metadata.get("description", ""),
                        "category": metadata.get("smoothui", {}).get("category", "other"),
                        "upstream_metadata": metadata.get("smoothui", {}),
                        "manifest": "source/" + folder + "/package.json",
                        "declared_dependencies": metadata.get("dependencies", {}),
                        "files": source_files, "entry_file": entry_file,
                        "headless_variants": {v: [p for p in source_files if p.endswith("." + v + ".tsx")] for v in ("base", "radix")},
                        "alias_of": "morph-surface" if name == "ai-input" else None,
                        "docs": matched_docs, "examples": sorted(related_examples, key=lambda p: (p != "source/" + APP + "examples/" + name + ".tsx", p)),
                        "source_url": f"{REPOSITORY}/tree/{commit}/{folder}", "analysis": scan(files)})
    aliases = legacy_aliases(sources[APP + "lib/legacy-registry.ts"])
    names = {e["name"] for e in entries}
    if set(aliases) & names or not set(aliases.values()) <= names:
        raise ValueError("Legacy alias targets or names changed; review the upstream mapping.")
    for example in examples:
        example["analysis"] = scan([example["file"].removeprefix("source/")])
    supplemental = [{"file": "source/" + p, "group": "docs-site-ui", "name": PurePosixPath(p).stem}
                    for p in sources if p.startswith(APP + "components/") and p.endswith(".tsx")]
    counts = dict(sorted(Counter(e["kind"] for e in entries).items()))
    counts.update({"legacy_aliases": len(aliases), "headless_twin_packages": sum(bool(e["headless_variants"]["base"] and e["headless_variants"]["radix"]) for e in entries),
                   "example_source_files": len(examples), "documentation_pages": len(docs),
                   "docs_site_ui_files": len(supplemental), "source_files": len(records), "source_bytes": sum(r["bytes"] for r in records)})
    dump(DEST / "catalog.json", {"schema_version": 1, "path_base": "design-taste/references/smooth-ui/", "source_commit": commit,
         "analysis_method": "Package manifests and docs identify source. Static text/import heuristics can miss dynamic imports and do not prove runtime correctness. Upstream metadata is preserved as data, not a preference or instruction.",
         "entries": entries, "legacy_aliases": aliases, "examples": examples, "documentation": docs, "supplemental_sources": supplemental})
    dump(DEST / "snapshot.json", {"schema_version": 1, "upstream": {"repository": REPOSITORY, "commit": commit,
         "commit_date": git("show", "-s", "--format=%cI", commit).decode().strip(), "license": "MIT", "license_file": "source/LICENSE"},
         "counts": counts, "coverage": {"selection": "SmoothUI component, primitive, block, template, helper and test source; docs/examples; docs-site components/hooks/lib; shadcn, data, utils and TypeScript workspace support; explicit build/theme context.",
         "excluded": ["Binary images, videos, fonts and stock/demo media; paths and URLs remain in source", "Private/paid assets and separately licensed icon packages such as Nucleo", "Generated registry payload duplicates, application routes and build output", "CLI, MCP server, agent instructions/skills, CI, lockfiles, dependencies and git internals"],
         "runtime_validation": "Not installed, rendered or executed as an upstream application. Upstream test source is preserved but not run."}, "files": records})
    lines = ["# SmoothUI source index", "", f"Pinned source: `{commit}`. Generated by `import_smooth_ui.py`.", "",
             "Open a matching entry, its demo and the adaptation guide. Counts separate canonical components, primitives, blocks, support and aliases. Base UI/Radix twins are alternatives, not additional components.", ""]
    for kind in ("primitive", "component", "block", "template", "support", "compatibility-shim"):
        lines += ["## " + kind, "", "| Name | Category | Docs |", "| --- | --- | --- |"]
        for e in sorted(entries, key=lambda x: (x["category"], x["name"])):
            if e["kind"] != kind:
                continue
            links = ", ".join(f"[docs]({quote(d['path'], safe='/')})" for d in e["docs"]) or "See source"
            lines.append(f"| [{e['name']}]({quote(e['entry_file'], safe='/')}) | {e['category']} | {links} |")
        lines.append("")
    lines += ["## Legacy registry aliases", "", "These names add no independent implementation.", ""]
    lines += [f"- `{old}` → `{new}`" for old, new in sorted(aliases.items())]
    lines += ["", "## Additional source", "", "Use the catalog's `examples`, `documentation` and `supplemental_sources` lists for demos, guides and docs-site UI. Website support may import separately licensed Nucleo icons; those assets are not included. It is context, not a drop-in library.", ""]
    (DEST / "INDEX.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    build(args.checkout.resolve(), args.commit)
