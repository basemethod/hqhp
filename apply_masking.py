import os

def apply_masking():
    file_path = 'tohoku_2025/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace "南東北事業本部"
    content = content.replace('南東北事業本部', '〇〇事業本部')

    # Mask address
    content = content.replace('980-0014', '〇〇〇-〇〇〇〇')
    content = content.replace('宮城県仙台市青葉区本町2丁目19-21  CST共立ビル4階', '〇〇県〇〇市〇〇区〇〇町〇丁目〇-〇  〇〇〇〇〇〇階')
    
    # Mask phone
    content = content.replace('022-398-4975', '000-000-0000')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_masking()
