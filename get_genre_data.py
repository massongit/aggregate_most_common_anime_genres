import copy
import json
import os
from contextlib import closing

import MySQLdb.cursors

with closing(MySQLdb.connect(
        host="db",
        port=int(os.environ.get('MYSQL_TCP_PORT')),
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        db=os.environ.get('MYSQL_DATABASE'),
        cursorclass=MySQLdb.cursors.DictCursor,
        charset='utf8'
)) as cnct, closing(cnct.cursor()) as cur:
    stack = [[rc] for rc in ['SFのジャンル', 'ジャンル別の映画', 'ジャンル別のゲーム', '小説のジャンル', 'ジャンル別の漫画', 'ジャンル別のアニメーション']]
    genres = dict()
    used_titles = list()

    while stack:
        cl_to = stack.pop()
        search_genre = cl_to[-1]

        for c in ['"', "'"]:
            search_genre = search_genre.replace(c, '\\' + c)

        query = f"""
            SELECT
                cl_to,
                cl_type,
                page_id,
                page_title
            FROM
            (
                SELECT
                    cl_to,
                    cl_type,
                    cl_from as page_id
                FROM categorylinks
                WHERE
                    cl_to = "{search_genre}"
            ) as a
            JOIN page as b
            USING (page_id)
            ;
            """
        print(f'Execute query: {query}')
        cur.execute(query)

        for row in cur.fetchall():
            for key in row.keys():
                if isinstance(row[key], bytes):
                    row[key] = row[key].decode()

            if row['cl_type'] == 'subcat':
                cl_type = 'category'
            else:
                cl_type = row['cl_type']

            title = row['page_title']
            titles_str = '/'.join([title, cl_type])

            if titles_str not in used_titles:
                titles = copy.deepcopy(cl_to) + [title]
                used_titles.append(titles_str)
                if cl_type == 'category':
                    stack.append(titles)
                else:
                    for genre in titles[1:-1]:
                        genres.setdefault(title, set())
                        genres[title].add(genre)

dir_name = 'results'
os.makedirs(dir_name, exist_ok=True)

with open(os.path.join(dir_name, 'genres.json'), 'w') as f:
    json.dump({k: list(v) for k, v in genres.items()}, f, ensure_ascii=False, sort_keys=True, indent=4)
