import os
import re

root_dir = 'tohoku_2025'

# リンクを補完する正規表現
# href="../../works" や href="../../" などを対象にする
link_pattern = re.compile(r'href="([^"]+)"')

def fix_link(match):
    path = match.group(1)
    
    # 外部リンク、アンカー、既に拡張子がある場合はそのまま
    if path.startswith(('http', 'https', 'mailto', '#')) or '.' in os.path.basename(path.split('?')[0]):
        return f'href="{path}"'
    
    # 末尾がスラッシュでないディレクトリ指定を補完
    if path == "" or path.endswith("/"):
        return f'href="{path}index.html"'
    else:
        return f'href="{path}/index.html"'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # リンクの補完
                new_content = link_pattern.sub(fix_link, content)
                
                # 特殊ケース: href="../../" -> href="../../index.html" の重複スラッシュなどを微調整
                new_content = new_content.replace('//index.html', '/index.html')

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed links in: {file_path}")
            except Exception as e:
                print(f"Error: {e}")
