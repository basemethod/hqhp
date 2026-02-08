import os
import csv
import re

root_dir = 'tohoku_2025'
img_new_path_prefix = 'wp-content/uploads/new_assets/'

# 1. データの読み込み
text_data = []
with open('text.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # キーから余分な空白を除去
        clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
        if clean_row.get('テキスト'):
            text_data.append(clean_row)

image_data = []
with open('imageList.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
        image_data.append(clean_row)

def get_filename(url):
    return url.split('/')[-1]

def update_top_page():
    file_path = os.path.join(root_dir, 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

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

    # 画像 (スライダー)
    slides = [r for r in image_data if 'トップスライダー' in r['セクション']]
    # 既存の画像パスを特定して置換 (複数あるのでループ)
    old_imgs = [
        'wp-content/uploads/2025/12/20260119085447.jpg',
        'wp-content/uploads/2025/12/20260119085448.jpg',
        'wp-content/uploads/2026/01/20260204035414.jpg'
    ]
    for i, old_path in enumerate(old_imgs):
        if i < len(slides):
            new_path = img_new_path_prefix + get_filename(slides[i]['画像'])
            content = content.replace(old_path, new_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_aboutus_page():
    file_path = os.path.join(root_dir, 'aboutus/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    c = next((r['テキスト'] for r in text_data if r['ページ'] == 'わたし達について' and r['位置'] == 'キャッチ'), None)
    if c: content = re.sub(r'(<h3[^>]*>).*?(</h3>)', rf'\1{c}\2', content, flags=re.DOTALL)
    
    b = next((r['テキスト'] for r in text_data if r['ページ'] == 'わたし達について' and r['位置'] == '文章'), None)
    if b: content = re.sub(r'(<h3[^>]*>.*?</h3>\s*<p[^>]*>).*?(</p>)', rf'\1{b}\2', content, flags=re.DOTALL)

    # 画像
    row = next((r for r in image_data if r['ページ'] == 'わたし達について' and r['画像']), None)
    if row:
        new_img = '../' + img_new_path_prefix + get_filename(row['画像'])
        content = re.sub(r'(<div class="image">.*?<img src=")[^"]+(")', rf'\1{new_img}\2', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

update_top_page()
update_aboutus_page()
print("Top and Aboutus pages updated.")
