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

    # 3. Handle specific links
    # Replace the whole link tag with a styled span
    content = re.sub(
        r'<a[^>]*href="https://www\.talent-clip\.jp/workers/jobs"[^>]*>.*?</a>',
        r'<span style="border: 3px solid white; color: white; padding: 5px 10px; display: inline-block;">外部リンク1</span>',
        content, flags=re.DOTALL
    )
    
    content = re.sub(
        r'<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>.*?</a>',
        r'<span style="border: 3px solid white; color: white; padding: 5px 10px; display: inline-block;">外部リンク2</span>',
        content, flags=re.DOTALL
    )

    # Specific cleanup for sponsor list if it's within <li> and now has a <span>
    content = re.sub(
        r'<li>\s*<span style="border: 3px solid white; color: white; padding: 5px 10px; display: inline-block;">(外部リンク[12])</span>\s*</li>',
        r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">\1</div></li>',
        content, flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = 'tohoku_2025'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                process_file(file_path)

if __name__ == "__main__":
    main()
