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
