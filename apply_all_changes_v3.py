import re
import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace "南東北事業本部"
    content = content.replace('南東北事業本部', '〇〇事業本部')

    # 2. Mask address and phone
    content = content.replace('980-0014', '〇〇〇-〇〇〇〇')
    content = re.sub(r'宮城県仙台市青葉区本町2丁目19-21\s+CST共立ビル4階', '〇〇県〇〇市〇〇区〇〇町〇丁目〇-〇  〇〇〇〇〇〇階', content)
    content = content.replace('022-398-4975', '000-000-0000')

    # 3. Handle specific links in SPONSOR LIST (Footer)
    # Target only inside <ul id="sponsorList">
    sponsor_match = re.search(r'(<ul id="sponsorList"[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
    if sponsor_match:
        before_sponsor = sponsor_match.group(1)
        sponsor_inner = sponsor_match.group(2)
        after_sponsor = sponsor_match.group(3)
        
        # Replace talent-clip in sponsor list
        sponsor_inner = re.sub(
            r'<li>\s*<a[^>]*href="https://www\.talent-clip\.jp/workers/jobs"[^>]*>.*?</a>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク1</div></li>',
            sponsor_inner, flags=re.DOTALL
        )
        # Also catch the one we already broke
        sponsor_inner = re.sub(
            r'<li>\s*<div[^>]*>外部リンク1</div>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク1</div></li>',
            sponsor_inner, flags=re.DOTALL
        )

        # Replace i-choice-workers in sponsor list
        sponsor_inner = re.sub(
            r'<li>\s*<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>.*?</a>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク2</div></li>',
            sponsor_inner, flags=re.DOTALL
        )
        # Also catch the one we already broke
        sponsor_inner = re.sub(
            r'<li>\s*<div[^>]*>外部リンク2</div>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク2</div></li>',
            sponsor_inner, flags=re.DOTALL
        )

        # Update the content with fixed sponsor list
        content = content[:sponsor_match.start()] + before_sponsor + sponsor_inner + after_sponsor + content[sponsor_match.end():]

    # 4. Handle remaining links in MAIN CONTENT
    # For these, we remove the <a> tag but KEEP the <img> or text inside
    # (Fixing the damage from the previous script which replaced them with span/div)
    
    # Restore the specific images in recruit_block if they were replaced
    content = re.sub(
        r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク1</div></li>',
        r'<li><img src="wp-content/uploads/new_assets/fukaya.jpg" alt="採用情報"></li>',
        content
    )
    content = re.sub(
        r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク2</div></li>',
        r'<li><img src="wp-content/uploads/new_assets/shizukanagogo.jpg" alt="採用情報"></li>',
        content
    )
    # Fix relative paths for nested pages if necessary
    if '/disclosures/' in file_path or '/news/' in file_path or '/aboutus/' in file_path or '/works/' in file_path or '/branches/' in file_path or '/recruit/' in file_path or '/overview/' in file_path or '/contact/' in file_path or '/sitemap/' in file_path or '/privacy-policy/' in file_path:
        content = content.replace('src="wp-content/uploads/new_assets/', 'src="../wp-content/uploads/new_assets/')

    # Remove the <a> tags but keep the content for these URLs everywhere else
    content = re.sub(r'<a[^>]*href="https://www\.talent-clip\.jp/workers/jobs"[^>]*>(.*?)</a>', r'\1', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>(.*?)</a>', r'\1', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = 'tohoku_2025'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    main()
