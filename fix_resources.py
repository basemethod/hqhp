import os
import re

root_dir = 'tohoku_2025'

# 1. クエリパラメータ（?ver=xxx等）を削除する正規表現
# \s を正しくエスケープ
query_pattern = re.compile(r'(\.(?:css|js|png|jpg|jpeg|gif|svg|pdf|woff|woff2|ttf))(\?[^"\'\s)]+)')

# 2. ディレクトリ指定を index.html 指定に補完する正規表現
link_pattern = re.compile(r'href="(\./(?:\.\./)*[a-zA-Z0-9\-_/]+)"')

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.html', '.css', '.js')):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # クエリパラメータの削除
                new_content = query_pattern.sub(r'\1', content)
                
                # HTMLの場合、ディレクトリリンクを index.html に補完
                if file.endswith('.html'):
                    def link_replacer(match):
                        path = match.group(1)
                        # 拡張子があるか、.htmlで終わる場合はそのまま
                        if path.endswith('.html') or '.' in os.path.basename(path):
                            return f'href="{path}"'
                        # ディレクトリとして扱い、index.htmlを付与
                        sep = "" if path.endswith("/") else "/"
                        return f'href="{path}{sep}index.html"'
                    
                    new_content = link_pattern.sub(link_replacer, new_content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed resources in: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")