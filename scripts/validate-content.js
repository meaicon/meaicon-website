#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function scanPageDir(dir, errors) {
  if (!fs.existsSync(dir)) return 0;
  let count = 0;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      count += scanPageDir(fullPath, errors);
    } else if (entry.name.endsWith('.njk')) {
      count++;
      const contents = fs.readFileSync(fullPath, 'utf8');
      const frontMatterMatch = contents.match(/^---\r?\n([\s\S]*?)\r?\n---/);
      if (!frontMatterMatch) {
        errors.push(`${path.relative(process.cwd(), fullPath)}: missing front matter`);
        continue;
      }
      const fm = frontMatterMatch[1];
      if (!/^title:\s+.+/m.test(fm)) errors.push(`${path.relative(process.cwd(), fullPath)}: missing title`);
      if (!/^description:\s+.+/m.test(fm)) errors.push(`${path.relative(process.cwd(), fullPath)}: missing description`);
      if (!/^permalink:\s+\//m.test(fm)) errors.push(`${path.relative(process.cwd(), fullPath)}: missing permalink`);
    }
  }
  return count;
}

const root = process.cwd();
const manifestPath = path.join(root, 'data', 'site-content.json');

const manifest = readJson(manifestPath);
const pages = Array.isArray(manifest.futurePages) ? manifest.futurePages : [];
const errors = [];
const seen = new Set();

for (const page of pages) {
  if (!page.slug) errors.push('Missing slug in futurePages');
  if (!page.title) errors.push(`Missing title for ${page.slug || 'unnamed page'}`);
  if (!page.description) errors.push(`Missing description for ${page.slug || 'unnamed page'}`);
  if (page.slug && seen.has(page.slug)) errors.push(`Duplicate slug: ${page.slug}`);
  if (page.slug) seen.add(page.slug);
}

// Scan pages/ directory for .njk files
const pagesDir = path.join(root, 'pages');
let pageFiles = 0;
if (fs.existsSync(pagesDir)) {
  pageFiles = scanPageDir(pagesDir, errors);
}

// Also scan root-level .njk files
const rootNjk = fs.readdirSync(root).filter(f => f.endsWith('.njk'));
for (const file of rootNjk) {
  const fullPath = path.join(root, file);
  const contents = fs.readFileSync(fullPath, 'utf8');
  const frontMatterMatch = contents.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (frontMatterMatch) {
    const fm = frontMatterMatch[1];
    if (!/^title:\s+.+/m.test(fm)) errors.push(`${file}: missing title`);
    if (!/^description:\s+.+/m.test(fm)) errors.push(`${file}: missing description`);
    if (!/^permalink:\s+\//m.test(fm)) errors.push(`${file}: missing permalink`);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`PASS: ${pages.length} planned pages in manifest, ${pageFiles} page templates in pages/, ${rootNjk.length} root .njk files — all structurally valid.`);
