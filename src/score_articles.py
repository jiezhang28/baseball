'''
1. get_wiki_articles  
2. score_articles     <-- HERE
3. get_player_article
4. get_wiki_view_stats

Score each wiki article using naive-bayes classifier to determine if the article is a baseball player bio.
Using Levenschtein distance, generate score on how closely the baseball player name matches the wiki article title.
Obtain final score by calculating the harmonic mean of the two numbers above
'''

import pandas as pd
import pickle
import re
import os
from nltk import tokenize, stem, corpus
from scipy import stats
from fuzzywuzzy import fuzz

SRC_BASE_PATH = 'H:/baseball/wiki_articles/'
DEST_BASE_PATH = 'H:/baseball/wiki_articles_scored/'

stopwords = set(corpus.stopwords.words('english'))
stemmer = stem.snowball.EnglishStemmer()
def process_text(text):
	tokens = [stemmer.stem(t) for t in tokenize.word_tokenize(re.sub(r'\W', ' ', text.lower())) if t.isalpha()]
	return [t for t in tokens if t not in stopwords]

def main():
	with open('../models/baseball_clf_nb_model.p','rb') as f: nb = pickle.load(f)
	with open('../models/baseball_tfidf_vect.p','rb') as f: tfidf = pickle.load(f)

	files = os.listdir(SRC_BASE_PATH)
	for f in files:
		print(f)
		df = pd.read_csv(os.path.join(SRC_BASE_PATH, f))
		df = df[df['title'].notnull()]
		df['title_cleaned'] = df['title'].map(lambda x: re.sub(r'\(baseball\)', '', x).strip())
		df['clf'] = nb.predict_proba(tfidf.transform(df['text']))[:,1]
		df['lvs'] = [fuzz.ratio(a, b)/100 for a, b in zip(df['name'], df['title_cleaned'])]
		df['score'] = [stats.hmean([a, b]) if a>0 and b>0 else 0 for a, b in zip(df['clf'],df['lvs'])]

		filename = f.split('.')[0] + '_proc.csv'
		df.to_csv(os.path.join(DEST_BASE_PATH, filename), index=False)



if __name__ == '__main__':
	main()