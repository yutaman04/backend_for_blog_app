import os
import sys
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, './../../'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)
print(project_root)

import database
from models.article import Article
import hashlib



db = database.SessionLocal()
  
def seed():
    sample_article_list = [
        {
            "category_id": 1,
            "title": "雑記記事のサンプルタイトル1",
            "content": "雑記記事サンプルの本文1",
        },
        {
            "category_id": 1,
            "title": "雑記記事のサンプルタイトル2",
            "content": "雑記記事サンプルの本文2",
        },
        {
            "category_id": 1,
            "title": "雑記記事のサンプルタイトル3",
            "content": "雑記記事サンプルの本文3",
        },
        {
            "category_id": 2,
            "title": "プログラミング記事のサンプルタイトル1",
            "content": "プログラミング記事サンプルの本文1",
        },
        {
            "category_id": 2,
            "title": "プログラミング記事のサンプルタイトル2",
            "content": "プログラミング記事サンプルの本文2",
        },
    ]
    
    try:
        print("開始:articles")
        for article in sample_article_list:
            tmp_article = Article()
            tmp_article.category_id = article["category_id"]
            tmp_article.title = article["title"]
            tmp_article.content = article["content"]
            tmp_article.create_user_id = 1
            db.add(tmp_article)
            
        db.commit()
        print("完了:articles")
    except Exception as e:
        print("失敗:articles")
        print(e)
        db.rollback()