import re
import os

def fix_works():
    file_path = 'tohoku_2025/works/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the common header (up to the first inner-title)
    # Actually, let's take everything up to the first main-article works
    header_match = re.search(r'<!DOCTYPE html>.*?<div id="main-article" class="works">\s*<ul id="worksList" class="archive contain-1200 wid-90pct">', content, re.DOTALL)
    if not header_match:
        print("Header not found")
        return
    header = header_match.group(0)

    # Extract all business items
    # They look like <li>\s*<div class="cover flex">.*?</li>
    items = re.findall(r'<li>\s*<div class="cover flex">.*?</li>', content, re.DOTALL)
    
    # Dedup items based on title
    seen_titles = set()
    unique_items = []
    for item in items:
        title_match = re.search(r'<h3>(.*?)</h3>', item)
        if title_match:
            title = title_match.group(1)
            if title not in seen_titles:
                seen_titles.add(title)
                unique_items.append(item)

    # Extract the common footer (from brancheslinkbtn to the end)
    footer_match = re.search(r'</ul>\s*<div class="brancheslinkbtn">.*</html>', content, re.DOTALL)
    if not footer_match:
        # Try finding from the last </ul>
        footer_parts = content.split('</ul>')
        footer = '</ul>' + footer_parts[-1]
    else:
        footer = footer_match.group(0)

    # Reconstruct
    new_content = header + '\n' + '\n'.join(unique_items) + '\n' + footer
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    fix_works()