#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;

    const raw = arg.slice(2);
    if (raw.includes('=')) {
      const [key, ...rest] = raw.split('=');
      parsed[key] = rest.join('=');
      continue;
    }

    const key = raw;
    const value = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : '';
    parsed[key] = value;
    if (value) i += 1;
  }
  return parsed;
}

function slugify(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function titleCase(value) {
  return String(value || '')
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function createPage({ slug, section, title, description, prefix }) {
  const templatePath = path.join(process.cwd(), 'content', 'page-template.njk');
  const outputDir = path.join(process.cwd(), 'migrated', 'generated');

  if (!fs.existsSync(templatePath)) {
    console.error('Missing page template at content/page-template.njk');
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  let template = fs.readFileSync(templatePath, 'utf8');
  template = template
    .replace(/\{\{ pageSlug \}\}/g, slug)
    .replace(/\{\{ pageTitle \}\}/g, title)
    .replace(/\{\{ pageDescription \}\}/g, description)
    .replace(/\{\{ pageSection \}\}/g, section)
    .replace(/\{\{ pageTitlePrefix \}\}/g, prefix);

  const outputPath = path.join(outputDir, `${slug}.njk`);
  fs.writeFileSync(outputPath, template, 'utf8');
  return outputPath;
}

const args = parseArgs(process.argv.slice(2));
const slug = slugify(args.slug || args.name || 'new-page');
const section = args.section || 'Solutions';
const title = args.title || titleCase(slug);
const description = args.description || `${title} from MEAICON, designed for organisations that need resilient digital infrastructure and dependable execution.`;
const prefix = args.prefix || 'Built for';

const outputPath = createPage({ slug, section, title, description, prefix });
console.log(`Created ${outputPath}`);
