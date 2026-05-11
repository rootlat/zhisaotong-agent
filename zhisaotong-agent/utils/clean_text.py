import re

def clean_text(text, min_sentence_len=6):
    """
    一键清洗文本中的无效信息：网址、表情、@、话题、特殊符号、空行、重复内容、过短无效句
    :param text: 原始文本
    :param min_sentence_len: 最小有效句子长度（默认6）
    :return: 清洗后的干净文本
    """
    # 1. 清洗网址、@、话题、emoji、特殊符号
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'@[\w\u4e00-\u9fa5]+', '', text)
    text = re.sub(r'#.*?#', '', text)
    text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', text)
    text = re.sub(r'[#$%^&*+=_~<>｜…]', '', text)

    # 2. 处理空行、空格
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)

    # 3. 去重
    lines = text.split('\n')
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    # 4. 过滤过短无效句子
    final_lines = [line for line in unique_lines if len(line) >= min_sentence_len]

    return '\n'.join(final_lines)