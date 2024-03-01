from snownlp import SnowNLP
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white', {'font.sans-serif': ['simhei','FangSong']})

def get_sentiment_score(data_path):
    data_path=r"E:\新桌面\文本2.csv"
    df = pd.read_csv(data_path, encoding='GB18030')
    texts = df['content'].to_list()
    scores = []
    for i in texts:
        s = SnowNLP(i)
        print(s.sentiments) # 越接近0越负面，越接近1越正面
        scores.append(s.sentiments)
    df['sentiment_score'] = scores


df = pd.DataFrame({
    'newTime': ['2308', '2309', '2310','2311','2312','2401','2402'],
    'sentiment_score': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
})

# 将newTime列转换为datetime类型
df['newTime'] = pd.to_datetime(df['newTime'], format='%y%m')

# 按照时间排序
df.sort_values(by='newTime', inplace=True)

# 查看转换和排序后的DataFrame
print(df)



def get_sentiment_score(data_path):
    data_path=r"E:\新桌面\文本2.csv"
    df = pd.read_csv(data_path, encoding='utf-8')
    # 确保文本列名为'content'
    texts = df['content'].astype(str).to_list()
    scores = []
    for i in texts:
        s = SnowNLP(i)
        scores.append(s.sentiments)
    df['sentiment_score'] = scores
    return df  # 返回包含情感得分的DataFrame

def draw(df):  # 修改draw函数以接受DataFrame作为参数
    send_df = df[df['isSend'] == 1]
    receive_df = df[df['isSend'] == 0]
    send_mean = send_df.groupby('newTime')['sentiment_score'].mean()
    receive_mean = receive_df.groupby('newTime')['sentiment_score'].mean()
    
    # Assuming send_mean and receive_mean are Series obtained from groupby and mean operations
    new_df = pd.DataFrame({
    "月份": list(send_mean.index) + list(receive_mean.index),
    "情感得分均值": list(send_mean.values) + list(receive_mean.values),  # Use .values here
    "is_send": ['send'] * len(send_mean) + ['receive'] * len(receive_mean)
})
    sns.lineplot(x="月份", y="情感得分均值", hue="is_send",data=new_df)
    import os

    directory = "result"

# 检查目录是否存在
    if not os.path.exists(directory):
    # 如果不存在，创建它
        os.makedirs(directory)

    plt.savefig(f"{directory}/情感得分随时间变化.png")

    
    plt.show()


# 首先调用get_sentiment_score函数，并将结果DataFrame传递给draw函数
df = get_sentiment_score(r"E:\新桌面\文本2.csv")
draw(df)



