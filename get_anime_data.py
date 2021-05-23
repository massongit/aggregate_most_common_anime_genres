import json
import os
import re
import urllib

import requests

dir_name = 'results'

with open(os.path.join(dir_name, 'genres.json')) as f:
    genres = json.load(f)

animes = []
genre_not_found_animes = {}
next_page = 1

while next_page is not None:
    params = {}

    if 1 < next_page:
        params['page'] = next_page

    res = requests.get('https://api.annict.com/v1/me/works',
                       params=params,
                       headers={'Authorization': f'Bearer {os.environ.get("ANNICT_PERSONAL_ACCESS_TOKEN")}'})
    print(f'GET {res.url}')
    print()
    res_json = res.json()

    url_pattern = re.compile(r'https?://ja\.wikipedia\.org/wiki/')

    for anime in res_json['works']:
        if anime['status']['kind'] == 'no_select':
            raise Exception(f"Kind is not set: {anime['title']}")

        anime.setdefault('genres', list())
        anime_name = url_pattern.sub('', urllib.parse.unquote(anime['wikipedia_url'].split('#')[0]))

        if anime_name in genres:
            anime['genres'] = genres[anime_name]
        else:
            genre_not_found_anime = {k: anime[k] for k in ['title', 'wikipedia_url']}
            genre_not_found_animes[int(anime['id'])] = genre_not_found_anime
            print('[genres not found]')

            for v in genre_not_found_anime.values():
                print(v)

            print()

        animes.append(anime)

    if res_json['next_page']:
        next_page = res_json['next_page']
    else:
        next_page = None

os.makedirs(dir_name, exist_ok=True)

with open(os.path.join(dir_name, 'animes.json'), 'w') as f:
    json.dump(animes, f, ensure_ascii=False, sort_keys=True, indent=4)

with open(os.path.join(dir_name, 'genre_not_found_animes.json'), 'w') as f:
    json.dump(genre_not_found_animes, f, ensure_ascii=False, sort_keys=True, indent=4)
