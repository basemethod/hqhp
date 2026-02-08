import os
import csv
import re
from bs4 import BeautifulSoup

root_dir = 'tohoku_2025'
img_new_path_prefix = 'wp-content/uploads/new_assets/'

# ページ名とファイル名のマッピング
page_map = {
    'トップページ': 'index.html',
    'わたし達について': 'aboutus/index.html',
    '事業内容': 'works/index.html',
    '採用情報': 'recruit/index.html'
}

def get_b64_filename(url):
    return url.split('/')[-1]

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

# 2. 各ページの処理
for page_name, rel_path in page_map.items():
    file_path = os.path.join(root_dir, rel_path)
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    print(f"Processing {page_name}...")

    # --- 画像の置換 ---
    page_images = [row for row in image_data if row['ページ'] == page_name]
    
    if page_name == 'トップページ':
        # スライダー
        slides = soup.select('#slider_block ul.large_slider img, #slider_block ul.small_slider img')
        for i, row in enumerate([r for r in page_images if 'トップスライダー' in r['セクション']]):
            if i < len(slides):
                slides[i]['src'] = img_new_path_prefix + get_b64_filename(row['画像'])
        
        # わたし達について
        about_img = soup.select_one('#aboutus_block .image img')
        row = next((r for r in page_images if r['セクション'] == 'わたし達について'), None)
        if about_img and row:
            about_img['src'] = img_new_path_prefix + get_b64_filename(row['画像'])

        # 事業内容 (フロントページ)
        works_items = soup.select('#worksList.frontpage li')
        for i, row in enumerate([r for r in page_images if '事業内容（' in r['セクション']]):
            if i < len(works_items):
                img = works_items[i].find('img')
                if img:
                    img['src'] = img_new_path_prefix + get_b64_filename(row['画像'])

    elif page_name == '事業内容':
        # 事業リストの更新と追加
        works_list = soup.select_one('#worksList.archive')
        if works_list:
            template_li = works_list.find('li')
            items_to_add = [row for row in text_data if row['ページ'] == '事業内容' and row['位置'] == '事業名']
            
            # 既存のリストをクリアして再構築
            works_list.clear()
            for i, row in enumerate(items_to_add):
                new_li = BeautifulSoup(str(template_li), 'html.parser').find('li')
                
                # 番号
                num_div = new_li.select_one('.num')
                if num_div: num_div.string = f"{i+1:02d}"
                
                # タイトル
                h3 = new_li.find('h3')
                if h3: h3.string = row['テキスト']
                
                # 本文
                p_text = next((r['テキスト'] for r in text_data if r['ページ'] == '事業内容' and r['セクション'] == row['セクション'] and r['位置'] == 'テキスト'), "")
                p = new_li.find('p')
                if p: p.string = p_text
                
                # 画像
                img_row = next((r for r in image_data if r['ページ'] == '事業内容' and row['テキスト'] in r['セクション']), None)
                img = new_li.find('img')
                if img and img_row:
                    img['src'] = '../' + img_new_path_prefix + get_b64_filename(img_row['画像'])
                
                works_list.append(new_li)

    # --- テキストの置換 (全般的なマッチング) ---
    # 特定のIDやクラスがわかっているものは個別処理、それ以外は現在のテキストをヒントに置換
    for row in [r for r in text_data if r['ページ'] == page_name]:
        txt = row['テキスト']
        pos = row['位置']
        
        if page_name == 'トップページ':
            if pos == 'メインキャッチ':
                target = soup.select_one('.large_txt span')
                if target: target.string = txt
            elif pos == 'サブキャッチ1':
                target = soup.select_one('.s_txt_01 span')
                if target: target.string = txt
            elif pos == 'サブキャッチ2':
                target = soup.select_one('.s_txt_02 span')
                if target: target.string = txt
            elif pos == 'テキスト' and row['セクション'] == 'わたし達について':
                target = soup.select_one('#aboutus_block .text p')
                if target: target.string = txt
            elif pos == '業種名':
                # 事業1, 事業2...
                idx = int(re.search(r'\d+', row['セクション']).group()) - 1
                items = soup.select('#worksList.frontpage li h3')
                if idx < len(items): items[idx].string = txt
            elif pos == '内容':
                idx = int(re.search(r'\d+', row['セクション']).group()) - 1
                items = soup.select('#worksList.frontpage li p')
                if idx < len(items): items[idx].string = txt

        elif page_name == 'わたし達について':
            if pos == 'キャッチ':
                target = soup.select_one('.aboutus.first-block h3')
                if target: target.string = txt
            elif pos == '文章':
                target = soup.select_one('.aboutus.first-block p')
                if target: target.string = txt

    # 保存 (HTMLエンティティをデコードした状態で保存)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify(formatter="html"))

print("HTML updates completed.")
