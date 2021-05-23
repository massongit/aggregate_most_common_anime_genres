# よく見るアニメのジャンル集計ツール
[Annict](https://annict.jp/) に登録されたアニメの視聴履歴とWikipediaのカテゴリを元に、よく見るアニメのジャンルを集計するツールです。

## 実行方法
1. https://annict.jp/settings/apps でAnnictの `読み込み専用` の個人用アクセストークンを作成します。この際、表示されたアクセストークンを記録しておいてください。
1. 以下の内容で `.env` を作成します。
    ```.env
    ANNICT_PERSONAL_ACCESS_TOKEN={Annictの個人用アクセストークン}
    MYSQL_DATABASE={DB名 (任意)}
    MYSQL_ROOT_PASSWORD={DBのパスワード (任意)}
    MYSQL_TCP_PORT={DBのポート番号 (3306, 他のポートでも可)}
    ```
1. `docker-compose up -d` を実行します。
1. 処理が完了すると `results/most_common_genres.json` に集計結果が出力されます。

## 実行ログの閲覧方法
1. `docker-compose logs -f --tail=500 main` を実行します。
