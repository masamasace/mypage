import os

# 記事が格納されているフォルダ
CONTENT_DIR = "articles"  # 適宜変更

# index.md のヘッダー
INDEX_HEADER = """# 技術記事一覧
このページは自動生成されています。
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
                title = file.replace(".md", "")
                index_content.append(f"{indent}  - [{title}]({file_path})")

    with open("index.md", "w", encoding="utf-8") as f:
        f.write("\n".join(index_content))

if __name__ == "__main__":
    generate_index()
