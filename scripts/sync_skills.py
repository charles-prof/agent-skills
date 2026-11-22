#!/usr/bin/env python3
"""
Sync Skills Script
Discovers canonical nested skills across the repository (e.g. cms/, workflow/, research/),
extracts their skill names from SKILL.md frontmatter, and mirrors them into a flat
skills/<skill-name>/ directory for universal compatibility with:
- npx skills add <user>/agent-skills --skill <name>
- agy plugin install
- gemini skills install --path skills
"""

import os
import sys
import shutil
import filecmp
import argparse
from pathlib import Path


def parse_skill_name(skill_md_path: Path) -> str:
    """Extract 'name:' from YAML frontmatter in SKILL.md."""
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.splitlines():
                    if line.strip().startswith("name:"):
                        return line.split("name:", 1)[1].strip()
    except Exception as e:
        print(f"⚠️ Error reading {skill_md_path}: {e}", file=sys.stderr)
    return skill_md_path.parent.name


def find_nested_skills(repo_root: Path) -> dict[str, Path]:
    """Find all canonical skills outside of skills/, .git, etc."""
    ignore_dirs = {"skills", ".git", "node_modules", ".github", "scripts"}
    skills_map = {}

    for root, dirs, files in os.walk(repo_root):
        rel_root = Path(root).relative_to(repo_root)
        if any(part in ignore_dirs for part in rel_root.parts):
            continue

        if "SKILL.md" in files:
            skill_dir = Path(root)
            skill_name = parse_skill_name(skill_dir / "SKILL.md")
            if skill_name in skills_map:
                print(f"⚠️ Warning: Duplicate skill name '{skill_name}' found at {skill_dir} and {skills_map[skill_name]}", file=sys.stderr)
            skills_map[skill_name] = skill_dir

    return skills_map


def dir_diff(src: Path, dst: Path) -> list[str]:
    """Recursively compare two directories and return list of differences."""
    diffs = []
    if not dst.exists():
        return [f"Target directory {dst} does not exist."]

    dcmp = filecmp.dircmp(src, dst)
    for name in dcmp.left_only:
        diffs.append(f"Missing in target: {dst / name}")
    for name in dcmp.right_only:
        diffs.append(f"Extra file in target: {dst / name}")
    for name in dcmp.diff_files:
        diffs.append(f"File contents differ: {src / name} != {dst / name}")

    for sub_dir in dcmp.common_dirs:
        diffs.extend(dir_diff(src / sub_dir, dst / sub_dir))

    return diffs


def main():
    parser = argparse.ArgumentParser(description="Synchronize nested skills into flat skills/ directory.")
    parser.add_argument("--check", action="store_true", help="Check for differences without modifying files (returns non-zero if out of sync).")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    skills_dir = repo_root / "skills"
    nested_skills = find_nested_skills(repo_root)

    print(f"🔍 Discovered {len(nested_skills)} canonical skill(s):")
    for name, path in nested_skills.items():
        print(f"  • {name} -> {path.relative_to(repo_root)}")

    if args.check:
        print("\n🧪 Verifying flat/nested synchronization...")
        has_errors = False
        if not skills_dir.exists():
            print("❌ skills/ directory is missing!", file=sys.stderr)
            sys.exit(1)

        # Check existing flat skills
        existing_targets = {p.name: p for p in skills_dir.iterdir() if p.is_dir()}
        for name, src_path in nested_skills.items():
            if name not in existing_targets:
                print(f"❌ Skill '{name}' is not mirrored in skills/{name}/", file=sys.stderr)
                has_errors = True
            else:
                diffs = dir_diff(src_path, existing_targets[name])
                if diffs:
                    print(f"❌ Skill '{name}' is out of sync:")
                    for d in diffs:
                        print(f"    - {d}")
                    has_errors = True

        for extra_name in set(existing_targets.keys()) - set(nested_skills.keys()):
            print(f"⚠️ Extra skill '{extra_name}' in skills/ that has no canonical nested source.")
            has_errors = True

        if has_errors:
            print("\n❌ Check failed: skills/ is out of sync with nested source directories. Run 'npm run sync' to resolve.", file=sys.stderr)
            sys.exit(1)
        else:
            print("\n✅ Verification passed: all flat skills are in perfect sync!")
            sys.exit(0)

    # Sync mode
    print("\n🔄 Synchronizing into skills/...")
    skills_dir.mkdir(exist_ok=True)

    # Clean removed skills
    for item in skills_dir.iterdir():
        if item.is_dir() and item.name not in nested_skills:
            print(f"  🗑️ Removing deprecated flat skill: {item.name}")
            shutil.rmtree(item)

    # Mirror each nested skill into skills/<name>
    for name, src_path in nested_skills.items():
        target_path = skills_dir / name
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(src_path, target_path)
        print(f"  ✅ Mirrored {name} -> skills/{name}/")

    print("\n🎉 Synchronization complete! All skills mirrored into skills/ for universal npx/cli access.")


if __name__ == "__main__":
    main()
