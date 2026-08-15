# Meaicon Website

Official static website for **Meaicon**. This repository contains the full source for the marketing/corporate site — plain HTML, CSS, and vanilla JavaScript, with no build step required to view pages locally.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [Coding Standards](#coding-standards)
- [Branching & Commit Conventions](#branching--commit-conventions)
- [Deployment](#deployment)
- [Guidelines for AI Agents](#guidelines-for-ai-agents)
- [Roadmap / TODO](#roadmap--todo)
- [License](#license)

## Project Overview

This is a **static HTML website** (no framework, no server-side rendering). Pages are plain `.html` files linked together via relative paths, styled with CSS, and enhanced with minimal vanilla JS where necessary. The goal is a fast, dependency-free, easily maintainable site.

## Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Markup     | HTML5                                |
| Styling    | CSS3 (custom, no framework unless noted below) |
| Scripting  | Vanilla JavaScript (ES6+)            |
| Hosting    | GitHub Pages / static hosting (TBD)  |
| Build Tool | None required (pure static files)    |

If a CSS framework (e.g. Tailwind, Bootstrap) or bundler is introduced later, this section **must** be updated accordingly.

## Folder Structure

```
meaicon-website/
├── index.html              # Homepage
├── about.html              # About page
├── contact.html            # Contact page
├── /pages/                 # Additional inner pages (if any)
├── /assets/
│   ├── /css/               # Stylesheets (style.css, variables.css, etc.)
│   ├── /js/                # JavaScript files
│   ├── /images/            # Image assets (optimized, web-ready formats)
│   └── /fonts/             # Self-hosted fonts (if any)
├── /components/            # Reusable HTML snippets (header, footer) if using includes
├── README.md               # This file
└── .gitignore
```

> Note: Adjust this tree to match the actual structure as files are added. Keep it accurate — this is the single source of truth for navigating the repo.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/triqbit/meaicon-website.git
   cd meaicon-website
   ```
2. Open `index.html` directly in a browser, or serve locally for accurate relative-path/CORS behavior:
   ```bash
   npx serve .
   # or
   python3 -m http.server 8080
   ```
3. Visit `http://localhost:8080` (or the port shown).

No dependencies, no `npm install` required for the core site.

## Coding Standards

- **HTML**: Semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`). Every page must have proper `<title>`, `<meta charset>`, `<meta name="viewport">`, and `<meta name="description">` tags.
- **CSS**: Use a single consistent naming convention (BEM recommended: `.block__element--modifier`). Avoid inline styles. Keep shared variables (colors, spacing, fonts) in a `variables.css` or `:root` block.
- **JavaScript**: Vanilla ES6+, no inline `onclick` handlers. Keep scripts unobtrusive and placed at the end of `<body>` or loaded with `defer`.
- **Accessibility**: All images require `alt` text. Maintain proper heading hierarchy (`h1` → `h2` → `h3`). Ensure sufficient color contrast and keyboard navigability.
- **Performance**: Optimize/compress images before committing. Avoid unused CSS/JS. Minify assets before production deployment if a build step is added later.
- **SEO**: Every page needs unique `<title>` and meta description. Use Open Graph tags for social sharing where relevant.
- **Responsiveness**: Mobile-first CSS. Test at common breakpoints (360px, 768px, 1024px, 1440px).
- **Consistency**: Reuse existing components/classes before creating new ones. Do not duplicate CSS rules already defined elsewhere.

## Branching & Commit Conventions

- `main` — production-ready branch, always deployable.
- Feature branches: `feature/<short-description>`
- Fixes: `fix/<short-description>`
- Commits should follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat: add new pricing section`
  - `fix: correct broken nav link on mobile`
  - `style: adjust footer spacing`
  - `docs: update README structure`
  - `refactor: simplify hero section markup`

## Deployment

- The site is static and can be deployed to GitHub Pages, Netlify, Vercel, or any static host.
- Do not commit build artifacts unless a build step is formally introduced and documented here.
- Confirm all relative paths (`href`, `src`) work correctly relative to the deployed root before merging to `main`.

## Guidelines for AI Agents

This section exists so that any AI coding agent (e.g. Google Jules, Copilot, Claude, etc.) can work on this repo efficiently, consistently, and with minimal back-and-forth correction.

1. **Read this README first** before making any change. Do not assume framework usage — this is plain HTML/CSS/JS unless explicitly stated otherwise above.
2. **Preserve existing structure.** Do not introduce a new folder layout, CSS framework, or JS library without explicit instruction.
3. **Match existing patterns.** Before creating new components, styles, or scripts, check `/assets/css/` and `/assets/js/` for existing reusable code.
4. **No unrequested dependencies.** Do not add npm packages, CDNs, or build tools unless the task explicitly asks for it.
5. **Small, scoped changes.** Prefer minimal diffs that solve the stated task rather than broad refactors, unless refactoring is the explicit task.
6. **Update this README** whenever the folder structure, tech stack, or conventions change, so future agents/humans stay in sync.
7. **Validate before committing:**
   - HTML validates (no unclosed tags, correct nesting).
   - Links (internal/external) are not broken.
   - Pages render correctly at mobile and desktop widths.
8. **Commit messages** must follow the Conventional Commits format described above.
9. **Never remove content** (copy, sections, images) without explicit instruction — flag it instead of deleting.
10. **Ask/flag ambiguity** in a PR description or comment rather than guessing silently when requirements are unclear.

## Roadmap / TODO

- [ ] Finalize folder structure to match actual files in repo
- [ ] Add favicon and social preview (Open Graph) images
- [ ] Add sitemap.xml and robots.txt
- [ ] Set up GitHub Pages / hosting deployment
- [ ] Add basic HTML/CSS linting (e.g. Prettier, Stylelint) if project grows

## License

Proprietary — All rights reserved by Meaicon / Triqbit, unless otherwise specified.
