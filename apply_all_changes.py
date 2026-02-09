import re
import os

def apply_all_changes():
    file_path = 'tohoku_2025/index.html'
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace "南東北事業本部"
    content = content.replace('南東北事業本部', '〇〇事業本部')

    # 2. Mask address and phone
    content = content.replace('980-0014', '〇〇〇-〇〇〇〇')
    # Use more flexible regex for address and phone
    content = re.sub(r'宮城県仙台市青葉区本町2丁目19-21\s+CST共立ビル4階', '〇〇県〇〇市〇〇区〇〇町〇丁目〇-〇  〇〇〇〇〇〇階', content)
    content = content.replace('022-398-4975', '000-000-0000')

    # 3. Handle specific links and images
    # We want to find the <li> containing these specific URLs or the previously inserted data URIs
    
    # talent-clip -> 外部リンク1
    # i-choice-workers -> 外部リンク2
    
    # Since they might have been partially modified, let's look for the <li> structure in the sponsor list
    # Specifically targeting the items that had "採用情報" and "採用サイト"
    
    # We'll replace the entire <li> content for these two
    content = re.sub(
        r'<li>\s*(?:<a[^>]*href="https://www\.talent-clip\.jp/workers/jobs"[^>]*>)?\s*<img[^>]*alt="(?:採用情報|外部リンク1)"[^>]*>\s*(?:</a>)?\s*</li>',
        r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク1</div></li>',
        content, flags=re.DOTALL
    )
    
    content = re.sub(
        r'<li>\s*(?:<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>)?\s*<img[^>]*alt="(?:採用サイト|外部リンク2)"[^>]*>\s*(?:</a>)?\s*</li>',
        r'<li><div style="border: 3px solid white; color: white; padding: 10px; text-align: center; min-width: 100px;">外部リンク2</div></li>',
        content, flags=re.DOTALL
    )

    # Also handle the recruit block in main if it has these links
    content = re.sub(
        r'<a[^>]*href="https://tohoku\.jwcc\.coop/i-choice-workers/"[^>]*>.*?</a>',
        r'<span style="border: 3px solid white; color: white; padding: 5px 10px; display: inline-block;">外部リンク2</span>',
        content, flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_all_changes()
