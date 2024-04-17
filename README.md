# backend_for_blog_app
ブログアプリのバックエンドアプリ

# DBマイグレーション
- モデル定義：/db/models配下にあるsqlalchemyによる定義
- マイグレーションツール：alembic

## マイグレーション方法
### マイグレーションファイル生成

```
alembic revision --autogenerate
```

### マイグレーション実行
最新のVersionまでマイグレーション
```
alembic upgrade head
```
1つだけVersionを上げたいなどの場合は、headの部分を+1とかにする

### ロールバック
初期状態まで戻したい場合
```
alembic downgrade base
```
1つ前のVersionに戻したい場合は、baseの部分を-1にする

## 初期データ投入
マイグレーション実行後、db/seed/run_seed.pyを実行すれば初期データ投入される
```
/app # python db/seed/run_seed.py
Seeding data...
開始
開始:categories
完了:categories
開始:users
完了:users
開始:articles
完了:articles
完了
/app # 
```
