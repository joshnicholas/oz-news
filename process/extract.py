import sqlite3
import pandas as pd

from sklearn.feature_extraction.text import  TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

conn = sqlite3.connect('data/news.db')

df = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM Post
                               ''', conn)
# 'id', 'publication', 'scraped_datetime',
# 'headline', 'url', 'body','page_rank'

df.set_index('scraped_datetime', inplace=True)

today = df.loc['2022-03-23 05:00:00':'2022-03-23 07:00:00']
today = today.reset_index()


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
    # Sort list so that it's similar
    indices.sort()

    # print(indices)

    row['Similar'] = indices

    if len(indices) > 0:
        print("First ", row['headline'])
        for story in indices:
            print(story)
            init = entire.iloc[story]
            print("Next ", init['headline'])

    # print(row)
# p = today


# print(p)
# print(p.columns)