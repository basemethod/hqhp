import re
import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Basic replacements
    content = content.replace('南東北事業本部', '〇〇事業本部')
    content = content.replace('980-0014', '〇〇〇-〇〇〇〇')
    content = re.sub(r'宮城県仙台市青葉区本町2丁目19-21\s+CST共立ビル4階', '〇〇県〇〇市〇〇区〇〇町〇丁目〇-〇  〇〇〇〇〇〇階', content)
    content = content.replace('022-398-4975', '000-000-0000')

    # 2. Fix the broken recruit section in index.html specifically if it was corrupted
    if file_path.endswith('index.html') and 'tohoku_2025/index.html' in file_path:
        # The previous run might have put "外部リンク1" twice or "fukaya.jpg" twice
        content = re.sub(
            r'<div class="images">\s*<ul class="flex">\s*<li>.*?</li>\s*<li>.*?</li>\s*</ul>',
            r'<div class="images">
        <ul class="flex">
                    <li><img src="wp-content/uploads/new_assets/fukaya.jpg" alt="採用情報"></li>
          <li><img src="wp-content/uploads/new_assets/shizukanagogo.jpg" alt="採用情報"></li>
        </ul>',
            content, flags=re.DOTALL
        )

    # 3. Handle Footer Sponsor List
    sponsor_match = re.search(r'(<ul id="sponsorList"[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
    if sponsor_match:
        before_sponsor = sponsor_match.group(1)
        sponsor_inner = sponsor_match.group(2)
        after_sponsor = sponsor_match.group(3)
        
        # Talent-clip -> 外部リンク1
        sponsor_inner = re.sub(
            r'<li>\s*<a[^>]*href="https://www\.talent-clip\.jp/workers/jobs"[^>]*>.*?</a>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク1</div></li>',
            sponsor_inner, flags=re.DOTALL
        )
        # i-choice-workers -> 外部リンク2
        sponsor_inner = re.sub(
            r'<li>\s*<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>.*?</a>\s*</li>',
            r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク2</div></li>',
            sponsor_inner, flags=re.DOTALL
        )
        # Also catch any text replacements from previous broken runs
        sponsor_inner = re.sub(r'alt="採用情報"', r'alt="外部リンク1"', sponsor_inner)
        sponsor_inner = re.sub(r'alt="採用サイト"', r'alt="外部リンク2"', sponsor_inner)

        content = content[:sponsor_match.start()] + before_sponsor + sponsor_inner + after_sponsor + content[sponsor_match.end():]

    # 4. Remove links everywhere else but keep content
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
