const fs = require("node:fs");
const path = require("node:path");

function decodeEntities(value) {
  return value
    .replace(/&amp;/g, "&")
    .replace(/&mdash;/g, "—")
    .replace(/&middot;/g, "·")
    .replace(/&nbsp;/g, " ");
}

function findHtmlFiles(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findHtmlFiles(fullPath));
    } else if (entry.name.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const siteDir = path.join(process.cwd(), '_site');
const pages = findHtmlFiles(siteDir).map(f => path.relative(siteDir, f)).sort();

const metadata = pages.map((file) => {
  const html = fs.readFileSync(path.join(siteDir, file), "utf8");
  const title = decodeEntities(html.match(/<title>([^<]*)<\/title>/i)?.[1] || "").trim();
  const description = decodeEntities(html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i)?.[1] || "").trim();
  return { file, title, description };
});

const errors = [];
const titles = new Map();
for (const page of metadata) {
  if (!page.title) errors.push(`${page.file}: missing title`);
  if (!page.description) errors.push(`${page.file}: missing meta description`);
  if (page.title.length > 65) errors.push(`${page.file}: title is ${page.title.length} characters (max 65)`);
  if (page.description.length > 165) errors.push(`${page.file}: description is ${page.description.length} characters (max 165)`);
  if (titles.has(page.title)) errors.push(`${page.file}: duplicate title with ${titles.get(page.title)}`);
  titles.set(page.title, page.file);
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exitCode = 1;
} else {
  console.log(`PASS: ${metadata.length} pages have unique, usable metadata`);
}
