import sqlite3
import pandas as pd
import datetime 
import pytz

from sklearn.feature_extraction.text import  TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import ast 
from ast import literal_eval

import nltk  
import string  
from heapq import nlargest

conn = sqlite3.connect('data/news.db')

df = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM Post
                               ''', conn)
# 'id', 'publication', 'scraped_datetime',
# 'headline', 'url', 'body','page_rank'

df['scraped_datetime'] = pd.to_datetime(df['scraped_datetime'])
df.set_index('scraped_datetime', inplace=True)

# begin = datetime.datetime.now().replace(hour=5,minute=0,second=0,microsecond=0)
# end = datetime.datetime.now().replace(hour=7,minute=0,second=0,microsecond=0)

begin = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane")) - datetime.timedelta(days=1)
begin = begin.replace(hour=17,minute=0,second=0,microsecond=0)
end = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane")).replace(hour=7,minute=0,second=0,microsecond=0)



today = df.loc[begin:end]
today = today.reset_index()

# print(today)

corpus = today['body']

## Create a series with indexes to return the matches
indexes = pd.Series(today.index, index=today['headline']).drop_duplicates()

# Generate the tf-idf vectors for the corpus
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

entire = today.copy()

today = today
today['Similar'] = ''

listo = []
for index, row in today.iterrows():

    # Getpairwise linear kernel scores scores
    sim_scores = list(enumerate(cosine_sim[index]))

    # Sort based on the similarity
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the 5 most similar
    sim_scores = [x for x in sim_scores if x[1] > 0.60]
    sim_scores = sim_scores[1:6]

    # Get the indices
    indices = [i[0] for i in sim_scores]
    indices.append(index)
    # Sort list so that it's similar
    indices.sort()

    # print(indices)

    if len(indices) < 2:
        indices = ''
        

    row['Similar'] = indices

    # if len(indices) > 0:
    #     print("First ", row['headline'])
    #     for story in indices:
    #         print(story)
    #         init = entire.iloc[story]
    #         print("Next ", init['headline'])

    # print(row)
    listo.append(row)

end = pd.concat(listo, axis=1).T

today_begin = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane")).replace(hour=5,minute=0,second=0,microsecond=0)

# end = end.loc[end['publication'] == 'The Guardian']
end = end.loc[end['scraped_datetime'] > today_begin]

end['Num_similar'] = end['Similar'].str.len()
# end['Num_similar'] = 10 - end['Num_similar']
end.sort_values(by=['Num_similar'], ascending=False, inplace=True)
end['Similar'] = end['Similar'].astype(str)

end.drop_duplicates(subset=['Similar'], inplace=True)
end = end.loc[end['Similar'] != '']

end = end[:1]
for index,row in end.iterrows():
    similars = row['Similar']

    similars = literal_eval(similars)

    print(similars)
    inter = entire.loc[entire.index.isin(similars)]
    # print(type(similars))

    texto = ' '.join(inter['body'].unique().tolist())
    length = texto.count(". ")
    # Remove punctuation  
    nopunc = [char for char in texto if char not in string.punctuation]  
    nopunc = ''.join(nopunc)# Remove stopwords  
    processed_text =[word for word in nopunc.split() if word.lower() not in nltk.corpus.stopwords.words('english')]

    # Create a dictionary to store word frequency  
    word_freq = {}# Enter each word and its number of occurrences  
    for word in processed_text:  
        if word not in word_freq:  
            word_freq[word] = 1  
        else:  
            word_freq[word] = word_freq[word] + 1

    # Divide all frequencies by max frequency to give store of (0, 1]
    max_freq = max(word_freq.values()) 
    for word in word_freq.keys():  
        word_freq[word] = (word_freq[word]/max_freq)

    # Create a list of the sentences in the text  
    sent_list = nltk.sent_tokenize(texto)# Create an empty dictionary to store sentence scores  
    sent_score = {}  
    for sent in sent_list:  
        for word in nltk.word_tokenize(sent.lower()):  
            if word in word_freq.keys():  
                if sent not in sent_score.keys():  
                    sent_score[sent] = word_freq[word]  
                else:  
                    sent_score[sent] = sent_score[sent] + word_freq[word]


    summary_sents = nlargest(1, sent_score, key = sent_score.get)
    summary = ' '.join(summary_sents)  

    print("Text: \n\n")
    print(texto)
    print("\n\n\n\n")
    print("Summary: \n\n")
    print(summary)
    # print(inter)

p = end
# p = p[[ 'publication','headline','page_rank', 'Similar', 'Num_similar']]


# print(p)
# print(p.columns)