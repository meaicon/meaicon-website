# Meaicon Website

This repository contains the static marketing website for Meaicon. The project is built with plain HTML, CSS, and JavaScript, and does not require a build step.

## Overview

- Static site with multi-page HTML structure
- No framework dependency required
- Designed for fast hosting on GitHub Pages, Netlify, Vercel, or any static host
- Assets are stored in the `assets/` folder, including branding, CSS, and JavaScript

## Project structure

```text
/workspaces/meaicon-website
├── index.html
├── about.html
├── solutions.html
├── industries.html
├── global-connectivity.html
├── partners.html
├── case-studies.html
├── contact.html
├── products.html
├── robots.txt
├── sitemap.xml
├── favicon.ico
├── favicon.svg
├── apple-touch-icon.png
├── README.md
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── brand/
│       └── meaicon/
└── .gitignore
```

## Quick start

Open the site directly in a browser, or run a local static server:

```bash
cd /workspaces/meaicon-website
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Update the repo from a zip

If you have a new site zip and want to replace the repo content in one fast step, run:

```bash
cd /workspaces/meaicon-website && \
rm -rf /tmp/meaicon-update && \
mkdir -p /tmp/meaicon-update && \
unzip -o "/path/to/your-site.zip" -d /tmp/meaicon-update && \
rsync -a --delete /tmp/meaicon-update/ ./
```

This updates the whole repository and removes old files that are no longer in the new package.

## Deployment

This site is intended for static hosting. Any of the following are suitable:

- GitHub Pages
- Netlify
- Vercel
- Any web host that supports static HTML files

Before deployment, verify that:

- all HTML pages load correctly
- all links resolve without 404s
- favicon and branding assets are present
- the site root renders correctly on desktop and mobile

## Notes

- This repo is intentionally lightweight and easy to manage.
- Keep the site stateless and static unless a new build system is explicitly added.
- If you update structure or asset paths, keep this README current.

## License

This project is for the Meaicon website and is intended for internal site management and deployment use unless otherwise specified by the owning organization.
- [ ] Run Lighthouse/PageSpeed Insights audit and address Core Web Vitals issues

## License

Proprietary — All rights reserved by Meaicon / Triqbit, unless otherwise specified.
