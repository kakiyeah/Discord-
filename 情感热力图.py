import pandas as pd
pd.set_option("display.max_columns",None)
import jieba
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#解决中文显示问题
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
plt.rcParams.update({'font.size': 12.5})



def get_sentiment_dict():
    df = pd.read_excel(r'E:\新桌面\情感词汇.xlsx')
    print(df.head())  # 打印 DataFrame 的前几行，以查看其内容

    # 整理情绪列表
    Joy = []
    Like = []
    Surprise = []
    Anger = []
    Depress = []
    Fear = []
    Dislike = []
    for idx, row in df.iterrows():
        sentiment_category = str(row['情感分类']).strip()
        if sentiment_category in ['PA', 'PE']:
            Joy.append(row['词语'])
        if sentiment_category in ['PD', 'PH', 'PG', 'PB', 'PK']:
            Like.append(row['词语'])
        if sentiment_category in ['PC']:
            Surprise.append(row['词语'])
        if sentiment_category in ['NA']:
            Anger.append(row['词语'])
        if sentiment_category in ['NB', 'NJ', 'NH', 'PF']:
            Depress.append(row['词语'])
        if sentiment_category in ['NI', 'NC', 'NG']:
            Fear.append(row['词语'])
        if sentiment_category in ['NE', 'ND', 'NN', 'NK', 'NL']:
            Dislike.append(row['词语'])
    Positive = Joy + Like + Surprise
    Negative = Anger + Depress + Fear + Dislike
    print(df['情感分类'].unique())  # 打印出所有独特的“情感分类”值，以验证过滤条件
  
    print('情绪词语列表整理完成')
    print('Joy:', Joy[:5])  # 打印前5个“喜悦”类词汇作为示例
    print('Like:', Like[:5])  # 同上
    print('Surprise:', Surprise[:5])  # 同上
    return Joy , Like , Surprise,Anger , Depress , Fear , Dislike,Positive,Negative

Joy , Like , Surprise,Anger , Depress , Fear , Dislike,Positive,Negative = get_sentiment_dict()


    

def emotion_caculate(text):
    positive = 0
    negative = 0
    anger = 0
    dislike = 0
    fear = 0
    depress = 0
    surprise = 0
    like = 0
    joy = 0
    none = 0
    wordlist = text.split(" ")
    wordset = set(wordlist)

    for word in wordset:
        freq = wordlist.count(word)
        if word in Positive:
            positive+=freq
        if word in Negative:
            negative+=freq
        if word in Anger:
            anger+=freq
        if word in Dislike:
            dislike+=freq
        if word in Fear:
            fear+=freq
        if word in Depress:
            depress+=freq
        if word in Surprise:
            surprise+=freq
        if word in Like:
            like+=freq
        if word in Joy:
            joy+=freq

    emotion_info = {
        'length':len(wordlist),
        'positive': positive,
        'negative': negative,
        'anger': anger,
        'dislike': dislike,
        'fear':fear,
        'like':like,
        'depress':depress,
        'surprise':surprise,
        'joy':joy,
    }

    if positive>negative:
        polarity = '正面'
    elif positive==negative:
        polarity = '中立'
    else:
        polarity = '负面'

    dict = {'Anger': anger,
        'Dislike': dislike,
        'Fear':fear,
        'Like':like,
        'Depress':depress,
        'Surprise':surprise,
        'Joy':joy,}
    sentiment_type = max(dict.items(), key=lambda x: x[1])[0]

    if dict[sentiment_type]==0:
        sentiment_type = 'None'

    return sentiment_type,polarity,str(emotion_info)


def sentiment_analysis(path):
    data_df = pd.read_csv(path, encoding='GBK')
    content = data_df['content'].to_list()
    content = [' '.join(jieba.lcut(str(s))) for s in content]
    types = []
    polaritys = []
    details = []
    for i in range(len(content)):
        if pd.isna(content[i]):
            sentiment_type, polarity, detail = emotion_caculate("")
        else:
            sentiment_type, polarity, detail = emotion_caculate(content[i])
        types.append(sentiment_type)
        polaritys.append(polarity)
        details.append(detail)

    data_df['情感类别'] = types
    data_df['情感极性'] = polaritys
    data_df['情感词汇统计'] = details
    data_df.to_csv(path, encoding='GBK', index=False)



def draw(path,savepath,order=None):
    df = pd.read_csv(path,encoding='GBK')
    df = df[df["情感类别"]!="None"]

    w = df.groupby(['newTime','情感类别'], as_index=False).count()
    w=w.loc[:,['newTime','情感类别','AuthorID']]

    w.columns = ['时间','情感','Count']
    data_heatmap = w.pivot( index='情感',columns='时间' ,values='Count')

    data_heatmap = data_heatmap.reindex(index=['Like','Depress','Anger','Dislike','Fear', 'Joy','Surprise'],fill_value=0)

    print(data_heatmap)

    if order!=None:
       data_heatmap = data_heatmap[order]

    pic = sns.heatmap(data_heatmap, fmt="d", cmap='gist_heat_r', annot=False)

    plt.tight_layout()
    plt.savefig(savepath)
    plt.show()

sentiment_analysis(r"E:\新桌面\文本2.csv")
draw(r"E:\新桌面\文本2.csv","result/情感热力图.png")

