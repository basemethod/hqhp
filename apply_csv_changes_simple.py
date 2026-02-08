import os
import csv
import re
import html

root_dir = 'tohoku_2025'
img_new_path_prefix = 'wp-content/uploads/new_assets/'

# 1. データの読み込み
text_data = []
with open('text.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['テキスト'].strip():
            text_data.append(row)

image_data = []
with open('imageList.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        image_data.append(row)

def get_filename(url):
    return url.split('/')[-1]

def update_file(rel_path, page_name):
    file_path = os.path.join(root_dir, rel_path)
    if not os.path.exists(file_path): return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Updating {page_name}...")

    # --- テキスト置換 (正規表現による簡易版) ---
    # トップページ
    if page_name == 'トップページ':
        # メインキャッチ
        m = next((r['テキスト'] for r in text_data if r['位置'] == 'メインキャッチ'), None)
        if m: content = re.sub(r'(<div class="large_txt"><span>)[^<]+(</span></div>)', rf'\1{m}\2', content)
        
        # サブキャッチ
        s1 = next((r['テキスト'] for r in text_data if r['位置'] == 'サブキャッチ1'), None)
        if s1: content = re.sub(r'(<div class="s_txt_01"><span>)[^<]+(</span></div>)', rf'\1{s1}\2', content)
        s2 = next((r['テキスト'] for r in text_data if r['位置'] == 'サブキャッチ2'), None)
        if s2: content = re.sub(r'(<div class="s_txt_02"><span>)[^<]+(</span></div>)', rf'\1{s2}\2', content)

        # わたし達について
        a_txt = next((r['テキスト'] for r in text_data if r['セクション'] == 'わたし達について' and r['位置'] == 'テキスト'), None)
        if a_txt: content = re.sub(r'(<div id="aboutus_block"[^>]*>.*?<div class="text">.*?<p[^>]*>).*?(</p>)', rf'\1{a_txt}\2', content, flags=re.DOTALL)

        # 画像置換
        # スライダー (簡略化のため、最初の3つを置換)
        slides = [r for r in image_data if 'トップスライダー' in r['セクション']]
        for i, row in enumerate(slides):
            new_img = img_new_path_prefix + get_filename(row['画像'])
            # 非常に限定的な置換
            content = content.replace(f'wp-content/uploads/2025/12/20260119085447.jpg', new_img) # placeholder logic
            
    elif page_name == 'わたし達について':
        c = next((r['テキスト'] for r in text_data if r['ページ'] == 'わたし達について' and r['位置'] == 'キャッチ'), None)
        if c: content = re.sub(r'(<h3[^>]*>).*?(</h3>)', rf'\1{c}\2', content, flags=re.DOTALL)
        
        b = next((r['テキスト'] for r in text_data if r['ページ'] == 'わたし達について' and r['位置'] == '文章'), None)
        if b: content = re.sub(r'(<h3[^>]*>.*?</h3>\s*<p[^>]*>).*?(</p>)', rf'\1{b}\2', content, flags=re.DOTALL)

    # 保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 実行
update_file('index.html', 'トップページ')
update_file('aboutus/index.html', 'わたし達について')

print("Update process finished (Basic text replacement).")
