#!/usr/bin/env python3
"""
Template: SMACSS CSS Compiler & Font Leak Enforcer

Features:
1. Compiles modular CSS @imports into a single minified bundle.
2. Forbids external font CDN imports (@import url(http...)) to enforce 100% self-hosted local fonts.
3. Performs build-time responsive breakpoint token replacement.
"""

import os
import re
import sys

# Configuration
THEME_DIR = 'theme'
MAIN_CSS = os.path.join(THEME_DIR, 'style.css')
COMPILED_CSS = os.path.join(THEME_DIR, 'style.compiled.css')

# Responsive Breakpoint Tokens (Mobile-First)
BREAKPOINTS = {
    '$bp-mobile': '320px',
    '$bp-tablet': '768px',
    '$bp-laptop': '960px',
    '$bp-desktop': '1440px',
    # Fallback Desktop-First
    '$bp-desktop-max': '1439px',
    '$bp-laptop-max': '959px',
    '$bp-tablet-max': '767px',
    '$bp-mobile-max': '599px',
}


def minify_css(css_str: str) -> str:
    """Minify CSS by stripping comments and excessive whitespace."""
    css_str = re.sub(r'/\*.*?\*/', '', css_str, flags=re.DOTALL)
    css_str = re.sub(r'\s+', ' ', css_str)
    css_str = re.sub(r'\s*([\{\}\:\;\,])\s*', r'\1', css_str)
    return css_str.strip()


def build():
    if not os.path.exists(MAIN_CSS):
        print(f"Error: {MAIN_CSS} not found.")
        sys.exit(1)

    print(f"Building {COMPILED_CSS}...")
    with open(MAIN_CSS, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Theme Header comment
    header_match = re.search(r'/\*[\s\S]*?\*/', content)
    header = header_match.group(0) + '\n' if header_match else ''
    compiled_content = header

    # Find and resolve all @import url("...");
    imports = re.findall(r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\);', content)
    css_payload = ""

    for imp in imports:
        # Enforce 100% self-hosted local fonts rule
        if imp.startswith('http'):
            raise ValueError(
                f"Performance Violation: External import '{imp}' forbidden. "
                f"All fonts must be 100% self-hosted local .woff2 files."
            )

        file_path = os.path.join(THEME_DIR, imp)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as cf:
                css_payload += cf.read() + "\n"
        else:
            print(f"Warning: File not found {file_path}")

    # Substitute Breakpoint Tokens
    for token, value in sorted(BREAKPOINTS.items(), key=lambda x: len(x[0]), reverse=True):
        css_payload = css_payload.replace(token, value)

    # Minify
    minified = minify_css(css_payload)
    compiled_content += minified

    with open(COMPILED_CSS, 'w', encoding='utf-8') as f:
        f.write(compiled_content)

    print(f"Compilation complete! Wrote {len(minified)} bytes to {COMPILED_CSS}")


if __name__ == '__main__':
    build()
