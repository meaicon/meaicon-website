const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES = [
  // Solution pages (25)
  '/solutions/ai-compute.html',
  '/solutions/ai-data-services.html',
  '/solutions/application-services.html',
  '/solutions/blockchain.html',
  '/solutions/cloud.html',
  '/solutions/connectivity.html',
  '/solutions/consulting.html',
  '/solutions/critical-infrastructure-consulting.html',
  '/solutions/cyber-security.html',
  '/solutions/data-centre.html',
  '/solutions/digital-workplace.html',
  '/solutions/disaster-recovery.html',
  '/solutions/edge-ai-inference.html',
  '/solutions/edge-compute-infrastructure.html',
  '/solutions/hardware-security.html',
  '/solutions/identity-access.html',
  '/solutions/iot.html',
  '/solutions/managed-services.html',
  '/solutions/mobile-data-centre.html',
  '/solutions/network-security.html',
  '/solutions/ota-fleet-management.html',
  '/solutions/post-quantum-security.html',
  '/solutions/secure-edge-computing.html',
  '/solutions/smart-building-edge.html',
  '/solutions/sovereign-compute.html',
  
  // Consulting sub-pages (7)
  '/solutions/consulting/digital-transformation-strategy.html',
  '/solutions/consulting/infrastructure-network-audits.html',
  '/solutions/consulting/managed-services-outsourcing.html',
  '/solutions/consulting/regulatory-compliance-advisory.html',
  '/solutions/consulting/technology-roadmap-vendor-selection.html',
  '/solutions/consulting/tokenisation-advisory.html',
  
  // Industry pages (12)
  '/industries/banking.html',
  '/industries/defence.html',
  '/industries/education.html',
  '/industries/energy.html',
  '/industries/government.html',
  '/industries/healthcare.html',
  '/industries/hospitality.html',
  '/industries/logistics.html',
  '/industries/maritime.html',
  '/industries/real-estate.html',
  '/industries/retail.html',
  '/industries/telecom.html',
  
  // Core pages
  '/index.html',
  '/solutions.html',
  '/industries.html',
  '/case-studies.html',
  '/insights.html',
  '/about.html',
  '/contact.html',
];

const BASE_URL = 'http://localhost:8095';
const SCREENSHOTS_DIR = path.join(__dirname, 'audit-screenshots');

