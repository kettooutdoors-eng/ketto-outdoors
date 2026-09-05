# Ketto Outdoors — Base44 Dev Environment

## What this is
A static HTML website (Ketto Outdoors fishing brand). Pages are self-contained "bundled" HTML files in `docs/` — each embeds all JS, CSS, and base64-encoded images. No backend, no build step, no package.json.

## How it runs
Served by nginx (alpine) via `docker-compose.base44.yml`. The `docs/` directory is bind-mounted read-only at nginx's web root. Port 3000 → nginx port 80.

## Editing
Edit files in `docs/` directly. Changes are served immediately by nginx (no rebuild needed), but call `reload_preview` to refresh the preview iframe since there's no live-reload dev server.

## Pages
- `index.html` — Home
- `shop.html` — Shop
- `blog.html` — Blog index
- `blog-*.html` — Blog posts
- `baitcaster.html`, `baithooks.html`, `deep-six.html`, `driftworm.html`, `spinning-combo.html` — Product pages
- `new-to-fishing.html` — Guide page

## External dependencies
Pages load React/ReactDOM from `unpkg.com` CDN at runtime. No secrets or API keys required.

## Verify
```bash
docker compose -f docker-compose.base44.yml up -d
curl -sf http://localhost:3000/  # should return HTML
```
