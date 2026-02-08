import os
import csv
import re

root_dir = 'tohoku_2025'
img_new_path_prefix = 'wp-content/uploads/new_assets/'

# データの読み込み
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

# --- 1. 事業内容ページ ---
def update_works():
    file_path = os.path.join(root_dir, 'works/index.html')
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        html_str = f.read()

    template_match = re.search(r'(<li>.*?<div class="cover flex">.*?</li>)', html_str, re.DOTALL)
    if template_match:
        template_li = template_match.group(1)
        items = []
        for i in range(1, 11):
            sec = f"事業{i}"
            name = next((r['テキスト'] for r in text_data if r['ページ'] == '事業内容' and r['セクション'] == sec and r['位置'] == '事業名'), None)
            txt = next((r['テキスト'] for r in text_data if r['ページ'] == '事業内容' and r['セクション'] == sec and r['位置'] == 'テキスト'), None)
            img_row = next((r for r in image_data if r['ページ'] == '事業内容' and name in r['セクション']), None)
            if name and txt:
                items.append({'name': name, 'text': txt, 'img': '../' + img_new_path_prefix + get_filename(img_row['画像']) if img_row else ""})

        new_html_list = []
        for i, item in enumerate(items):
            li = re.sub(r'<div class="num mincho">[^<]+</div>', f'<div class="num mincho">{i+1:02d}</div>', template_li)
            li = re.sub(r'<h3[^>]*>[^<]+</h3>', f'<h3>{item["name"]}</h3>', li)
            li = re.sub(r'(<p[^>]*>).*?(</p>)', rf'\1{item["text"]}\2', li, flags=re.DOTALL)
            if item['img']: li = re.sub(r'(<img src=")[^"]+(")', rf'\1{item["img"]}\2', li)
            new_html_list.append("    " + li)
        
        new_html = "\n".join(new_html_list)
        html_str = re.sub(r'(<ul id="worksList"[^>]*>).*?(</ul>)', rf'\1\n{new_html}\n  \2', html_str, flags=re.DOTALL)
        with open(file_path, 'w', encoding='utf-8') as f: f.write(html_str)

# --- 2. 採用情報ページ ---
def update_recruit():
    file_path = os.path.join(root_dir, 'recruit/index.html')
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        html_str = f.read()

    # タイトルとテキスト
    title = next((r['テキスト'] for r in text_data if r['ページ'] == '採用情報' and r['セクション'] == 'トップリード' and r['位置'] == 'タイトル'), None)
    txt = next((r['テキスト'] for r in text_data if r['ページ'] == '採用情報' and r['セクション'] == 'トップリード' and r['位置'] == 'テキスト'), None)
    if title: html_str = re.sub(r'(<div class="text">.*?<h3[^>]*>).*?(</h3>)', rf'\1{title}\2', html_str, flags=re.DOTALL)
    if txt: html_str = re.sub(r'(<div class="text">.*?<h3[^>]*>.*?</h3>\s*<p[^>]*>).*?(</p>)', rf'\1{txt}\2', html_str, flags=re.DOTALL)

    # インタビュー画像削除 (特定のセクションのみ)
    html_str = re.sub(r'(<ul id="interviewList".*?)(<div class="image">.*?<img[^>]*>.*?</div>)', r'\1<!-- Image removed -->', html_str, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f: f.write(html_str)

update_works()
update_recruit()
print("All major pages updated successfully.")