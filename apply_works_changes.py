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

def update_works_page():
    file_path = os.path.join(root_dir, 'works/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # <li> 構造を抽出 (テンプレートとして使用)
    template_match = re.search(r'(<li>.*?<div class="cover flex">.*?</li>)', html_content, re.DOTALL)
    if not template_match:
        print("Template <li> not found.")
        return
    template_li = template_match.group(1)

    # CSVから事業内容のデータを抽出 (事業1〜事業10)
    works_items = []
    for i in range(1, 11):
        sec_name = f"事業{i}"
        name = next((r['テキスト'] for r in text_data if r['ページ'] == '事業内容' and r['セクション'] == sec_name and r['位置'] == '事業名'), None)
        text = next((r['テキスト'] for r in text_data if r['ページ'] == '事業内容' and r['セクション'] == sec_name and r['位置'] == 'テキスト'), None)
        img_row = next((r for r in image_data if r['ページ'] == '事業内容' and name in r['セクション']), None)
        
        if name and text:
            works_items.append({
                'name': name,
                'text': text,
                'img': '../' + img_new_path_prefix + get_filename(img_row['画像']) if img_row else ""
            })

    # 新しい <ul> 内容を作成
    new_works_html = ""
    for i, item in enumerate(works_items):
        li = template_li
        li = re.sub(r'<div class="num mincho">[^<]+</div>', f'<div class="num mincho">{i+1:02d}</div>', li)
        li = re.sub(r'<h3[^>]*>[^<]+</h3>', f'<h3>{item["name"]}</h3>', li)
        # 本文の置換 (改行を考慮)
        li = re.sub(r'(<p[^>]*>).*?(</p>)', rf'\1{item["text"]}\2', li, flags=re.DOTALL)
        # 画像srcの置換
        if item['img']:
            li = re.sub(r'(<img src=")[^"]+(")', rf'\1{item["img"]}\2', li)
        
        new_works_html += "    " + li + "
"

    # <ul> の中身を置換
    final_content = re.sub(r'(<ul id="worksList"[^>]*>).*?(</ul>)', rf'\1
{new_works_html}  \2', html_content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

update_works_page()
print("Works page updated with all items.")
