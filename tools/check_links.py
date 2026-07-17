import os
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse

HTML_DIR = '/Users/double2/Downloads/html/imposter-game/html'

url_cache = {}

def check_link(href, source_file):
    # Ignore empty, anchor, mailto, tel
    if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
        return True, "Ignored"

    if href in ['https://fonts.gstatic.com', 'https://fonts.googleapis.com']:
        return True, "Ignored Preconnect"

    # External link
    if href.startswith('http://') or href.startswith('https://'):
        if href in url_cache:
            return url_cache[href]
            
        try:
            req = urllib.request.Request(href, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status >= 400:
                    url_cache[href] = (False, f"HTTP {response.status}")
                else:
                    url_cache[href] = (True, "OK")
                return url_cache[href]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                url_cache[href] = (False, f"HTTP 404")
            else:
                url_cache[href] = (True, f"HTTP {e.code} (Ignored for 404 check)")
            return url_cache[href]
        except Exception as e:
            url_cache[href] = (False, f"Error: {e}")
            return url_cache[href]

    # Internal link
    parsed = urlparse(href)
    path = parsed.path
    if not path:
        return True, "Empty path"

    if path == '/':
        target_file = os.path.join(HTML_DIR, 'index.html')
    elif path.startswith('/'):
        # It's absolute to the domain, so relative to HTML_DIR
        rel_path = path.lstrip('/')
        target_file = os.path.join(HTML_DIR, rel_path)
    else:
        # Relative to current file
        target_file = os.path.join(os.path.dirname(source_file), path)

    # In Cloudflare pages, `/about-us` resolves to `about-us.html` or `about-us/index.html`
    possible_files = [
        target_file,
        target_file + '.html',
        os.path.join(target_file, 'index.html')
    ]

    for pf in possible_files:
        if os.path.exists(pf) and os.path.isfile(pf):
            return True, "OK"
            
    return False, "File not found (404)"

def main():
    broken_links = []
    
    # Regular expression to find href="..."
    href_pattern = re.compile(r'href=["\'](.*?)["\']', re.IGNORECASE)
    
    print("Starting link check. This might take a few seconds for external links...")

    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                hrefs = href_pattern.findall(content)
                hrefs = set(hrefs) # Deduplicate hrefs in the same file
                
                for href in hrefs:
                    ok, msg = check_link(href, filepath)
                    if not ok:
                        broken_links.append({
                            'source': os.path.relpath(filepath, HTML_DIR),
                            'href': href,
                            'error': msg
                        })
                        print(f"[BROKEN] {os.path.relpath(filepath, HTML_DIR)} -> {href} ({msg})")

    if not broken_links:
        print("\n✅ All links are working properly! No 404s found.")
    else:
        print(f"\n❌ Found {len(broken_links)} broken link(s).")

if __name__ == "__main__":
    main()
