import pandas as pd
import requests
from bs4 import BeautifulSoup


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


def main():
    df = pd.read_csv('anime2.csv', index_col='anime_id')
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
        print(rating)
        if rating == 'None':
            df.at[anime_id, 'rating'] = '?'
            continue
        df.at[anime_id, 'rating'] = rating

    print(non_existent_anime)

    df.to_csv(
        'new_anime.csv')  # Due to captcha, there might be a need to rerun the code to save progress, rename new_anime.csv to anime2.csv and rerun code


if __name__ == '__main__':
    main()
