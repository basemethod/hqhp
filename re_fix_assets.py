import os
import re

root_dir = 'tohoku_2025'

# シングルクォートを適切に扱うように修正
query_pattern = re.compile(r'(\.(?:css|js|png|jpg|jpeg|gif|svg|pdf|woff|woff2|ttf))(\?[^"\'\s\)]+)')

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.html', '.css', '.js')):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                new_content = query_pattern.sub(r'\1', content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Refixed: {file_path}")
            except Exception as e:
                print(f"Error: {e}")