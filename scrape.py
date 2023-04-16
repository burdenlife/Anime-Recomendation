import pandas as pd
import requests
import json
from time import sleep


def get_episodes(response):
    # Parse episode length from html
    soup = json.loads(response)
    return soup['data']['episodes']


def blank_episodes(data):
    return data.index[data['episodes'].isnull()].tolist()


def get_rating(response):
    soup = json.loads(response)
    rating = soup['data']['rating']
    if not rating:
        return
    return rating.split()[0]

def blank_ratings(data):
    return data.index[data['rating'].isnull()].tolist()


def get_year(response):
    soup = json.loads(response)
    return soup['data']['year']

def blank_year(data):
    return data.index[data['start_year'].isnull()].tolist()


def get_type(response):
    soup = json.loads(response)
    return soup['data']['type']

def blank_type(data):
    return data.index[data['type'].isnull()].tolist()


def blank_source(data):
    return data.index[data['source'].isnull()].tolist()


def get_source(response):
    soup = json.loads(response)
    return soup['data']['source']

def main():
    df = pd.read_csv('relevant_anime_data.csv', index_col='anime_id')
    no_episodes = blank_episodes(df)
    non_existent_anime = []
    for anime_id in no_episodes:
        sleep(1.5)
        response = requests.get("https://api.jikan.moe/v4/anime/{}".format(anime_id))
        if response.status_code == 429:
            print(response.status_code, anime_id)
            break
        elif response.status_code != 200:
            print(response.status_code, anime_id)
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'episodes'] = "Error 404"
            continue

        episodes = get_episodes(response.text)
        if not episodes:
            df.at[anime_id, 'episodes'] = '?'
            continue
        df.at[anime_id, 'episodes'] = episodes

    print('Finished for "episodes" now starting "ratings"')

    df.to_csv('temp.csv') #saving data to file in case of crash

    sleep(10)

    no_rating = blank_ratings(df)

    for anime_id in no_rating:
        sleep(1.5)
        response = requests.get("https://api.jikan.moe/v4/anime/{}/".format(anime_id))
        if response.status_code == 429:
            print(response.status_code, anime_id)
            break
        elif response.status_code != 200:
            print(response.status_code, anime_id)
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'rating'] = "Error 404"
            continue

        rating = get_rating(response.text)
        if not rating:
            df.at[anime_id, 'rating'] = '?'
            continue
        df.at[anime_id, 'rating'] = rating

    print('Finished for "ratings" now starting "start_year"')

    df.to_csv('temp.csv')  # saving data to file in case of crash

    sleep(10)

    no_year = blank_year(df)

    for anime_id in no_year:
        sleep(1.5)
        response = requests.get("https://api.jikan.moe/v4/anime/{}/".format(anime_id))
        if response.status_code == 429:
            print(response.status_code, anime_id)
            break
        elif response.status_code != 200:
            print(response.status_code, anime_id)
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'start_year'] = "Error 404"
            continue
        start_year = get_year(response.text)
        if not start_year:
            df.at[anime_id, 'start_year'] = '?'
            continue
        df.at[anime_id, 'start_year'] = start_year

    print('Finished for "start_year" now starting "type"')

    df.to_csv('temp.csv')  # saving data to file in case of crash

    sleep(10)

    no_type = blank_type(df)

    for anime_id in no_type:
        sleep(1.5)
        response = requests.get("https://api.jikan.moe/v4/anime/{}/".format(anime_id))
        if response.status_code == 429:
            print(response.status_code, anime_id)
            break
        elif response.status_code != 200:
            print(response.status_code, anime_id)
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'type'] = "Error 404"
            continue
        anime_type = get_type(response.text)
        if not anime_type:
            df.at[anime_id, 'type'] = '?'
            continue
        df.at[anime_id, 'type'] = anime_type

    print('Finished for "type" now starting "source"')

    df.to_csv('temp.csv')  # saving data to file in case of crash

    sleep(10)

    no_source = blank_source(df)

    for anime_id in no_source:
        sleep(1.5)
        response = requests.get("https://api.jikan.moe/v4/anime/{}/".format(anime_id))
        if response.status_code == 429:
            print(response.status_code, anime_id)
            break
        elif response.status_code != 200:
            print(response.status_code, anime_id)
            non_existent_anime.append(anime_id)  # These anime are no longer on myanimelist.net
            df.at[anime_id, 'source'] = "Error 404"
            continue
        anime_source = get_source(response.text)
        if not anime_source:
            df.at[anime_id, 'source'] = '?'
            continue
        df.at[anime_id, 'source'] = anime_source
    print(non_existent_anime)

    df.to_csv(
        'new_anime2.csv')


if __name__ == '__main__':
    main()


