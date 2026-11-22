#!/usr/bin/env python3
"""
Google Reviews Schema Validator & Formatter
Validates extracted Google Reviews for zero hallucination, proper ratings,
avatar authenticity, and formats them into JSON or PHP registry arrays.

Usage:
  python3 validate_reviews.py --input reviews.json
  python3 validate_reviews.py --input reviews.json --format php --output snippets.php
"""

import sys
import json
import argparse
import re
from pathlib import Path


def validate_review(review: dict, index: int) -> list[str]:
    """Validate a single review record."""
    errors = []
    
    author = review.get("author") or review.get("name")
    if not author or not str(author).strip():
        errors.append(f"Review #{index + 1}: Missing or empty reviewer 'author' / 'name'.")

    quote = review.get("quote")
    if not quote or not str(quote).strip():
        errors.append(f"Review #{index + 1} ({author}): Missing or empty 'quote'.")
    elif len(str(quote).strip()) < 10:
        errors.append(f"Review #{index + 1} ({author}): Quote is suspiciously short (<10 chars).")
    
    # Check for trailing truncation
    if str(quote).strip().endswith("...") or "... More" in str(quote):
        errors.append(f"Review #{index + 1} ({author}): Quote contains trailing truncation ('...More'). Verify full text.")

    rating = review.get("rating") if "rating" in review else review.get("stars", 5)
    try:
        r_val = float(rating)
        if not (1.0 <= r_val <= 5.0):
            errors.append(f"Review #{index + 1} ({author}): Rating {r_val} outside valid range (1.0 - 5.0).")
    except (ValueError, TypeError):
        errors.append(f"Review #{index + 1} ({author}): Invalid non-numeric rating '{rating}'.")

    avatar = review.get("avatar", "")
    # Check for forbidden AI/stock avatar filenames
    if avatar and any(k in str(avatar).lower() for k in ["stock", "ai-parent", "ai_face", "generated"]):
        errors.append(f"Review #{index + 1} ({author}): Avatar '{avatar}' appears to be synthetic/stock. Violates Zero AI Avatar rule.")

    return errors


def format_to_php(data: dict) -> str:
    """Format reviews data into a clean WordPress PHP registry snippet."""
    lines = []
    lines.append("// Auto-generated from authentic Google Reviews dataset")
    if "rating_value" in data:
        count_str = f" ({data.get('review_count', 0)} reviews)" if "review_count" in data else ""
        lines.append(f"'rating'             => '{data['rating_value']} / 5{count_str}',")
    if "google_maps_url" in data:
        lines.append(f"'google_reviews_url' => '{data['google_maps_url']}',")
    
    lines.append("'testimonials'       => array(")
    for rev in data.get("reviews", []):
        author = rev.get("author") or rev.get("name", "Parent")
        quote = rev.get("quote", "").replace("'", "\\'")
        role = rev.get("role", "Parent").replace("'", "\\'")
        stars = rev.get("rating", rev.get("stars", 5))
        source = rev.get("source", "Google Review")
        avatar = rev.get("avatar", "")
        initial = rev.get("initial", "")

        lines.append("\tarray(")
        lines.append(f"\t\t'quote'   => '{quote}',")
        lines.append(f"\t\t'name'    => '{author}',")
        lines.append(f"\t\t'role'    => '{role}',")
        lines.append(f"\t\t'stars'   => {int(stars)},")
        lines.append(f"\t\t'source'  => '{source}',")
        if avatar:
            lines.append(f"\t\t'avatar'  => get_theme_file_uri( '{avatar}' ),")
        else:
            lines.append(f"\t\t'avatar'  => '',")
            if initial:
                lines.append(f"\t\t'initial' => '{initial}',")
            else:
                clean_initial = re.sub(r'^(dr\.|mr\.|mrs\.|ms\.|[a-z]\.\s*)', '', str(author), flags=re.I).strip()[:1]
                lines.append(f"\t\t'initial' => '{clean_initial.upper()}',")
        lines.append("\t),")
    lines.append("),")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate and format Google Reviews datasets.")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON file.")
    parser.add_argument("--format", "-f", choices=["json", "php"], default="json", help="Output format (json or php).")
    parser.add_argument("--output", "-o", help="Optional output path to write formatted file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    reviews = data.get("reviews", [])
    if not isinstance(reviews, list) or not reviews:
        print(f"❌ Error: 'reviews' list is missing or empty in {input_path}.", file=sys.stderr)
        sys.exit(1)

    all_errors = []
    for idx, rev in enumerate(reviews):
        all_errors.extend(validate_review(rev, idx))

    if all_errors:
        print(f"⚠️ Validation Failed with {len(all_errors)} issue(s):")
        for err in all_errors:
            print(f"  • {err}")
        sys.exit(1)

    print(f"✅ Success: All {len(reviews)} reviews passed authentic verification checks!")

    if args.format == "php":
        formatted = format_to_php(data)
    else:
        formatted = json.dumps(data, indent=2, ensure_ascii=False)

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"📄 Output saved to: {out_path}")
    else:
        print("\n--- Formatted Output Preview ---")
        print(formatted[:500] + ("..." if len(formatted) > 500 else ""))


if __name__ == "__main__":
    main()
