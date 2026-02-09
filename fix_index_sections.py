import os
import csv
import re

root_dir = 'tohoku_2025'
img_prefix = 'wp-content/uploads/new_assets/'

def load_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
            data.append(clean_row)
    return data

text_data = load_csv('text.csv')
image_data = load_csv('imageList.csv')

def get_filename(url):
    return url.split('/')[-1]

def update_index():
    file_path = os.path.join(root_dir, 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 事業内容 (Works) ---
    for i in range(1, 4):
        sec = f"事業{i}"
        title = next((r['テキスト'] for r in text_data if r['ページ'] == 'トップページ' and r['セクション'] == sec and r['位置'] == '業種名'), None)
        desc = next((r['テキスト'] for r in text_data if r['ページ'] == 'トップページ' and r['セクション'] == sec and r['位置'] == '内容'), None)
        # 画像URL
        img_row = next((r for r in image_data if r['ページ'] == 'トップページ' and f'事業内容（{title}）' in r['セクション']), None)
        if not img_row: # fallback
             img_row = next((r for r in image_data if r['ページ'] == 'トップページ' and f'事業内容（' in r['セクション'] and str(i) in r['セクション']), None)

        if title and desc:
            # <li> の中身を正規表現で特定して置換 (番号01, 02, 03をキーにする)
            pattern = rf'(<div class="num mincho">0{i}</div>.*?<h3>).*?(</h3>\s*<p>).*?(</p>)'
            html = re.sub(pattern, rf'\1{title}\2{desc}\3', html, flags=re.DOTALL)
            
            if img_row:
                new_img = img_prefix + get_filename(img_row['画像'])
                # 画像タグのsrcを置換 (その事業のタイトルの前にあるimgを探す)
                img_pattern = rf'(<div class="num mincho">0{i}</div>\s*<div class="image"><img src=")[^"]+(")'
                html = re.sub(img_pattern, rf'\1{new_img}\2', html, flags=re.DOTALL)

    # --- 採用情報 (Recruit) ---
    r_text = next((r['テキスト'] for r in text_data if r['ページ'] == 'トップページ' and r['セクション'] == '採用情報' and r['位置'] == 'テキスト'), None)
    if r_text:
        html = re.sub(r'(<div id="recruit_block".*?<div class="text">.*?<p>).*?(</p>)', rf'\1{r_text}\2', html, flags=re.DOTALL)

    # 採用情報の画像 (2枚)
    r_imgs = [r for r in image_data if r['ページ'] == 'トップページ' and '採用情報' in r['セクション']]
    if len(r_imgs) >= 2:
        # 1枚目
        html = re.sub(r'(<div class="images">.*?<li><img src=")[^"]+(")', rf'\1{img_prefix + get_filename(r_imgs[0]["画像"])}\2', html, flags=re.DOTALL)
        # 2枚目
        html = re.sub(r'(<div class="images">.*?<li>.*?</li>\s*<li><img src=")[^"]+(")', rf'\1{img_prefix + get_filename(r_imgs[1]["画像"])}\2', html, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

update_index()
print("Front page Works and Recruit sections updated.")
