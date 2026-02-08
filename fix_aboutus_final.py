import os
import re

path = 'tohoku_2025/wp-content/themes/minami_tohoku/css/share.css'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# セレクタ部分を特定して置換
pattern = re.compile(r'#aboutus_block\.index \.image \{[^}]+\}', re.DOTALL)
original_style = """#aboutus_block.index .image {
  -webkit-mask-image: url('../img/index/aboutus_cover.gif');
  -webkit-mask-mode: alpha;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: right;
  -webkit-mask-size: contain;
  mask-image: url('../img/index/aboutus_cover.gif');
  mask-mode: alpha;
  mask-repeat: no-repeat;
  mask-position: right;
  mask-size: contain;
  position: absolute;
  top: 50%;
  right: 0;
  width: 50vw;
  height: 100%;
  transform: translateY(-50%);
  z-index: 1;
  pointer-events: none;
}"""

content = pattern.sub(original_style, content)

if '#aboutus_block.index .image img' not in content:
    content += "\n#aboutus_block.index .image img { width: 100%; height: 100%; object-fit: cover; }\n"

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)