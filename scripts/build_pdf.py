#!/usr/bin/env python3
"""
build_pdf.py — Render any purely-personal HTML artifact to PDF.

Usage:
    python3 scripts/build_pdf.py <input.html> <output.pdf> [--format A4|letter|auto]

Examples:
    python3 scripts/build_pdf.py examples/BUSINESS-BRAIN.rendered.html BUSINESS-BRAIN.pdf
    python3 scripts/build_pdf.py examples/BUSINESS-BRAIN.rendered.html BUSINESS-BRAIN.pdf --format auto

Formats:
    A4      — 595 × 842 pt, portrait, 0 margins (default for full Brain renders)
    letter  — 612 × 792 pt, portrait, 0 margins (US letter alternative)
    auto    — detect body/main content height and fit exactly (for single-section standalones)

Dependencies:
    pip install playwright
    playwright install chromium

This is PDF Export Method C from the Brain renderer spec. For in-browser export (Method A),
just hit Cmd+P in the rendered HTML and choose "Save as PDF".
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def render_to_pdf(html_path: str, pdf_path: str, paper_format: str = "A4") -> None:
    """Render an HTML file to PDF via headless Chromium."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: Playwright not installed.\n"
            "Install with:\n"
            "    pip install playwright\n"
            "    playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(2)

    html_abs = Path(html_path).resolve()
    if not html_abs.exists():
        print(f"ERROR: input file not found: {html_abs}", file=sys.stderr)
        sys.exit(1)

    pdf_abs = Path(pdf_path).resolve()
    pdf_abs.parent.mkdir(parents=True, exist_ok=True)

    html_url = html_abs.as_uri()
    print(f"→ Loading {html_abs.name} …")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(html_url, wait_until="networkidle")

            # Give Google Fonts an extra moment to paint on first load
            page.wait_for_timeout(600)

            pdf_opts = _pdf_options_for_format(paper_format, page)
            page.pdf(path=str(pdf_abs), **pdf_opts)
        finally:
            browser.close()

    size_kb = pdf_abs.stat().st_size // 1024
    print(f"✓ Wrote {pdf_abs.name} ({size_kb} KB)")


def _pdf_options_for_format(paper_format: str, page) -> dict:
    """Build the page.pdf() options dict for the requested format."""
    base = {
        "print_background": True,
        "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
    }

    fmt = paper_format.lower()

    if fmt == "a4":
        return {**base, "format": "A4"}

    if fmt == "letter":
        return {**base, "format": "Letter"}

    if fmt == "auto":
        # Detect the rendered main content box and size the PDF to match exactly.
        # Good for single-section renders from engine-output-builder (1080×1080,
        # 1080×1350, 1200×628, etc.)
        dims = page.evaluate(
            """() => {
                const el = document.querySelector('.frame, main, body');
                const rect = el.getBoundingClientRect();
                return { width: Math.ceil(rect.width), height: Math.ceil(rect.height) };
            }"""
        )
        return {
            **base,
            "width": f"{dims['width']}px",
            "height": f"{dims['height']}px",
        }

    raise ValueError(f"Unknown format: {paper_format}. Use A4, letter, or auto.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a purely-personal HTML artifact to PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run `python3 scripts/build_pdf.py --help` for details.",
    )
    parser.add_argument("input", help="Path to the HTML artifact to render.")
    parser.add_argument("output", help="Path for the output PDF.")
    parser.add_argument(
        "--format",
        default="A4",
        choices=["A4", "letter", "auto"],
        help="Paper format. A4 for full Brain renders, auto for single-section standalones.",
    )

    args = parser.parse_args()
    render_to_pdf(args.input, args.output, args.format)


if __name__ == "__main__":
    main()
