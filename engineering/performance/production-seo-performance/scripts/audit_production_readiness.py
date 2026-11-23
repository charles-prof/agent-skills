#!/usr/bin/env python3
"""
audit_production_readiness.py — Production SEO & Web Performance Auditor
Verifies technical SEO health, staging noindex guards, font self-hosting,
and Core Web Vitals (CLS) media reservation.

Run:
  python3 scripts/audit_production_readiness.py --path /path/to/project
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Terminal formatting
PASS = '\033[92m✔\033[0m'
FAIL = '\033[91m✘\033[0m'
WARN = '\033[93m⚠\033[0m'
BOLD = '\033[1m'
RESET = '\033[0m'


class AuditContext:
    def __init__(self, root_path: Path, verbose: bool = False):
        self.root = root_path.resolve()
        self.verbose = verbose
        self.failures = []
        self.warnings = []
        self.passed_count = 0

    def record_check(self, label: str, passed: bool, detail: str = "", fatal: bool = True):
        if passed:
            self.passed_count += 1
            print(f"  {PASS}  {label}")
        else:
            marker = FAIL if fatal else WARN
            print(f"  {marker}  {label}")
            if detail:
                print(f"       {detail}")
            if fatal:
                self.failures.append(label)
            else:
                self.warnings.append(label)


def check_staging_guard(ctx: AuditContext):
    """Gate 1: Verify staging/dev environments have noindex/nofollow logic."""
    print(f"\n{BOLD}[1] Staging Environment Guard (Indexation Protection){RESET}")
    found_staging_guard = False

    search_exts = {".php", ".html", ".js", ".ts", ".py"}
    for root, _, files in os.walk(ctx.root):
        if any(part in root for part in [".git", "node_modules", "vendor"]):
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix in search_exts:
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    if "noindex" in content and ("staging" in content.lower() or "chithramaya_is_staging" in content or "is_staging" in content.lower()):
                        found_staging_guard = True
                        if ctx.verbose:
                            print(f"       Found staging guard in: {p.relative_to(ctx.root)}")
                        break
                except Exception:
                    pass
        if found_staging_guard:
            break

    ctx.record_check(
        "Priority-0 Staging Noindex Guard detected",
        found_staging_guard,
        detail="No staging noindex/nofollow check found. Non-production hosts must inject noindex meta tags.",
        fatal=True
    )


def check_font_leaks(ctx: AuditContext):
    """Gate 2: Verify zero third-party font CDN requests (Google Fonts, etc.)."""
    print(f"\n{BOLD}[2] Font Pipeline & Self-Hosting (Zero Third-Party Leaks){RESET}")
    font_cdn_patterns = [
        re.compile(r"fonts\.googleapis\.com", re.IGNORECASE),
        re.compile(r"fonts\.gstatic\.com", re.IGNORECASE),
        re.compile(r"use\.typekit\.net", re.IGNORECASE),
        re.compile(r"@import\s+url\([\'\"]?https?://", re.IGNORECASE)
    ]

    leaks = []
    text_exts = {".css", ".scss", ".php", ".html", ".js", ".ts"}

    for root, _, files in os.walk(ctx.root):
        if any(part in root for part in [".git", "node_modules", "vendor"]):
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix in text_exts:
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    for pattern in font_cdn_patterns:
                        match = pattern.search(content)
                        if match:
                            leaks.append(f"{p.relative_to(ctx.root)}: {match.group(0)}")
                            break
                except Exception:
                    pass

    ctx.record_check(
        "Zero external font CDN calls (100% self-hosted requirement)",
        len(leaks) == 0,
        detail=f"Detected external font leak(s):\n       " + "\n       ".join(leaks[:5]),
        fatal=True
    )


def check_local_woff2_fonts(ctx: AuditContext):
    """Gate 2 (Sub-check): Verify local .woff2 font assets exist."""
    woff2_files = list(ctx.root.glob("**/*.woff2"))
    has_local_fonts = len(woff2_files) > 0

    ctx.record_check(
        f"Local .woff2 font assets present ({len(woff2_files)} font files found)",
        has_local_fonts,
        detail="No local .woff2 files found in repository. Production fonts should be self-hosted.",
        fatal=False
    )


def check_schema_structured_data(ctx: AuditContext):
    """Gate 1 (Sub-check): Verify Schema.org Knowledge Graph structured data."""
    print(f"\n{BOLD}[3] Schema.org Structured Data & Entity Graph{RESET}")
    has_schema = False
    has_graph = False

    search_exts = {".php", ".html", ".js", ".ts", ".json"}
    for root, _, files in os.walk(ctx.root):
        if any(part in root for part in [".git", "node_modules", "vendor"]):
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix in search_exts:
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    if "schema.org" in content.lower():
                        has_schema = True
                        if "@graph" in content or "'@graph'" in content or '"@graph"' in content:
                            has_graph = True
                            break
                except Exception:
                    pass
        if has_graph:
            break

    ctx.record_check(
        "Schema.org structured data declarations present",
        has_schema,
        detail="No Schema.org structured data detected. Essential for rich search snippets.",
        fatal=True
    )
    ctx.record_check(
        "Interconnected Schema.org Knowledge Graph (@graph) implemented",
        has_graph,
        detail="Schema is not organized as an interconnected @graph array linking entities.",
        fatal=False
    )


def check_media_layout_stability(ctx: AuditContext):
    """Gate 3: Verify <img> elements declare dimensions to prevent CLS."""
    print(f"\n{BOLD}[4] Media Stability & Cumulative Layout Shift (CLS Guard){RESET}")
    missing_dims = []

    img_tag_pattern = re.compile(r"<img\s+([^>]+)>", re.IGNORECASE)
    search_exts = {".php", ".html"}

    for root, _, files in os.walk(ctx.root):
        if any(part in root for part in [".git", "node_modules", "vendor"]):
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix in search_exts:
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    for match in img_tag_pattern.finditer(content):
                        tag_attrs = match.group(1)
                        # Check for width and height or aspect-ratio
                        has_width = "width=" in tag_attrs.lower() or "width:" in tag_attrs.lower()
                        has_height = "height=" in tag_attrs.lower() or "height:" in tag_attrs.lower()
                        has_aspect = "aspect-ratio" in tag_attrs.lower()
                        has_alt = "alt=" in tag_attrs.lower()

                        if not ((has_width and has_height) or has_aspect):
                            missing_dims.append(f"{p.relative_to(ctx.root)}: <img {tag_attrs[:40]}...>")
                            if len(missing_dims) >= 5:
                                break
                except Exception:
                    pass
        if len(missing_dims) >= 5:
            break

    ctx.record_check(
        "Image elements reserve intrinsic dimensions / aspect-ratio (CLS < 0.1)",
        len(missing_dims) == 0,
        detail=f"Found image(s) lacking explicit width/height/aspect-ratio:\n       " + "\n       ".join(missing_dims),
        fatal=False
    )


def main():
    parser = argparse.ArgumentParser(description="Audit web project for Production SEO & Performance readiness.")
    parser.add_argument("--path", default=".", help="Path to project root directory (default: current directory)")
    parser.add_argument("--verbose", action="store_true", help="Print verbose scan details")
    args = parser.parse_args()

    project_path = Path(args.path)
    if not project_path.exists():
        print(f"Error: Path '{project_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"{BOLD}=== Production SEO & Performance Audit ==={RESET}")
    print(f"Target: {project_path.resolve()}\n")

    ctx = AuditContext(project_path, verbose=args.verbose)

    check_staging_guard(ctx)
    check_font_leaks(ctx)
    check_local_woff2_fonts(ctx)
    check_schema_structured_data(ctx)
    check_media_layout_stability(ctx)

    print(f"\n{BOLD}Audit Summary:{RESET}")
    print(f"  Passed Checks: {ctx.passed_count}")
    print(f"  Warnings:      {len(ctx.warnings)}")
    print(f"  Failures:      {len(ctx.failures)}")

    if ctx.failures:
        print(f"\n{FAIL} {BOLD}Audit FAILED: {len(ctx.failures)} fatal issue(s) must be resolved before release.{RESET}")
        sys.exit(1)
    else:
        print(f"\n{PASS} {BOLD}Audit PASSED: Project meets production SEO and performance standards.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
