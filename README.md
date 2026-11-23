# anton.antonchik.com

Developer site for Anton Antonchik's apps (NavCalc, Pilotiq): developer page, support and legal documents used by App Store / Google Play listings. Plain static HTML/CSS/JS served by GitHub Pages (`.nojekyll`, no build step).

## URLs for store listings

| App | Marketing / Support URL | Privacy Policy | Terms |
|---|---|---|---|
| NavCalc | https://anton.antonchik.com/navcalcapp_support/ | https://anton.antonchik.com/privacy/navcalc/ | — |
| Pilotiq | https://anton.antonchik.com/pilotiq_support/ | https://anton.antonchik.com/privacy/pilotiq/ | https://anton.antonchik.com/terms/pilotiq/ |

General: `/support/`, `/legal/`. Old `antonchik.github.io/...` links redirect automatically once the custom domain is set; `/pilotiq_tos/` redirects to `/terms/pilotiq/`. `app-ads.txt` stays at the root.

## Structure

```
index.html              developer home
support/  legal/        support centre, documents index
*_support/              app pages (old URLs kept for store links)
privacy/<app>/  terms/pilotiq/
assets/                 site.css, site.js, favicon, og image
CNAME                   anton.antonchik.com
```

## Deploy

1. Cloudflare DNS for antonchik.com: `CNAME anton → antonchik.github.io`, proxy **off** (DNS only).
2. GitHub → repo Settings → Pages: source branch `gh-pages`, custom domain `anton.antonchik.com`, enable *Enforce HTTPS*.
3. Cloudflare Email Routing: create `support@antonchik.com`, `navcalc@antonchik.com`, `pilotiq@antonchik.com` → forward to your inbox.
