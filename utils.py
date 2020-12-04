import math
import numpy as np
import pandas as pd
from sklearn import decomposition

def exponentialList(len):
    upper_exp = np.ceil(np.log2(len))-1
    numbers = np.logspace(start=0,stop=upper_exp,num=upper_exp+1,base=2,dtype='int')+1
    numbers[0] = numbers[0]-1
    return numbers

def sliceDataFrame(sliceAmount):
    # n_news - Quantidade de cada tipo de notícias que estará no dataframe reduzido
    n_news = list(range(sliceAmount))

    fake_csv = pd.read_csv('./assets/Fake.csv')
    true_csv = pd.read_csv('./assets/True.csv')

    fake_csv.loc[n_news].to_csv(f'./assets/Fake_{sliceAmount}.csv')
    true_csv.loc[n_news].to_csv(f'./assets/True_{sliceAmount}.csv')

def plots(df):
    # Grafico de quantidade de noticias divididas entre True e Fake
    # sns.set_style("darkgrid")
    # veracityChart = sns.countplot(data=df, x="category")
    # plt.title('Number of news divided in True or Fake')
    # for p in veracityChart.patches:
    #     veracityChart.annotate(p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')

    # Grafico de quantidade de noticias divididas entre seus assuntos
    # plt.figure(figsize = (12,8))
    # sns.set(style = "whitegrid",font_scale = 1.2)
    # subjectChart = sns.countplot(x = "subject", hue = "category" , data = df )
    # plt.title('Number of news divided in subjects')
    # for p in subjectChart.patches:
    #     subjectChart.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2, p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
    # subjectChart.set_xticklabels(subjectChart.get_xticklabels(),rotation=90)
    pass

def wordcloud(df):
    # plt.figure(figsize = (20,20)) # Text that is not Fake
    # wc = WordCloud(max_words = 2000 , width = 1600 , height = 800 , stopwords = STOPWORDS).generate(" ".join(df[df.category == 1].text))
    # plt.imshow(wc , interpolation = 'bilinear')
    # plt.title('Most used words in authentic news')

    # plt.figure(figsize = (20,20)) # Text that is not Fake
    # wc = WordCloud(max_words = 2000 , width = 1600 , height = 800 , stopwords = STOPWORDS).generate(" ".join(df[df.category == -1].text))
    # plt.imshow(wc , interpolation = 'bilinear')
    # plt.title('Most used words in fake news')
    pass
