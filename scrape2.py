import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from time import sleep


def get_episodes(soup):
    # Parse episode length from html
    episodes = soup.find(id='curEps')
    episode = str(episodes).split('">')[-1].split('</')[0]
    return episode


def blank_episodes(data):
    return data.index[data['episodes'].isnull()].tolist()


def get_rating(response):
    index = response.split('>').index('Rating:</span')
    rating = response.split('>')[index + 1].split()[0]
    return rating


def blank_ratings(data):
    return data.index[data['rating'].isnull()].tolist()


def get_year(response):
    index = response.split('>').index('Aired:</span')
    pattern = '\d\d\d\d'
    year = response.split('>')[index + 1]
    match = re.search(pattern, year)
    if match:
        return match.group()
    else:
        return 'None'

def blank_year(data):
    return data.index[data['start_year'].isnull()].tolist()


def get_type(response):
    index = response.split('>').index('Type:</span')
    anime_type = response.split('>')[index + 2].split('<')[0]
    if anime_type == '\n\n': #This is the output if type is unknown
        return 'None'
    return anime_type

def blank_type(data):
    return data.index[data['type'].isnull()].tolist()


def blank_source(data):
    return data.index[data['source'].isnull()].tolist()


def get_source(response):
    index = response.split('>').index('Source:</span')
    source = response.split('>')[index + 1].split()[0] #Light Novel will return Light

    if source in ('Light', 'Web', 'Visual') :
        source = "_".join(response.split('>')[index+1].split()[:2])
    return source

def main():
    df = pd.read_csv('new_anime.csv', index_col='anime_id')
    no_episodes = blank_episodes(df)
    non_existent_anime = []
    for anime_id in no_episodes:
        response = requests.get("https://myanimelist.net/anime/{}/".format(anime_id))
        if response.status_code == 404:
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'episodes'] = "Error 404"
            continue
        elif response.status_code != 200:  # This is due to captcha system on MAL. IP must be refreshed to rerun code
            print(anime_id)
            print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        episodes = get_episodes(soup)
        if episodes == 'None':
            df.at[anime_id, 'rating'] = '?'
            continue
        df.at[anime_id, 'episodes'] = episodes
        sleep(0.025)

    no_rating = blank_ratings(df)

    for anime_id in no_rating:
        response = requests.get("https://myanimelist.net/anime/{}/".format(anime_id))
        if response.status_code == 404:
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'rating'] = "Error 404"
            continue
        elif response.status_code != 200:
            print(anime_id)
            print(response.status_code)
            break
        rating = get_rating(response.text)
        if rating == 'None':
            df.at[anime_id, 'rating'] = '?'
            continue
        df.at[anime_id, 'rating'] = rating
        sleep(0.025)

    no_year = blank_year(df)

    for anime_id in no_year:
        response = requests.get("https://myanimelist.net/anime/{}/".format(anime_id))
        if response.status_code == 404:
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'start_year'] = "Error 404"
            continue
        elif response.status_code != 200:
            print(anime_id)
            print(response.status_code)
            break
        start_year = get_year(response.text)
        if start_year == 'None':
            df.at[anime_id, 'start_year'] = '?'
            continue
        df.at[anime_id, 'start_year'] = start_year
        sleep(0.025)

    no_type = blank_type(df)

    for anime_id in no_type:
        response = requests.get("https://myanimelist.net/anime/{}/".format(anime_id))
        if response.status_code == 404:
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'type'] = "Error 404"
            continue
        elif response.status_code != 200:
            print(anime_id)
            print(response.status_code)
            break
        anime_type = get_type(response.text)
        if anime_type == 'None':
            df.at[anime_id, 'type'] = '?'
            continue
        df.at[anime_id, 'type'] = anime_type
        sleep(0.025)

    no_source = blank_source(df)

    for anime_id in no_source:
        response = requests.get("https://myanimelist.net/anime/{}/".format(anime_id))
        if response.status_code == 404:
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'source'] = "Error 404" #To avoid revisiting the url
            continue
        elif response.status_code != 200:
            print(anime_id)
            print(response.status_code)
            break
        anime_source = get_source(response.text)
        if anime_source == 'Unknown':
            df.at[anime_id, 'type'] = '?'
            continue
        df.at[anime_id, 'source'] = anime_source
        sleep(0.025)



    print(non_existent_anime)

    df.to_csv(
        'new_anime.csv')  # Due to captcha, there might be a need to rerun the code to save progress, rename new_anime.csv to relevant_anime_data.csv and rerun code


if __name__ == '__main__':
    main()

