#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const manifest = require(path.join(process.cwd(), 'data', 'site-content.json'));
const generatorPath = path.join(process.cwd(), 'scripts', 'generate-page.js');
const generatedDir = path.join(process.cwd(), 'migrated', 'generated');

fs.mkdirSync(generatedDir, { recursive: true });

const pages = Array.isArray(manifest.futurePages) ? manifest.futurePages : [];
for (const page of pages) {
  const slug = page.slug || '';
  const section = page.section || 'Solutions';
  const title = page.title || 'New Page';
  const description = page.description || `${title} from MEAICON.`;
  const prefix = page.prefix || 'Built for';

  if (!slug) continue;

  execFileSync('node', [
    generatorPath,
    '--slug=' + slug,
    '--section=' + section,
    '--title=' + title,
    '--description=' + description,
    '--prefix=' + prefix
  ], { stdio: 'inherit' });
}

console.log(`Generated ${pages.length} template pages from data/site-content.json`);
