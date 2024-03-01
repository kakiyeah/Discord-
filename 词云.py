import pandas as pd
import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from opencc import OpenCC

def remove_links(text):
    # 正则表达式匹配并去除链接
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

def convert_traditional_to_simplified(text):
    cc = OpenCC('t2s')
    return cc.convert(text)

def get_wordcloud(data_path, save_path, is_send=0):
    df = pd.read_csv(data_path, encoding='utf-8')
    texts = df[df['isSend']==is_send]['content'].to_list()

    with open(r"E:\新桌面\CNstopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]

    norm_texts = []
    for text in texts:
        if not isinstance(text, str):
            continue  # Skip if text is not a string

        text = remove_links(text)
        text = convert_traditional_to_simplified(text)
        words = jieba.lcut(text)
        words = [word for word in words if word not in stopwords and len(word) > 1]
        norm_texts.extend(words)

    if not norm_texts:
        print("No valid words for word cloud.")
        return

    count_dict = dict(Counter(norm_texts))
    wc = WordCloud(font_path="data/simhei.ttf", background_color='white').fit_words(count_dict)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    wc.to_file(save_path)

# 示例：绘制对方发送的信息的词云图
get_wordcloud(r"E:\新桌面\文本2.csv", "result/词云-他发的.png", is_send=0)


