#!/usr/bin/env python3
"""Add a video layer to the home-page hero (docs/index.html).

Inserts an autoplay/looping <video> behind the hero overlay, right after
the existing background image-slot. The video stays hidden until it can
play, so the photo remains the fallback until a video exists.

The page framework re-renders elements and drops inline style/handlers
from <video>, so positioning and playback are driven by the wiring code
injected into componentDidMount (marked with ketto-hero-video:start/end).

To use: drop a file at docs/assets/hero.mp4 (see AGENTS.md).
"""
import json

PATH = "docs/index.html"
ANCHOR = 'id="hero-nature-fishing"'
MOUNT = "componentDidMount() {"
MARK_START = "/* ketto-hero-video:start */"
MARK_END = "/* ketto-hero-video:end */"

VIDEO = (
    '\n    <video id="hero-video" src="assets/hero.mp4" '
    'preload="auto" aria-hidden="true"></video>'
)

WIRING = """/* ketto-hero-video:start */
    function wireHeroVideo(v) {
      if (v.dataset.wired) return;
      v.dataset.wired = '1';
      // The framework re-renders this element and drops its inline style,
      // so position it from here.
      v.style.position = 'absolute';
      v.style.top = '-6%';
      v.style.left = '0';
      v.style.width = '100%';
      v.style.height = '112%';
      v.style.objectFit = 'cover';
      v.style.display = 'none';
      v.muted = true;
      v.loop = true;
      v.playsInline = true;
      v.addEventListener('canplay', function () {
        v.style.display = 'block';
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
      });
      v.addEventListener('error', function () { v.style.display = 'none'; });
      if (v.readyState >= 3) {
        v.style.display = 'block';
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
      } else {
        try { v.load(); } catch (e) {}
      }
    }
    var heroVideoScan = function () {
      var v = document.getElementById('hero-video');
      if (v) wireHeroVideo(v);
    };
    heroVideoScan();
    if (!window.__kettoHeroVideoObserver) {
      window.__kettoHeroVideoObserver = new MutationObserver(heroVideoScan);
      window.__kettoHeroVideoObserver.observe(document.body, { childList: true, subtree: true });
    }
/* ketto-hero-video:end */
"""


def main() -> None:
    html = open(PATH, encoding="utf-8").read()
    ts = html.find('<script type="__bundler/template">')
    start = html.find(">", ts) + 1
    end = html.rfind("</script>")
    doc = json.loads(html[start:end].strip())

    # 1. Ensure the video element sits right after the hero image-slot.
    if 'id="hero-video"' not in doc:
        i = doc.find(ANCHOR)
        assert i != -1, "hero image-slot not found"
        slot_end = doc.find("</image-slot>", i)
        assert slot_end != -1, "image-slot close not found"
        slot_end += len("</image-slot>")
        doc = doc[:slot_end] + VIDEO + doc[slot_end:]

    # 2. Insert or refresh the wiring inside componentDidMount.
    if MARK_START in doc:
        a = doc.find(MARK_START)
        b = doc.find(MARK_END) + len(MARK_END)
        doc = doc[:a] + WIRING + doc[b:]
    else:
        m = doc.find(MOUNT)
        assert m != -1, "componentDidMount not found"
        insert_at = m + len(MOUNT)
        doc = doc[:insert_at] + "\n" + WIRING + doc[insert_at:]

    new_raw = json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")
    open(PATH, "w", encoding="utf-8").write(html[:start] + new_raw + html[end:])
    print("patched docs/index.html")


if __name__ == "__main__":
    main()
