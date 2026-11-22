#!/usr/bin/env python3
"""
FSE Theme & Block Architectural Validator
Ensures compliance with WordPress Core FSE, strict 8pt grid, Block API v3,
and zero inline layout styling.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

def validate_theme_json(theme_dir: Path) -> list:
    errors = []
    theme_json_path = theme_dir / "theme.json"
    if not theme_json_path.exists():
        errors.append("Missing theme.json in theme root.")
        return errors

    try:
        with open(theme_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON in theme.json: {e}")
        return errors

    version = data.get("version", 0)
    if version < 2:
        errors.append(f"theme.json version {version} is deprecated. Expected version 2 or 3.")

    # Spacing verification
    spacing = data.get("settings", {}).get("spacing", {})
    spacing_sizes = spacing.get("spacingSizes", [])
    if not spacing_sizes:
        errors.append("theme.json settings.spacing.spacingSizes is empty or missing.")
    else:
        for idx, item in enumerate(spacing_sizes):
            raw_size = item.get("size", "")
            match = re.match(r"^(\d+)px$", raw_size.strip())
            if not match:
                errors.append(f"Spacing token '{item.get('name', idx)}' size '{raw_size}' is not in px or invalid format.")
            else:
                px_val = int(match.group(1))
                if px_val % 8 != 0:
                    errors.append(f"Spacing token '{item.get('name', idx)}' ({raw_size}) violates the 8pt grid! (Must be divisible by 8)")

    return errors

def validate_blocks(theme_dir: Path) -> list:
    errors = []
    blocks_dir = theme_dir / "blocks"
    if not blocks_dir.is_dir():
        return errors

    for block_json_path in blocks_dir.glob("*/block.json"):
        block_slug = block_json_path.parent.name
        try:
            with open(block_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"Block '{block_slug}' has invalid block.json: {e}")
            continue

        api_version = data.get("apiVersion", 1)
        if api_version < 3:
            errors.append(f"Block '{block_slug}' uses apiVersion {api_version}. Expected apiVersion 3.")

        render_target = data.get("render")
        if not render_target:
            errors.append(f"Block '{block_slug}' missing 'render' declaration in block.json.")
        elif render_target.startswith("file:"):
            rel_file = render_target.replace("file:", "").lstrip("./")
            render_path = block_json_path.parent / rel_file
            if not render_path.exists():
                errors.append(f"Block '{block_slug}' render file not found: {render_path}")

    return errors

def validate_no_inline_layout(theme_dir: Path) -> list:
    errors = []
    forbidden_patterns = [
        (re.compile(r'style=[\'"][^\'"]*display\s*:\s*flex', re.IGNORECASE), "inline display: flex"),
        (re.compile(r'style=[\'"][^\'"]*display\s*:\s*grid', re.IGNORECASE), "inline display: grid"),
        (re.compile(r'style=[\'"][^\'"]*padding\s*:', re.IGNORECASE), "inline padding"),
        (re.compile(r'style=[\'"][^\'"]*margin\s*:', re.IGNORECASE), "inline margin"),
        (re.compile(r'style=[\'"][^\'"]*grid-template', re.IGNORECASE), "inline grid-template"),
    ]

    scan_dirs = [theme_dir / "blocks", theme_dir / "templates", theme_dir / "parts", theme_dir / "patterns"]
    for sdir in scan_dirs:
        if not sdir.is_dir():
            continue
        for file_path in sdir.rglob("*"):
            if file_path.suffix in [".php", ".html"]:
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    for pattern, label in forbidden_patterns:
                        if pattern.search(content):
                            rel = file_path.relative_to(theme_dir)
                            errors.append(f"Forbidden {label} found in {rel}")
                except Exception:
                    pass

    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate WordPress Core FSE & Block Theme Standards.")
    parser.add_argument("--theme-path", "-t", required=True, help="Absolute or relative path to the WordPress theme directory.")
    args = parser.parse_args()

    theme_dir = Path(args.theme_path).resolve()
    if not theme_dir.is_dir():
        print(f"❌ Error: Theme directory not found: {theme_dir}")
        sys.exit(1)

    print("=" * 70)
    print(f"🔍 Validating FSE Theme Standards: {theme_dir.name}")
    print("=" * 70)

    theme_errors = validate_theme_json(theme_dir)
    block_errors = validate_blocks(theme_dir)
    style_errors = validate_no_inline_layout(theme_dir)

    all_errors = theme_errors + block_errors + style_errors

    if theme_errors:
        print("\n❌ theme.json Violations:")
        for err in theme_errors:
            print(f"   • {err}")
    else:
        print("✅ theme.json and 8pt Spacing Scale: PASS")

    if block_errors:
        print("\n❌ Block API v3 Violations:")
        for err in block_errors:
            print(f"   • {err}")
    else:
        print("✅ Bespoke Blocks (API v3 & render.php): PASS")

    if style_errors:
        print("\n❌ Inline Layout Style Violations:")
        for err in style_errors:
            print(f"   • {err}")
    else:
        print("✅ Zero Inline Layout Styles: PASS")

    print("\n" + "=" * 70)
    if all_errors:
        print(f"FAILED: Found {len(all_errors)} architectural violation(s).")
        sys.exit(1)
    else:
        print("🎉 SUCCESS: Theme is 100% compliant with WordPress Core & FSE Standards!")
        sys.exit(0)

if __name__ == "__main__":
    main()
