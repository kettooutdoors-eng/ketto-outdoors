#!/usr/bin/env python3
"""Inject responsive-fit CSS into every bundled page in docs/.

Each docs/*.html is a self-contained bundle: the real page lives as a
JSON string inside <script type="__bundler/template">. This script
decodes that string, appends a responsive override stylesheet before the
last </style>, and re-encodes it safely (escaping "</" so the outer
<script> tag never closes prematurely).
"""
import glob
import json
import sys

RESPONSIVE_CSS = """
/* ═══ Ketto responsive fit — fluid containers on small screens ═══ */
html, body { overflow-x: hidden; }
[style*="display: grid"] > *, [style*="display:grid"] > * { min-width: 0; }
[style*="display: flex"] > *, [style*="display:flex"] > * { min-width: 0; }
image-slot { min-width: 0; }
image-slot img { max-width: 100%; }

@media (max-width: 760px) {
  [style*="repeat(3,"], [style*="repeat(4,"], [style*="repeat(2,"],
  [style*="minmax(300px,"],
  [style*="grid-template-columns: 1fr 1fr"], [style*="grid-template-columns:1fr 1fr"],
  [style*="grid-template-columns: 2fr 1fr"], [style*="grid-template-columns:2fr 1fr"],
  [style*="grid-template-columns: 1fr 2fr"], [style*="grid-template-columns:1fr 2fr"] {
    grid-template-columns: 1fr !important;
  }
  [style*="top: 50%; left: 50%"], [style*="top:50%;left:50%"] {
    flex-direction: column !important;
    width: calc(100% - 32px) !important;
    padding: 24px 20px !important;
    gap: 16px !important;
  }
  [style*="display: flex"], [style*="display:flex"] { flex-wrap: wrap; }
}
"""


def process(path: str) -> bool:
    html = open(path, encoding="utf-8").read()
    marker = '<script type="__bundler/template">'
    ts = html.find(marker)
    if ts == -1:
        print(f"  SKIP {path}: no template")
        return False
    start = html.find(">", ts) + 1
    end = html.rfind("</script>")
    raw = html[start:end].strip()

    doc = json.loads(raw)
    if "Ketto responsive fit" in doc:
        print(f"  SKIP {path}: already patched")
        return False

    idx = doc.rfind("</style>")
    if idx == -1:
        print(f"  SKIP {path}: no style block")
        return False
    doc = doc[:idx] + RESPONSIVE_CSS + doc[idx:]

    # Re-encode; escape "</" as "<\/" (valid JSON) so the serialized page
    # can never close the outer <script> tag early.
    new_raw = json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")
    open(path, "w", encoding="utf-8").write(html[:start] + new_raw + html[end:])
    return True


def main() -> None:
    files = sorted(glob.glob("docs/*.html"))
    if not files:
        sys.exit("no docs/*.html found — run from repo root")
    for f in files:
        ok = process(f)
        print(f"  {'PATCHED' if ok else 'skipped':8} {f}")


if __name__ == "__main__":
    main()
