'''
1. get_wiki_articles  
2. score_articles     
3. get_player_article     <-- HERE
4. get_wiki_view_stats

For each player and his respective relevant wiki articles, select the article with the maximum score.
Perform one last check on this article to see if it contains the word baseball in order to reduce the number of false positives.
'''

import pandas as pd
import os

SRC_BASE_PATH = 'H:/baseball/wiki_articles_scored/'
DEST_BASE_PATH = 'H:/baseball/player_articles/'

def main():
	files = os.listdir(SRC_BASE_PATH)

	for f in files:
		print(f)
		df = pd.read_csv(os.path.join(SRC_BASE_PATH, f))
		grouped_df = df.groupby('id')

		data = []
		for playerid, group in grouped_df:
			article = group[group['score']==max(group['score'])][['name','pageid','text','title']].iloc[0]
			if 'baseball' in article['text'].lower(): #last sanity check
				data.append({
					'id' : playerid,
					'name' : article['name'],
					'pageid' : article['pageid'],
					'title' : article['title']
				})
			else:
				data.append({
					'id' : playerid,
					'name' : None,
					'pageid' : None,
					'title' : None
				})

		filename = f.split('.')[0] + '_player.csv'
		pd.DataFrame(data).to_csv(os.path.join(DEST_BASE_PATH,filename), index=False)

if __name__ == '__main__':
	main()