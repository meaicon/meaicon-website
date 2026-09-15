#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

const root = process.cwd();
const manifestPath = path.join(root, 'data', 'site-content.json');
const generatedDir = path.join(root, 'migrated', 'generated');

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

if (fs.existsSync(generatedDir)) {
  const generatedFiles = fs.readdirSync(generatedDir).filter((file) => file.endsWith('.njk')).sort();
  for (const file of generatedFiles) {
    const fullPath = path.join(generatedDir, file);
    const contents = fs.readFileSync(fullPath, 'utf8');
    const frontMatterMatch = contents.match(/^---\n([\s\S]*?)\n---\n/);
    if (!frontMatterMatch) {
      errors.push(`${file}: missing front matter`);
      continue;
    }

    const fm = frontMatterMatch[1];
    if (!/title:\s*"/.test(fm)) errors.push(`${file}: missing title`);
    if (!/description:\s*"/.test(fm)) errors.push(`${file}: missing description`);
    if (!/permalink:\s*\//.test(fm)) errors.push(`${file}: missing permalink`);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`PASS: ${pages.length} planned pages and ${fs.existsSync(generatedDir) ? fs.readdirSync(generatedDir).filter((file) => file.endsWith('.njk')).length : 0} generated page templates are structurally valid.`);
