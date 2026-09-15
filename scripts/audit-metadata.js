const fs = require("node:fs");
const path = require("node:path");

function decodeEntities(value) {
  return value
    .replace(/&amp;/g, "&")
    .replace(/&mdash;/g, "—")
    .replace(/&middot;/g, "·")
    .replace(/&nbsp;/g, " ");
}

const pages = fs.readdirSync(".")
  .filter((file) => file.endsWith(".html"))
  .sort();
const metadata = pages.map((file) => {
  const html = fs.readFileSync(path.join(".", file), "utf8");
  const title = decodeEntities(html.match(/<title>([^<]*)<\/title>/i)?.[1] || "").trim();
  const description = decodeEntities(html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i)?.[1] || "").trim();
  return { file, title, description };
});

const errors = [];
const titles = new Map();
for (const page of metadata) {
  if (!page.title) errors.push(`${page.file}: missing title`);
  if (!page.description) errors.push(`${page.file}: missing meta description`);
  if (page.title.length > 60) errors.push(`${page.file}: title is ${page.title.length} characters`);
  if (page.description.length > 160) errors.push(`${page.file}: description is ${page.description.length} characters`);
  if (titles.has(page.title)) errors.push(`${page.file}: duplicate title with ${titles.get(page.title)}`);
  titles.set(page.title, page.file);
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exitCode = 1;
} else {
  console.log(`PASS: ${metadata.length} pages have unique, usable metadata`);
}
