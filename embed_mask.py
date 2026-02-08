import base64
import os
import re

# マスク画像を読み込んでBase64に変換
img_path = 'tohoku_2025/wp-content/themes/minami_tohoku/img/index/aboutus_cover.gif'
with open(img_path, 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

data_uri = f'data:image/gif;base64,{b64_data}'

# CSSファイルを修正
css_path = 'tohoku_2025/wp-content/themes/minami_tohoku/css/share.css'
with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

# mask-image の URL を Data URI に置換 (複数箇所ある可能性を考慮)
content = re.sub(r'-webkit-mask-image:\s*url\([^\)]+\);', f'-webkit-mask-image: url("{data_uri}");', content)
content = re.sub(r'mask-image:\s*url\([^\)]+\);', f'mask-image: url("{data_uri}");', content)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Successfully embedded mask image as Base64.')
