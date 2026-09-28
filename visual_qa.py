from playwright.sync_api import sync_playwright
import os, http.server, socketserver, threading
import json
import sys

site_dir = 'C:/Users/nev3s/repos/meaicon-website/_site'
PORT = 8121

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=site_dir, **kwargs)
    def log_message(self, *args): pass

def start_server():
    httpd = socketserver.TCPServer(('127.0.0.1', PORT), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

def check_page_layout(page, url, viewport_width, viewport_height):
    """Check a page for layout issues and return findings"""
    issues = []
    
    # Set viewport
    page.set_viewport_size({"width": viewport_width, "height": viewport_height})
    
    # Navigate to page
    try:
        page.goto(f'http://127.0.0.1:{PORT}/{url}', wait_until='domcontentloaded', timeout=10000)
        page.wait_for_timeout(800)
    except Exception as e:
        issues.append({
            "type": "navigation_error",
            "message": f"Failed to load page: {str(e)}",
            "url": url,
            "viewport": f"{viewport_width}x{viewport_height}"
        })
        return issues
    
    # Check for teal/green colors (should all be blue #0A66C2)
    color_check = page.evaluate('''() => {
        const issues = [];
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(el => {
            const computedStyle = window.getComputedStyle(el);
            const bgColor = computedStyle.backgroundColor;
            const color = computedStyle.color;
            const borderColor = computedStyle.borderColor;
            
            // Check for teal/green-ish colors (not our accent blue #0A66C2)
            const tealGreenPatterns = [
                /rgb\\s*\\(\\s*0\\s*,\\s*(\\d{2,3})\\s*,\\s*(\\d{2,3})\\s*\\)/, // rgb(0, *, *)
                /rgb\\s*\\(\\s*(\\d{1,3})\\s*,\\s*(\\d{2,3})\\s*,\\s*0\\s*\\)/, // rgb(*, *, 0)
                /rgba\\s*\\(\\s*0\\s*,\\s*(\\d{2,3})\\s*,\\s*(\\d{2,3})\\s*,\\s*[0-9.]+\\s*\\)/,
                /rgba\\s*\\(\\s*(\\d{1,3})\\s*,\\s*(\\d{2,3})\\s*,\\s*0\\s*,\\s*[0-9.]+\\s*\\)/
            ];
            
            const checkColor = (colorStr) => {
                if (!colorStr || colorStr === 'transparent' || colorStr === 'rgba(0, 0, 0, 0)') return false;
                return tealGreenPatterns.some(pattern => pattern.test(colorStr));
            };
            
            if (checkColor(bgColor) || checkColor(color) || checkColor(borderColor)) {
                // Additional check to exclude our accent blue
                const isNotOurBlue = !(
                    bgColor.includes('rgb(10, 102, 194)') || 
                    color.includes('rgb(10, 102, 194)') ||
                    borderColor.includes('rgb(10, 102, 194)')
                );
                
                if (isNotOurBlue) {
                    issues.push({
                        element: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : ''),
                        property: 'color',
                        value: {bgColor, color, borderColor}
                    });
                }
            }
        });
        
        return issues;
    }''')
    
    if color_check and len(color_check) > 0:
        issues.append({
            "type": "unexpected_colors",
            "message": f"Found {len(color_check)} elements with teal/green colors",
            "details": color_check[:10],  # Limit to first 10
            "url": url,
            "viewport": f"{viewport_width}x{viewport_height}"
        })
    
    # Check for broken images/missing icons
    broken_images = page.evaluate('''() => {
        const images = Array.from(document.querySelectorAll('img'));
        const broken = [];
        
        images.forEach(img => {
            if (!img.complete || img.naturalWidth === 0 || img.naturalHeight === 0) {
                broken.push({
                    src: img.src,
                    alt: img.alt,
                    outerHTML: img.outerHTML.substring(0, 100)
                });
            }
        });
        
        return broken;
    }''')
    
    if broken_images and len(broken_images) > 0:
        issues.append({
            "type": "broken_images",
            "message": f"Found {len(broken_images)} broken images",
            "details": broken_images[:5],
            "url": url,
            "viewport": f"{viewport_width}x{viewport_height}"
        })
    
    # Check layout: grids, cards alignment, spacing, overflow
    layout_issues = page.evaluate('''() => {
        const issues = [];
        
        // Check for elements with overflow
        const checkOverflow = (el) => {
            const style = window.getComputedStyle(el);
            if ((style.overflow === 'auto' || style.overflow === 'scroll' || 
                 style.overflowX === 'auto' || style.overflowX === 'scroll' ||
                 style.overflowY === 'auto' || style.overflowY === 'scroll') &&
                (el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight)) {
                return true;
            }
            return false;
        };
        
        const allElements = document.querySelectorAll('*');
        allElements.forEach(el => {
            if (checkOverflow(el)) {
                issues.push({
                    type: 'overflow',
                    element: el.tagName.toLowerCase() + (el.id ? '#' + el.id : el.className ? '.' + el.className.split(' ')[0] : ''),
                    scrollWidth: el.scrollWidth,
                    clientWidth: el.clientWidth,
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight
                });
            }
        });
        
        // Check card heights in grids
        const grids = document.querySelectorAll('.card-grid, .grid, [class*="grid"]');
        grids.forEach(grid => {
            const cards = grid.querySelectorAll('.feature-card, .card, [class*="card"]');
            if (cards.length > 1) {
                const heights = Array.from(cards).map(card => card.getBoundingClientRect().height);
                const maxHeight = Math.max(...heights);
                const minHeight = Math.min(...heights);
                if (maxHeight - minHeight > 10) { // More than 10px difference
                    issues.push({
                        type: 'uneven_card_heights',
                        grid: grid.className,
                        height_diff: maxHeight - minHeight,
                        max_height: maxHeight,
                        min_height: minHeight
                    });
                }
            }
        });
        
        // Check for overlapping elements (simplified)
        const positioned = document.querySelectorAll('[style*="position: absolute"], [style*="position: fixed"], [style*="position: relative"]');
        positioned.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) {
                issues.push({
                    type: 'zero_dimension_element',
                    element: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : ''),
                    rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}
                });
            }
        });
        
        return issues;
    }''')
    
    if layout_issues and len(layout_issues) > 0:
        issues.append({
            "type": "layout_issues",
            "message": f"Found {len(layout_issues)} layout issues",
            "details": layout_issues[:10],
            "url": url,
            "viewport": f"{viewport_width}x{viewport_height}"
        })
    
    return issues

def take_screenshot(page, url, filename):
    """Take screenshot of a page"""
    try:
        page.goto(f'http://127.0.0.1:{PORT}/{url}', wait_until='domcontentloaded', timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=filename, full_page=True)
        return True
    except Exception as e:
        print(f"Failed to take screenshot of {url}: {str(e)}")
        return False

def main():
    print("Starting visual QA testing...")
    
    # Start HTTP server
    httpd = start_server()
    
    # Define test pages
    main_pages = [
        "index.html",
        "about.html", 
        "solutions.html",
        "industries.html",
        "case-studies.html",
        "contact.html",
        "faq.html",
        "global-connectivity.html",
        "leadership.html",
        "methodology.html",
        "partners.html",
        "privacy-policy.html",
        "terms-of-service.html",
        "why-meaicon.html",
        "404.html"
    ]
    
    solution_pages = [
        "solutions/ai-compute.html",
        "solutions/ai-data-services.html", 
        "solutions/application-services.html",
        "solutions/blockchain.html",
        "solutions/cloud.html",
        "solutions/connectivity.html",
        "solutions/consulting.html",
        "solutions/critical-infrastructure-consulting.html",
        "solutions/cyber-security.html",
        "solutions/data-centre.html",
        "solutions/digital-workplace.html",
        "solutions/disaster-recovery.html",
        "solutions/edge-ai-inference.html",
        "solutions/edge-compute-infrastructure.html",
        "solutions/hardware-security.html",
        "solutions/identity-access.html",
        "solutions/iot.html",
        "solutions/managed-services.html",
        "solutions/mobile-data-centre.html",
        "solutions/network-security.html",
        "solutions/ota-fleet-management.html",
        "solutions/post-quantum-security.html",
        "solutions/secure-edge-computing.html",
        "solutions/smart-building-edge.html",
        "solutions/sovereign-compute.html"
    ]
    
    industry_pages = [
        "industries/banking.html",
        "industries/defence.html",
        "industries/education.html", 
        "industries/energy.html",
        "industries/government.html",
        "industries/healthcare.html",
        "industries/hospitality.html",
        "industries/logistics.html",
        "industries/maritime.html",
        "industries/real-estate.html",
        "industries/retail.html",
        "industries/telecom.html"
    ]
    
    # Consulting subpages (these are in nested directories)
    consulting_subpages = []
    consulting_dir = 'C:/Users/nev3s/repos/meaicon-website/_site/solutions/consulting'
    if os.path.exists(consulting_dir):
        for file in os.listdir(consulting_dir):
            if file.endswith('.html'):
                consulting_subpages.append(f"solutions/consulting/{file}")
    
    # Combine all pages to test
    all_pages_to_test = main_pages + solution_pages + industry_pages + consulting_subpages
    
    # Responsive test pages (homepage, solutions, industries at different breakpoints)
    responsive_tests = [
        {"page": "index.html", "width": 1440, "height": 900, "label": "desktop"},
        {"page": "index.html", "width": 768, "height": 1024, "label": "tablet"},
        {"page": "index.html", "width": 375, "height": 667, "label": "mobile"},
        {"page": "solutions.html", "width": 1440, "height": 900, "label": "desktop"},
        {"page": "solutions.html", "width": 768, "height": 1024, "label": "tablet"},
        {"page": "solutions.html", "width": 375, "height": 667, "label": "mobile"},
        {"page": "industries.html", "width": 1440, "height": 900, "label": "desktop"},
        {"page": "industries.html", "width": 768, "height": 1024, "label": "tablet"},
        {"page": "industries.html", "width": 375, "height": 667, "label": "mobile"}
    ]
    
    all_issues = []
    screenshots_taken = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Block Tailwind CDN to test static CSS
        page.route('**/cdn.tailwindcss.com**', lambda route: route.abort())
        
        # Test all pages at desktop resolution
        print("Testing all pages at 1440x900...")
        for page_url in all_pages_to_test:
            print(f"  Testing: {page_url}")
            
            # Take screenshot
            screenshot_name = f"screenshots/{page_url.replace('/', '_').replace('.', '_')}_desktop.png"
            os.makedirs(os.path.dirname(screenshot_name), exist_ok=True)
            if take_screenshot(page, page_url, screenshot_name):
                screenshots_taken.append(screenshot_name)
            
            # Check layout
            issues = check_page_layout(page, page_url, 1440, 900)
            all_issues.extend(issues)
        
        # Test responsive behavior
        print("Testing responsive behavior...")
        for test in responsive_tests:
            print(f"  Testing {test['page']} at {test['label']} ({test['width']}x{test['height']})")
            
            # Take screenshot
            screenshot_name = f"screenshots/{test['page'].replace('/', '_').replace('.', '_')}_{test['label']}.png"
            os.makedirs(os.path.dirname(screenshot_name), exist_ok=True)
            if take_screenshot(page, test['page'], screenshot_name):
                screenshots_taken.append(screenshot_name)
            
            # Check layout
            issues = check_page_layout(page, test['page'], test['width'], test['height'])
            all_issues.extend(issues)
        
        browser.close()
    
    # Shutdown server
    httpd.shutdown()
    
    # Generate report
    report = {
        "timestamp": str(p.__class__),
        "total_pages_tested": len(all_pages_to_test),
        "total_screenshots": len(screenshots_taken),
        "total_issues": len(all_issues),
        "issues_by_type": {},
        "screenshots": screenshots_taken,
        "detailed_issues": all_issues
    }
    
    # Group issues by type
    for issue in all_issues:
        issue_type = issue.get("type", "unknown")
        if issue_type not in report["issues_by_type"]:
            report["issues_by_type"][issue_type] = 0
        report["issues_by_type"][issue_type] += 1
    
    # Save report
    with open('visual_qa_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nVisual QA Complete!")
    print(f"Pages tested: {len(all_pages_to_test)}")
    print(f"Screenshots taken: {len(screenshots_taken)}")
    print(f"Total issues found: {len(all_issues)}")
    print(f"Issues by type: {report['issues_by_type']}")
    print(f"Report saved to: visual_qa_report.json")
    
    # Print summary of critical issues
    critical_issues = [issue for issue in all_issues if issue.get("type") in ["unexpected_colors", "broken_images", "layout_issues"]]
    if critical_issues:
        print(f"\nCritical Issues Found ({len(critical_issues)}):")
        for issue in critical_issues[:10]:  # Show first 10
            print(f"  - {issue['type']}: {issue['message']} ({issue['url']})")
    else:
        print("\nNo critical issues found!")
    
    return report

if __name__ == "__main__":
    main()