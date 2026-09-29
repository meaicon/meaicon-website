# Kyndryl Design Reference — Extracted from kyndryl.com/us/en

## Color Palette

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Spruce (brand accent) | `#29707A` | rgb(41,112,122) | Links, buttons, accent color |
| Cloud (off-white) | `#F2F1EE` | rgb(242,241,238) | Section alt background |
| Cloud Light | `#E4F4F1` | rgb(228,244,241) | Tinted section bg |
| White | `#FFFFFF` | rgb(255,255,255) | Primary section background |
| Ink (body text) | `#3D3C3C` | rgb(61,60,60) | Body text, headings |
| Gray Mid | `#BBBBBB` | rgb(187,187,187) | Borders, dividers |
| Gray Warm | `#565049` | rgb(86,80,73) | Secondary text |
| Gray Stone | `#9E9287` | rgb(158,146,135) | Muted text |
| Dark | `#2B2B2B` | rgb(43,43,43) | Footer bg |
| Green Primary | `#1B904B` | rgb(27,144,75) | Status, success |
| Green Light | `#4CDD84` | rgb(76,221,132) | Highlights |
| Green Dark | `#042315` | rgb(4,35,21) | Dark sections |
| Red/Orange | `#FF462D` | rgb(255,70,45) | Alert, attention |
| Orange | `#FB512F` | rgb(251,81,47) | CTA accent |

## Typography

- **Headings**: "TWK Everett" → use `Plus Jakarta Sans` (already loaded via Google Fonts)
- **Body**: "Roboto" → use `Inter` (already loaded)
- **H1**: 40px, font-weight 300, line-height 1.28 (51.2px)
- **H2**: 45.6px, font-weight 300, line-height 1.12
- **H3**: 16px, font-weight 400, line-height 1.5 (24px)
- **Body**: 16px, line-height 1.5 (24px), weight 400
- **Nav links**: 14px, weight 400, white over hero, #3D3C3C on white

## Layout Patterns

- **Sections**: Full-width, alternating bg (white → cloud → white), 128px vertical padding on desktop, 80px horizontal padding
- **Section headers**: Centered title + subtitle, `kd-component-palette--white` or `--cloud` classes
- **Hero**: Image-based, full-viewport, white text over dark/image background
- **Cards**: Minimal, clean borders, no heavy shadows, subtle hover
- **Buttons**: 4px radius, 8px padding, 14px font, transparent bg with border OR solid spruce bg
- **Navigation**: Transparent over hero, white text, becomes solid on scroll
- **Footer**: Clean, organized columns, #3D3C3C text, light bg
- **Skip link**: Visually hidden until focus (accessibility)

## Palette Classes (Kyndryl's system)
- `kd-component-palette--white` → bg transparent, text #3D3C3C
- `kd-component-palette--spruce` → bg #29707A, text white
- `kd-component-palette--cloud` → bg transparent (tinted), text #3D3C3C
- `kd-component-palette--darkstone-10` → bg transparent, text #3D3C3C

## Current MEAICON Issues (Must Fix)

1. **Tailwind CDN NOT loaded on NJK pages** — all utility classes (`max-w-7xl`, `mx-auto`, `px-4`, `grid`, `flex`, `lg:grid-cols-*`) are broken. Layout is completely flat/unstyled.
2. **Skip-link visible** — `.skip-link` shows on page load. Must be visually hidden (off-screen) until :focus.
3. **Cookie consent out of shape** — `.cookie-prefs-link` is inline-block, static, disrupting footer layout.
4. **Nested `<main>` elements** — `<main id="main-content">` contains another `<main class="flex-1 site-shell">`. Invalid HTML.
5. **Header height 1825px** — Navigation is broken/expanded, taking full page height.
6. **Hero section has no background** — `bg: rgba(0,0,0,0)`, no padding, fontSize 16px (not the clamp value).
7. **Color scheme wrong** — Blue accent (#0066FF) instead of Kyndryl teal (#29707A).
8. **Typography weight wrong** — Headings are 700, should be 300 per Kyndryl.
