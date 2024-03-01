import pandas as pd
import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def remove_links_and_related_words(text):
    # 使用正则表达式匹配并去除完整的链接
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # 进一步去除常见的链接相关词汇
    text = re.sub(r'\b(https?|com|net|org|www)\b', '', text)
    return text

def get_wordcloud(data_path, save_path, is_send=0):
    df = pd.read_csv(data_path, encoding='GB18030')
    texts = df[df['isSend'] == is_send]['content'].to_list()

    with open(r"E:\新桌面\CNstopwords.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        stopwords = [line.strip().replace("\ufeff", "") for line in lines]

    norm_texts = []
    for text in texts:
        if not isinstance(text, str):
            continue  # 如果text不是字符串，跳过当前循环

        text = remove_links_and_related_words(text)  # 删除链接和相关词汇
        words = jieba.lcut(text)
        res = [word for word in words if word not in stopwords and word.replace(" ", "") != "" and len(word) > 1]
        if res != []:
            norm_texts.extend(res)

    count_dict = dict(Counter(norm_texts))
    wc = WordCloud(font_path="data/simhei.ttf", background_color='white', include_numbers=False, random_state=0)
    wc = wc.fit_words(count_dict)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file(save_path)

# 示例：绘制对方发送的信息的词云图
get_wordcloud(r"E:\新桌面\文本2.csv", save_path="result/词云-他发的.png", is_send=0)



