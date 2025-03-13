import os
import datetime

# 記事が格納されているフォルダ
CONTENT_DIR = "contents" 

# index.md のヘッダー
now_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
INDEX_HEADER = f"""
# 研究・教育資料一覧
このページは、{now_str} に生成されました。
"""

def generate_index():
    index_content = [INDEX_HEADER]

    for root, dirs, files in os.walk(CONTENT_DIR):
        level = root.replace(CONTENT_DIR, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)
        if level > 0:
            index_content.append(f"{indent}- **{folder_name}**")

        for file in sorted(files):
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                # flont matter中にtitleがあればそれを使用する
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    first_line = lines[1].strip()
                    if first_line.startswith("title:"):
                        title = first_line.replace("title:", "").strip()
                        title = title.replace("\"", "").replace("\'", "")
                    else:
                        title = file.replace(".md", "")
                index_content.append(f"{indent}  - [{title}]({file_path})")

    with open("index.md", "w", encoding="utf-8") as f:
        f.write("\n".join(index_content))

if __name__ == "__main__":
    generate_index()
