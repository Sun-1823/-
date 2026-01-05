import re
import pandas as pd

# ----------------- 文件路径设置 (请核对) -----------------
novel_file_path = 'D:\\桌面\\红与黑\\hong_yu_hei.txt'

# ----------------- 1. 文件加载函数 -----------------
def read_novel_text(file_path):
    """尝试以常见的中文编码读取文本文件，并返回文件内容。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            print("✅ 文件加载成功，使用 UTF-8 编码。")
            return raw_content
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                raw_content = f.read()
                print("✅ 文件加载成功，使用 GBK 编码。")
                return raw_content
        except Exception as e:
            print(f"❌ GBK 编码也失败了。请检查文件路径和编码。错误信息: {e}")
            return None

# ----------------- 2. 执行文件加载 -----------------
raw_content = read_novel_text(novel_file_path)

if raw_content is None:
    print("❌ 致命错误：无法读取文件，脚本中止。")
    exit()

print("-" * 40)
print(f"总共读取了 {len(raw_content)} 个字符。")
print("文件前 100 个字符预览:")
print(raw_content[:100])
print("-" * 40)


# ----------------- 3. 定义清洗函数 (增强版) -----------------
def clean_chapter_text(text):
    """增强版清洗函数：去除多余的空白字符、方括号和圆括号内的注释。"""
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(r'\[.*?\]', '', text)  # 移除方括号及其内容 (用于清除注释)
    text = re.sub(r'\(.*?\)', '', text)  # 移除圆括号及其内容
    text = re.sub(r' {2,}', ' ', text).strip()  # 移除多余的连续空格
    return text


# ----------------- 4. 预处理：定位正文起始点 -----------------
regex_start_point = r'(上卷|下卷)'
match = re.search(regex_start_point, raw_content)

if match:
    content_start_index = match.start()
    novel_body = raw_content[content_start_index:]
    print("✅ 已定位到正文起始点（上卷）。")
else:
    novel_body = raw_content
    print("⚠️ 警告：未找到'上卷/下卷'标识，使用全文进行分割。")


# ----------------- 5. 章节分割与数据构建 (最终修正版：按行匹配标题) -----------------
# 匹配行首的章节编号和标题：^\s*(\d+)\s+([^\n\r]+)$
regex_chapter = r'^\s*(\d+)\s+([^\n\r]+)$'
chapter_lines = novel_body.split('\n')

chapter_data = []
current_chapter_num = 0
current_chapter_title = ""
current_chapter_text = []

for line in chapter_lines:
    line = line.strip()
    if not line:
        continue

    match = re.match(regex_chapter, line)

    if match:
        # 匹配到新的章节标题行，保存上一个章节
        if current_chapter_num != 0:
            cleaned_text = clean_chapter_text(" ".join(current_chapter_text))

            # 只有内容长度大于50才视为有效章节
            if len(cleaned_text) >= 50:
                chapter_data.append({
                    '卷名': '上卷' if current_chapter_num <= 30 else '下卷',
                    '章节编号': current_chapter_num,
                    '章节名称': current_chapter_title,
                    '清洗后文本': cleaned_text,
                    '文本长度': len(cleaned_text)
                })

        # 开始新的章节
        try:
            current_chapter_num = int(match.group(1))
        except ValueError:
            continue

        current_chapter_title = match.group(2).strip()
        current_chapter_text = []
        print(f"✅ 找到章节: {current_chapter_num} {current_chapter_title}")
    else:
        # 匹配失败，说明是正文内容，将其添加到当前章节的文本列表
        current_chapter_text.append(line)

# 保存最后一个章节
if current_chapter_num != 0 and current_chapter_text:
    cleaned_text = clean_chapter_text(" ".join(current_chapter_text))
    if len(cleaned_text) >= 50:
        chapter_data.append({
            '卷名': '上卷' if current_chapter_num <= 30 else '下卷',
            '章节编号': current_chapter_num,
            '章节名称': current_chapter_title,
            '清洗后文本': cleaned_text,
            '文本长度': len(cleaned_text)
        })


# ----------------- 6. 结构化输出与保存 -----------------
df_chapters = pd.DataFrame(chapter_data)

print("\n🎉 章节分割与基础清洗结果预览：")
print(df_chapters[['卷名', '章节编号', '章节名称', '文本长度']].head(10))
print("-" * 50)
print(f"总共提取了 {len(df_chapters)} 个章节。")

# 保存为 CSV 文件
df_chapters.to_csv('hong_yu_hei_chapters_cleaned.csv', index=False, encoding='utf-8-sig')
print("\n✅ 已将清洗后的章节数据保存到 hong_yu_hei_chapters_cleaned.csv")
