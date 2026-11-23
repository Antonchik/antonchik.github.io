# anton.antonchik.com

Developer site for Anton Antonchik's apps (NavCalc, Pilotiq): developer page, support and legal documents used by App Store / Google Play listings. Plain static HTML/CSS/JS, no build step.

## URLs for store listings

| App | Marketing / Support URL | Privacy Policy | Terms |
|---|---|---|---|
| NavCalc | https://anton.antonchik.com/navcalcapp_support/ | https://anton.antonchik.com/privacy/navcalc/ | — |
| Pilotiq | https://anton.antonchik.com/pilotiq_support/ | https://anton.antonchik.com/privacy/pilotiq/ | https://anton.antonchik.com/terms/pilotiq/ |

General: `/support/`, `/legal/`. Old `antonchik.github.io/...` links keep working (GitHub Pages mirror); `/pilotiq_tos/` redirects to `/terms/pilotiq/`. `app-ads.txt` stays at the root.

## Structure

```
index.html              developer home (live demos)
support/  legal/        support centre, documents index
*_support/              app pages (old URLs kept for store links)
privacy/<app>/  terms/pilotiq/
assets/site.css         styles
assets/site.js          small enhancements on every page
assets/live.js          home page demos: wind triangle, converter, sample quiz, ISA and pressure sliders
tools/build.py          generator: content and page templates
wrangler.jsonc          Cloudflare Workers config
```

## Editing

Texts, app data and legal documents live in `tools/build.py`. After changing it, run `python3 tools/build.py` — it rewrites the HTML pages in place — and commit the result. Styles and scripts in `assets/` are edited directly.

## Deploy

Hosted on **Cloudflare Workers** (static assets), like the antonchik.com hub. Config: `wrangler.jsonc`; files excluded from upload: `.assetsignore`.

1. Cloudflare → Workers & Pages → Create → Import a repository → `antonchik.github.io`, production branch `gh-pages`. Build command: none; deploy command: `npx wrangler deploy`.
2. Worker → Settings → Domains & Routes → Add → Custom domain `anton.antonchik.com` (DNS record and certificate are created automatically).
3. Cloudflare Email Routing: create `support@antonchik.com`, `navcalc@antonchik.com`, `pilotiq@antonchik.com` → forward to your inbox.

GitHub Pages keeps serving the same files at `antonchik.github.io` (no custom domain), so old store links keep working; canonical tags point to `anton.antonchik.com`.
