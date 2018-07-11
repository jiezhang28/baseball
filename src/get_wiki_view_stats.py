'''
1. get_wiki_articles  
2. score_articles     
3. get_player_article   
4. get_wiki_view_stats  <-- HERE

For each player with corresponding wiki article, retrieve the view stats on this article
'''

import pandas as pd 
import requests
import os
from urllib.parse import quote

SRC_BASE_URL = 'H:/baseball/player_articles'
DEST_BASE_URL = 'H:/baseball/player_wiki_stats/'
API_URL = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{}/monthly/2015010100/2018063000'

def main():
	files = os.listdir(SRC_BASE_URL)

	for f in files:
		print(f)
		df = pd.read_csv(os.path.join(SRC_BASE_URL, f))
		df = df[df['title'].notnull()]
		df['title_enc'] = df['title'].map(lambda x: quote(x.replace(' ','_')))

		stats_data = []
		bad_data = []
		for playerid, wiki_title in zip(df['id'], df['title_enc']):
			results = requests.get(API_URL.format(wiki_title))
			if results.status_code==200:
				results_json = results.json()
				for month in results_json['items']:
					stats_data.append({
						'playerID' : playerid,
						'month' : month['timestamp'],
						'views' : month['views']
					})
			else:
				bad_data.append({
					'playerID' : playerid,
					'wiki_title' : wiki_title
				})

		base_filename = f.split('.')[0]
		stats_filename = base_filename + '_stats.csv'
		bad_data_filename = base_filename + '_bad.csv'

		pd.DataFrame(stats_data).to_csv(os.path.join(DEST_BASE_URL, stats_filename), index=False)
		if len(bad_data)>0: pd.DataFrame(bad_data).to_csv(os.path.join(DEST_BASE_URL, bad_data_filename), index=False)



if __name__ == '__main__':
	main()