import os
import re
from PIL import Image

# 文件路径
README_PATH = "README.md"
ASSETS_DIR = "assets"
BG_PATH = os.path.join(ASSETS_DIR, "bg.png")

# GitHub 需要相对路径
BG_TOP_PATH = "assets/bg_top.png"
BG_BOTTOM_PATH = "assets/bg_bottom.png"

# **调整背景高度，让其与表格高度一致**
ROW_HEIGHT = 50  # GitHub 默认表格行高约 50px
TABLE_ROWS = 2  # 1 行标题 + 1 行数据
BACKGROUND_HEIGHT = ROW_HEIGHT * TABLE_ROWS  # 计算目标背景图高度

BASE_URL = "https://github.com/Ascarshen/js-puzzles/tree/main"
PUZZLE_BASE_URL = "https://www.janestreet.com/puzzles"

def crop_background():
    """ 读取 `assets/bg.png` 并裁剪背景，使其高度与表格匹配 """
    if not os.path.exists(BG_PATH):
        print(f"❌ Error: Background image `{BG_PATH}` not found! Please make sure `assets/bg.png` exists.")
        return
    
    print(f"📤 Loading background image: {BG_PATH}")
    image = Image.open(BG_PATH)

    width, height = image.size

    # **确保裁剪高度不超过原始图片高度**
    crop_height = min(BACKGROUND_HEIGHT, height)

    # 确保 assets 目录存在
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    # 删除旧图片（如果存在）
    for file_path in [BG_TOP_PATH, BG_BOTTOM_PATH]:
        if os.path.exists(file_path):
            os.remove(file_path)

    # 裁剪上半部分，使其与表格高度一致
    top_half = image.crop((0, 0, width, crop_height))
    top_half.save(BG_TOP_PATH)
    print(f"✅ Updated top half: {BG_TOP_PATH}")

    # 裁剪下半部分，使其与表格高度一致
    bottom_half = image.crop((0, height - crop_height, width, height))
    bottom_half.save(BG_BOTTOM_PATH)
    print(f"✅ Updated bottom half: {BG_BOTTOM_PATH}")

def update_readme():
    """ 更新 README.md，确保 `<!-- 背景图上半部分 -->` 和 `<!-- 背景图下半部分 -->` 只出现一次 """
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.readlines()

    # **删除旧的 `<!-- 背景图上半部分 -->` 代码**
    cleaned_content = []
    inside_old_top_section = False
    inside_old_bottom_section = False

    for line in content:
        if "<!-- 背景图上半部分 -->" in line:
            inside_old_top_section = True
            continue
        if "<!-- TABLE_START -->" in line:
            inside_old_top_section = False
        if "<!-- 背景图下半部分 -->" in line:
            inside_old_bottom_section = True
            continue
        if "<!-- TABLE_END -->" in line:
            inside_old_bottom_section = False
        
        if not inside_old_top_section and not inside_old_bottom_section:
            cleaned_content.append(line)

    # **找到 `<!-- TABLE_START -->` 和 `<!-- TABLE_END -->` 的索引**
    if "<!-- TABLE_START -->\n" not in cleaned_content or "<!-- TABLE_END -->\n" not in cleaned_content:
        print("❌ Error: `README.md` is missing `<!-- TABLE_START -->` or `<!-- TABLE_END -->`.")
        return  

    start_idx = cleaned_content.index("<!-- TABLE_START -->\n")
    end_idx = cleaned_content.index("<!-- TABLE_END -->\n") + 1

    # 生成新的 **居中的表格**
    new_table = f"<!-- 背景图上半部分 -->\n![背景上半部分]({BG_TOP_PATH})\n\n"
    new_table += "<!-- TABLE_START -->\n"
    new_table += "<div align='center'>\n\n"
    new_table += "| Year  | Month | Puzzle Name | Problem | My Solution | Official Solution |\n"
    new_table += "|------ |------ |------------|---------|------------|------------------|\n"
    new_table += "| 2025  | 01  | Somewhat Square Sudoku | [📜](https://www.janestreet.com/puzzles/somewhat-square-sudoku-index/) | [✔](https://github.com/Ascarshen/js-puzzles/tree/main/2025/202501-somewhat-square-sudoku/) | [🔗](https://www.janestreet.com/puzzles/somewhat-square-sudoku-solution/) |\n"
    new_table += "</div>\n\n"
    new_table += "<!-- TABLE_END -->\n\n"
    new_table += f"<!-- 背景图下半部分 -->\n![背景下半部分]({BG_BOTTOM_PATH})\n"

    cleaned_content[start_idx:end_idx] = [new_table]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(cleaned_content)

    print("✅ README.md updated! Table is now centered.")

if __name__ == "__main__":
    crop_background()  # 自动裁剪背景
    update_readme()
