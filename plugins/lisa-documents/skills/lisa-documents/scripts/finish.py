#!/usr/bin/env python3
"""Turn a filled-in preset into a finished, self-contained document.

    python3 scripts/finish.py my-doc.html                # -> my-doc.final.html
    python3 scripts/finish.py my-doc.html -o out.html
    python3 scripts/finish.py my-doc.html --pdf          # also my-doc.final.pdf, if Chrome/Playwright is available

The preset's <!--FONTS-->...<!--/FONTS--> block (Google Fonts links, which
need internet and can't load Monaspace Krypton) is replaced with the bundled
fonts embedded as data, so the file looks the same offline, in email, and
when printed. Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import re
import subprocess
import sys
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

# (CSS family, file prefix, [(weight, style)])
KRYPTON = ("Monaspace Krypton", "monaspace-krypton")
PRESET_FONTS = {
    "field-order": [
        ("Big Shoulders Stencil Display", "big-shoulders-stencil-display", [(700, "normal"), (800, "normal")]),
        ("Courier Prime", "courier-prime", [(400, "normal"), (400, "italic"), (700, "normal")]),
    ],
    "report": [
        ("Raleway", "raleway", [(300, "normal"), (400, "normal"), (600, "normal"), (800, "normal")]),
        ("Lato", "lato", [(400, "normal"), (400, "italic"), (700, "normal"), (900, "normal")]),
        (*KRYPTON, [(400, "normal"), (800, "normal")]),
    ],
    "proof-sheet": [
        (*KRYPTON, [(300, "normal"), (400, "normal"), (800, "normal")]),
    ],
    "gallery": [
        # Variable font with optical sizes: hairlines sharpen as the type grows.
        ("Bodoni Moda", "bodoni-moda", [("var", "normal"), ("var", "italic")]),
        ("Hanken Grotesk", "hanken-grotesk", [(400, "normal"), (500, "normal"), (600, "normal")]),
    ],
    # Verdana, Georgia and Courier New come with the computer, as in 2002.
    "web-2002": [],
    "word-doc": [
        ("Carlito", "carlito", [(400, "normal"), (400, "italic"), (700, "normal"), (700, "italic")]),
    ],
}

FONTS_BLOCK = re.compile(r"<!--FONTS-->.*?<!--/FONTS-->", re.S)
PRESET_META = re.compile(r'<meta\s+name="preset"\s+content="([^"]+)"')


def font_faces(preset: str) -> str:
    rules = []
    for family, prefix, faces in PRESET_FONTS[preset]:
        for weight, style in faces:
            path = FONTS_DIR / f"{prefix}-{weight}-{style}.woff2"
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            css_weight = "400 900" if weight == "var" else weight
            rules.append(
                f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{css_weight};'
                f"font-display:block;src:url(data:font/woff2;base64,{data}) format(\"woff2\");}}"
            )
    return "<style>\n" + "\n".join(rules) + "\n</style>" if rules else ""


def find_chrome() -> str | None:
    for candidate in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    ):
        try:
            subprocess.run([candidate, "--version"], capture_output=True, check=True, timeout=20)
            return candidate
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def make_pdf(html: Path, pdf: Path) -> bool:
    try:  # Playwright waits for fonts; prefer it when installed.
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(html.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.emulate_media(media="print")
            page.pdf(path=str(pdf), print_background=True, prefer_css_page_size=True)
            browser.close()
        return True
    except Exception:
        pass
    chrome = find_chrome()
    if not chrome:
        return False
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", html.resolve().as_uri()],
        capture_output=True, timeout=120,
    )
    return pdf.exists()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--pdf", action="store_true", help="also save a PDF next to the HTML")
    args = ap.parse_args()

    html = args.input.read_text(encoding="utf-8")
    m = PRESET_META.search(html)
    if not m or m.group(1) not in PRESET_FONTS:
        sys.exit(f'No known <meta name="preset"> in {args.input} (expected one of: {", ".join(PRESET_FONTS)})')
    if not FONTS_BLOCK.search(html):
        sys.exit(f"{args.input} has no <!--FONTS--> block; copy it back from the preset.")

    out = args.output or args.input.with_name(args.input.stem.removesuffix(".final") + ".final.html")
    out.write_text(FONTS_BLOCK.sub(lambda _: font_faces(m.group(1)), html, count=1), encoding="utf-8")
    print(f"HTML: {out}")

    if args.pdf:
        pdf = out.with_suffix(".pdf")
        if make_pdf(out, pdf):
            print(f"PDF:  {pdf}")
        else:
            print("PDF:  skipped (no Chrome or Playwright here). Open the HTML in a browser and choose Print > Save as PDF.")


if __name__ == "__main__":
    main()
