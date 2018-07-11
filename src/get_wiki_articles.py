'''
1. get_wiki_articles  <-- HERE
2. score_articles
3. get_player_article
4. get_wiki_view_stats

Get wiki articles using each baseball player name as the search term.
Maximum 10 relevant articles are retrieved and stored for each player.
Files are broken up in to chunks of 1000 players
'''

import pandas as pd
import requests
import os

DEST_BASE_URL = 'H:/baseball/wiki_articles/'
API_URL = 'https://en.wikipedia.org/w/api.php'
MAX_COUNTER = 1000

def main():
	df = pd.read_csv('../../data/raw/baseball/Master.csv')
	df['nameFull'] = df['nameGiven'] + ' ' + df['nameLast']
	df = df[df['nameFull'].notnull()]

	#df = df.sample(n=1200)

	search_params = {
		'action' : 'query',
		'format' : 'json',
		'list' : 'search',
		#'srsearch' : 'search term',
		'srlimit' : 10
	}

	get_article_params = {
		'action' : 'query',
		'format' : 'json',
		'prop' : 'revisions',
		#'pageids' : '36494510|11173690|156002',
		'rvprop' : 'content'
	}

	counter=0
	master_counter=0
	article_data = []
	for playerid, name in zip(df['playerID'], df['nameFull']):
		print(name)
		search_params['srsearch'] = name
		results = requests.get(API_URL, params=search_params).json() #search for wiki articles based on search term

		if len(results['query']['search'])>0: #if search came back with hits
			pageids = '|'.join([str(r['pageid']) for r in results['query']['search']]) 
			get_article_params['pageids'] = pageids
			results = requests.get(API_URL, params=get_article_params).json() #get all articles returned from search
			pages = results['query']['pages']

			for key in pages:
				text = pages[key]['revisions'][0]['*']
				title = pages[key]['title']
				article_data.append({
					'id' : playerid,
					'name' : name,
					'pageid' : key,
					'title' : title,
					'text' : text
				})
		else: #if no hits from search then append a dummy row for this player
			article_data.append({
				'id' : playerid,
				'name' : name,
				'pageid' : None,
				'title' : None,
				'text' : None
			})

		counter+=1
		master_counter+=1
		if counter==MAX_COUNTER:
			filename = 'data_' + str(master_counter) + '.csv'
			pd.DataFrame(article_data).to_csv(os.path.join(DEST_BASE_URL,filename), index=False)
			counter=0
			article_data=[]

	if len(article_data)>0:
		filename = 'data_' + str(master_counter) + '.csv'
		pd.DataFrame(article_data).to_csv(os.path.join(DEST_BASE_URL,filename), index=False)


if __name__ == '__main__':
	main()