async function auditPage(page, url, name) {
  const issues = [];
  
  try {
    await page.goto(`${BASE_URL}${url}`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000); // Allow animations to settle
    
    // Check for common issues
    const checks = await page.evaluate(() => {
      const results = {
        gridIssues: [],
        emptySpaces: [],
        misalignedText: [],
        cardHeightIssues: [],
        bentoOverflow: [],
        horizontalOverflow: false,
        verticalOverflow: false
      };
      
      // Check horizontal overflow
      if (document.body.scrollWidth > window.innerWidth) {
        results.horizontalOverflow = true;
      }
      
      // Check for grid containers
      const grids = document.querySelectorAll('[class*="grid"], [class*="bento"], .feature-grid, .card-grid, .solution-grid, .industry-grid');
      grids.forEach((grid, i) => {
        const style = window.getComputedStyle(grid);
        const children = Array.from(grid.children);
        
        if (children.length > 0) {
          // Check if grid has proper columns
          if (style.gridTemplateColumns === 'none' && style.display === 'grid') {
            results.gridIssues.push(`Grid ${i} has no columns defined`);
          }
          
          // Check card heights for consistency
          const heights = children.map(c => c.getBoundingClientRect().height);
          const minHeight = Math.min(...heights);
          const maxHeight = Math.max(...heights);
          if (maxHeight - minHeight > 50) { // More than 50px difference
            results.cardHeightIssues.push(`Grid ${i}: card height variance ${Math.round(maxHeight - minHeight)}px (min: ${Math.round(minHeight)}, max: ${Math.round(maxHeight)})`);
          }
          
          // Check for empty grid cells
          children.forEach((child, ci) => {
            const rect = child.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) {
              results.emptySpaces.push(`Grid ${i} child ${ci} has zero dimensions`);
            }
          });
        }
      });
      
      // Check for bento grid overflow
      const bentoGrids = document.querySelectorAll('.bento-grid, [class*="bento"]');
      bentoGrids.forEach((bento, i) => {
        const style = window.getComputedStyle(bento);
        const rect = bento.getBoundingClientRect();
        if (rect.width > window.innerWidth || rect.height > window.innerHeight * 2) {
          results.bentoOverflow.push(`Bento grid ${i} may overflow: ${Math.round(rect.width)}x${Math.round(rect.height)}`);
        }
      });
      
      // Check for text alignment issues
      const textElements = document.querySelectorAll('h1, h2, h3, h4, p, .section-title, .page-title, .display-title');
      textElements.forEach((el, i) => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        // Check if text is clipped
        if (rect.width > window.innerWidth - 40) {
          results.misalignedText.push(`Text element ${i} (${el.tagName}) may be clipped: ${Math.round(rect.width)}px wide`);
        }
        // Check for very small text
        const fontSize = parseFloat(style.fontSize);
        if (fontSize < 10 && el.textContent.trim().length > 0) {
          results.misalignedText.push(`Text element ${i} has very small font: ${fontSize}px`);
        }
      });
      
      // Check for empty sections
      const sections = document.querySelectorAll('section, .content-section, .section-band');
      sections.forEach((section, i) => {
        const children = section.querySelectorAll(':scope > *');
        let hasContent = false;
        children.forEach(child => {
          if (child.textContent.trim().length > 0 || child.querySelector('img, svg, canvas')) {
            hasContent = true;
          }
        });
        if (!hasContent && section.offsetHeight < 50) {
          results.emptySpaces.push(`Section ${i} appears empty (${Math.round(section.offsetHeight)}px height)`);
        }
      });
      
      return results;
    });
    
    // Take screenshot
    const screenshotPath = path.join(SCREENSHOTS_DIR, `${name.replace(/\//g, '-').replace('.html', '')}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    
    // Combine issues
    Object.values(checks).flat().forEach(issue => {
      if (issue) issues.push(`${name}: ${issue}`);
    });
    
    if (checks.horizontalOverflow) issues.push(`${name}: Horizontal overflow detected`);
    
    return { url, issues, screenshot: screenshotPath };
  } catch (error) {
    return { url, issues: [`${name}: Error - ${error.message}`], screenshot: null };
  }
}

async function main() {
  // Create screenshots directory
  if (!fs.existsSync(SCREENSHOTS_DIR)) {
    fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
  }
  
  // Start server check
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  
  const allResults = [];
  let totalIssues = 0;
  
  for (const pageUrl of PAGES) {
    const name = pageUrl.replace(/^\//, '').replace('.html', '');
    console.log(`Auditing ${pageUrl}...`);
    const result = await auditPage(page, pageUrl, name);
    allResults.push(result);
    totalIssues += result.issues.length;
    if (result.issues.length > 0) {
      console.log(`  ⚠️  ${result.issues.length} issues found`);
      result.issues.forEach(i => console.log(`    - ${i}`));
    } else {
      console.log(`  ✓  No issues`);
    }
  }
  
  await browser.close();
  
  // Generate report
  const report = {
    timestamp: new Date().toISOString(),
    pagesChecked: PAGES.length,
    totalIssues,
    results: allResults
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'audit-report.json'),
    JSON.stringify(report, null, 2)
  );
  
  console.log('\n=== AUDIT SUMMARY ===');
  console.log(`Pages checked: ${PAGES.length}`);
  console.log(`Total issues: ${totalIssues}`);
  console.log(`Screenshots saved to: ${SCREENSHOTS_DIR}`);
  console.log(`Report saved to: audit-report.json`);
  
  // Print issues summary
  const issuesByType = {};
  allResults.forEach(r => {
    r.issues.forEach(issue => {
      const type = issue.split(': ')[1]?.split(' ')[0] || 'other';
      issuesByType[type] = (issuesByType[type] || 0) + 1;
    });
  });
  
  console.log('\nIssues by type:');
  Object.entries(issuesByType).forEach(([type, count]) => {
    console.log(`  ${type}: ${count}`);
  });
  
  return report;
}

main().catch(console.error);