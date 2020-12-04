import csv
import math
import re
import string
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import scipy as sp
import seaborn as sns
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn import decomposition, svm
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from wordcloud import STOPWORDS, WordCloud
from utils import sliceDataFrame

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def strip_strange_symbols(text):
    return re.sub(r'[\W_]+', ' ', text)

def to_lower_case(text):
    return text.lower()

# Removing the square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

# Removing URL's
def remove_urls(text):
    return re.sub(r'http\S+', '', text)

# Removing the stopwords from text
def remove_stopwords(text):
    final_text = []
    for i in text.split():
        if i.strip().lower() not in stop:
            final_text.append(i.strip())
    return " ".join(final_text)

# Doing stemming
def lemmatize(text):
    word_filtered = []
    for i in text.split():
        word_tokens = word_tokenize(i)
        for w in word_tokens:
            w = lemmatizer.lemmatize(w, pos='v')
            word_filtered.append(w)
    return " ".join(w for w in word_filtered)

#R emoving the noisy text
def denoise_text(text):
    text = strip_html(text)
    text = strip_strange_symbols(text)
    text = to_lower_case(text)
    text = remove_between_square_brackets(text)
    text = remove_urls(text)
    text = remove_stopwords(text)
    text = lemmatize(text)
    return text

# perform principal component analysis
def principal_component_analysis(X,search=False):
    print(f'B: n_samples = {len(X)}, n_features = {len(X[0])}')
    if search == False:
        pca = decomposition.PCA(n_components=len(X),svd_solver='auto')
        pca.fit(X)
    else:
        n_min,n_max = 1,int(min(len(X),len(X[0])))
        n = int((n_min + n_max) / 2)
        score = -math.inf
        while True:
            pca = decomposition.PCA(n_components=n,svd_solver='auto')
            pca.fit(X)
            score = np.cumsum(pca.explained_variance_ratio_)[-1]
            print(f'n_components = {n} => score = {score}')
            if score < 0.95:
                n = int((n + n_max) / 2)
                n_min = n
            else:
                break
    X = pca.transform(X)
    print(f'A: n_samples = {len(X)}, n_features = {len(X[0])}')
    return X

def load_and_preprocess(sliceAmount=-1):
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    try:
        # Tenta carregar os data sets ja processado do disco
        print('Attempting to load data from cached data set...')
        X = np.load(f'./assets/X_{sliceAmount}.npy',allow_pickle=True)
        Y = np.load(f'./assets/Y_{sliceAmount}.npy',allow_pickle=True)
        print('Data successfully loaded from cached files.')
    except OSError:
        print('Unable to load cached data set. Loading from original files...')
        # Carrega o data set inteiro (21417+23537=44954 noticias)
        if sliceAmount == -1:
            true = pd.read_csv('./assets/True.csv')
            false = pd.read_csv('./assets/Fake.csv')
        # Carrega o data set inteiro e seleciona 'sliceAmount' noticias
        else:
            sliceDataFrame(sliceAmount)
            true = pd.read_csv(f'./assets/True_{sliceAmount}.csv')
            false = pd.read_csv(f'./assets/Fake_{sliceAmount}.csv')
        print('Data successfully loaded from original files.')

        global lemmatizer
        global stop

        lemmatizer = WordNetLemmatizer()
        stop = set(stopwords.words('english'))

        true['category'] = 1
        false['category'] = -1

        df = pd.concat([true, false])

        Y = df['category']
        Y = [Y.to_numpy()]
        Y = np.transpose(Y)

        print('Title')
        print(df.title.count())
        print('Subject')
        print(df.subject.value_counts())

        df['text'] = df['text'] + " " + df['title']

        del df['title']
        del df['subject']
        del df['date']
        if 'Unnamed: 0' in df.columns:
            del df['Unnamed: 0']

        punctuation = list(string.punctuation)
        stop.update(punctuation)

        print(f'Performing denoise_text...')
        df['text'] = df['text'].apply(denoise_text)

        print(f'Performing TF-IDF vectorization...')
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['text']).toarray()
        X = StandardScaler().fit_transform(X)

        print(f'Performing principal component analysis...')
        X = principal_component_analysis(X)

    # cache data set to filesystem (numpy file format)
    np.save(f'./assets/X_{sliceAmount}.npy', X)
    np.save(f'./assets/Y_{sliceAmount}.npy', Y)
    print('Data set successfully cached for further reuse.')

    return X, Y
