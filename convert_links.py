import os

root_dir = 'tohoku_2025'
base_url = 'https://tohoku.jwcc.coop/2025/'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        # HTML, CSS, JSファイルを対象にする
        if file.endswith(('.html', '.css', '.js')) or file == 'index.html':
            file_path = os.path.join(root, file)
            
            # root_dir からの相対的な深さを計算
            rel_path_from_root = os.path.relpath(root, root_dir)
            if rel_path_from_root == '.':
                depth = 0
            else:
                depth = rel_path_from_root.count(os.sep) + 1
            
            # 深さに応じて相対パスのプレフィックスを作成
            rel_prefix = '../' * depth if depth > 0 else './'
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 絶対URLを相対パスに置換
                new_content = content.replace(base_url, rel_prefix)
                # 末尾スラッシュなしのパターンも考慮
                new_content = new_content.replace('https://tohoku.jwcc.coop/2025', rel_prefix)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {file_path} (Depth: {depth})")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")