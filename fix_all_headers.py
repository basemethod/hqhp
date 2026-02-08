import os

root_dir = 'tohoku_2025'

# 置換するパターンの定義
old_str_1 = '<div class="sp-navigation">'
new_str_1 = '<div id="spNav" class="sp-navigation">'

old_str_2 = '<nav id="spNav" class="container">'
new_str_2 = '<nav class="container">'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            # index.html は既に修正済みなのでスキップしても良いが、
            # 安全のためにチェックしながら処理する
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                new_content = content.replace(old_str_1, new_str_1)
                new_content = new_content.replace(old_str_2, new_str_2)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed header in: {file_path}")
            except Exception as e:
                print(f"Error: {e}")
