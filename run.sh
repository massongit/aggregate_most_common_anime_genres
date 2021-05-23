#!/bin/bash

until (echo "SELECT 0;" | mysql -h db -u root -p"${MYSQL_ROOT_PASSWORD}" -D "${MYSQL_DATABASE}" -P "${MYSQL_TCP_PORT}"); do
  echo "Waiting MySQL..."
  sleep 10
done

echo "MySQL connected!"

dump_env=jawiki
dump_date=$(curl https://dumps.wikimedia.org/jawiki/ | grep "<a" | sed -r 's:.*href="([^"/]+).*:\1:g' | grep "^[0-9]" | sort | tail -n 1)
dump_dir_name=wiki_dump_data

for kind in categorylinks page; do
  file_name_sql="${dump_env}-${dump_date}-${kind}.sql"
  file_name_gz="${file_name_sql}.gz"
  file_path_aql="${dump_dir_name}/${file_name_sql}"
  if [ ! -f "${file_path_aql}" ]; then
    mkdir -p ${dump_dir_name}
    wget -P "${dump_dir_name}/" "https://dumps.wikimedia.org/${dump_env}/${dump_date}/${file_name_gz}"
    gunzip -c "${dump_dir_name}/${file_name_gz}" >"${file_path_aql}"
    mysql -h db -u root -p"${MYSQL_ROOT_PASSWORD}" -D "${MYSQL_DATABASE}" -P "${MYSQL_TCP_PORT}" <"${file_path_aql}"
  fi
done

echo "Getting Wikipedia dump data is complated!"

if [ ! -f "results/genres.json" ]; then
  pipenv run python get_genre_data.py
fi

pipenv run python get_anime_data.py
pipenv run python get_most_common_genres.py
