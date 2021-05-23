import collections
import json
import os

genre_counter = collections.Counter()
dir_name = 'results'

with open(os.path.join(dir_name, 'animes.json')) as f:
    animes = json.load(f)

    for anime in animes:
        if anime['status']['kind'] not in ('stop_watching', 'on_hold'):
            for genre in anime['genres']:
                genre_counter[genre] += 1

most_common_genres = []
all_count = 0

for genre, count in genre_counter.most_common():
    most_common_genres.append({'genre': genre, 'count': count})
    all_count += count

for most_common_genre in most_common_genres:
    most_common_genre['percent'] = 1.0 * most_common_genre['count'] / all_count

with open(os.path.join(dir_name, 'most_common_genres.json'), 'w') as f:
    json.dump(most_common_genres, f, ensure_ascii=False, sort_keys=True, indent=4)
