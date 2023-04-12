anime.csv 

Original dataset taken from Kaggle

----------------------------------------

relevant_anime_data.csv 

Data of variables to be considered for clustering analysis

Anime that is not_yet_aired was removed from relevant_anime_data.csv as the data of these anime were not robust enough for analysis.


variables: 'type', 'source', 'status', 'episodes', 'start_year', 'rating, 'studios', 'source'




-------------------------------------------
scrape2.py

Static web scraper to obtain missing data from the original dataset.

Due to Captcha in myanimelist.com, the code will need to be rerun repeatedly with the incremental progress being saved in a new file.

scrape.py -> reads relevant_anime_data.csv -> scrapes missing data -> writes to new_data.csv

#
scrape2.py will self-terminate when faced with Captcha. scrape2.py will print the HTTP status on the console and write the current dataframe with newly scraped data into new_data.csv.

To rerun code with saved progress, rename new_data.csv to relevant_anime_data.csv before running. (It took me about 300 reruns to get the final data)



-------------------------------------------
new_anime.csv

The final dataset used for clustering analysis and development of recommendation algorithm

