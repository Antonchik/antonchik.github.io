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
index.html              developer home
support/  legal/        support centre, documents index
*_support/              app pages (old URLs kept for store links)
privacy/<app>/  terms/pilotiq/
assets/                 site.css, site.js, favicon, og image
wrangler.jsonc          Cloudflare Workers config
```

## Deploy

Hosted on **Cloudflare Workers** (static assets), like the antonchik.com hub. Config: `wrangler.jsonc`; files excluded from upload: `.assetsignore`.

1. Cloudflare → Workers & Pages → Create → Import a repository → `antonchik.github.io`, production branch `gh-pages`. Build command: none; deploy command: `npx wrangler deploy`.
2. Worker → Settings → Domains & Routes → Add → Custom domain `anton.antonchik.com` (DNS record and certificate are created automatically).
3. Cloudflare Email Routing: create `support@antonchik.com`, `navcalc@antonchik.com`, `pilotiq@antonchik.com` → forward to your inbox.

GitHub Pages keeps serving the same files at `antonchik.github.io` (no custom domain), so old store links keep working; canonical tags point to `anton.antonchik.com`.
