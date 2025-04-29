import os
import re
from PIL import Image

# 文件路径
README_PATH = "README.md"
ASSETS_DIR = "assets"
BG_PATH = os.path.join(ASSETS_DIR, "bg.png")
PUZZLES_DIR = "puzzles"

# GitHub 需要相对路径
BG_TOP_PATH = "assets/bg_top.png"
BG_BOTTOM_PATH = "assets/bg_bottom.png"

# **调整背景高度，让其与表格高度一致**
ROW_HEIGHT = 50  # GitHub 默认表格行高约 50px
TABLE_ROWS = 2  # 1 行标题 + 1 行数据
BACKGROUND_HEIGHT = ROW_HEIGHT * TABLE_ROWS  # 计算目标背景图高度

BASE_URL = "https://github.com/Ascarshen/js-puzzles/tree/main"
PUZZLE_BASE_URL = "https://www.janestreet.com/puzzles"

def find_solutions():
    """ 遍历 puzzles 目录，自动收集所有题目，并按时间顺序排序 """
    solutions = []
    
    if not os.path.exists(PUZZLES_DIR):
        print(f"❌ Error: `{PUZZLES_DIR}` folder not found!")
        return solutions

    for year in sorted(os.listdir(PUZZLES_DIR), reverse=True):  # 遍历 2024, 2025...
        year_path = os.path.join(PUZZLES_DIR, year)
        if not os.path.isdir(year_path) or not year.isdigit():
            continue  # 只处理年份文件夹

        for month_dir in sorted(os.listdir(year_path), reverse=True):  # **按时间顺序（最新在上）**
            match = re.match(r"(\d{6})-(.+)", month_dir)
            if match:
                year_month = match.group(1)  # 202411
                year_num, month_num = year_month[:4], year_month[4:]  # 2024, 11
                puzzle_name = match.group(2).replace("-", " ").title()  # 转换为 Title 格式
                
                # 构造 URL
                problem_url = f"{PUZZLE_BASE_URL}/{match.group(2)}-index/"
                solution_url = f"{PUZZLE_BASE_URL}/{match.group(2)}-solution/"
                my_solution_url = f"{BASE_URL}/{PUZZLES_DIR}/{year}/{month_dir}/"

                solutions.append((year_num, month_num, puzzle_name, problem_url, my_solution_url, solution_url))
    
    # **按时间排序（最新的题目在最上面）**
    solutions.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    return solutions

def generate_solution_table(solutions):
    """ 生成动态 Markdown 表格 """
    table_md = "<!-- 背景图上半部分 -->\n"
    table_md += f"![背景上半部分]({BG_TOP_PATH})\n\n"
    table_md += "<!-- TABLE_START -->\n"
    table_md += "<div align='center'>\n\n"
    table_md += "| Year  | Month | Puzzle Name | Problem | My Solution | Official Solution |\n"
    table_md += "|------ |------ |------------|---------|------------|------------------|\n"

    for year, month, puzzle_name, problem_url, my_solution_url, solution_url in solutions:
        table_md += f"| {year} | {month} | {puzzle_name} | [📜]({problem_url}) | [✔]({my_solution_url}) | [🔗]({solution_url}) |\n"

    table_md += "</div>\n\n"
    table_md += "<!-- TABLE_END -->\n\n"
    table_md += f"<!-- 背景图下半部分 -->\n![背景下半部分]({BG_BOTTOM_PATH})\n"

    return table_md

def update_readme():
    """ 更新 README.md，确保 `<!-- 背景图上半部分 -->` 和 `<!-- 背景图下半部分 -->` 只出现一次 """
    solutions = find_solutions()
    new_table = generate_solution_table(solutions)

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

    # **更新 README.md**
    cleaned_content[start_idx:end_idx] = [new_table]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(cleaned_content)

    print("✅ README.md updated! Table dynamically generated and sorted by time.")

if __name__ == "__main__":
    update_readme()
