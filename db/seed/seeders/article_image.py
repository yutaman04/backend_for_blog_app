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
from models.article_image import ArticleImage
import hashlib



db = database.SessionLocal()
  
def seed():
    sample_image_list = [
        {
            "artile_id": 1,
            "image_name": "DSC_9380.JPG",
            "sort_order": 1,
            "create_user_id": 1,
        },
        {
            "artile_id": 3,
            "image_name": "DSC_9379.JPG",
            "sort_order": 1,
            "create_user_id": 1,
        },
    ]
    
    try:
        print("開始:articles")
        for article_image in sample_image_list:
            tmp_article_image = ArticleImage()
            tmp_article_image.article_id = article_image["artile_id"]
            tmp_article_image.image_name = article_image["image_name"]
            tmp_article_image.sort_order = article_image["sort_order"]
            tmp_article_image.create_user_id = article_image["create_user_id"]
            db.add(tmp_article_image)
            
        db.commit()
        print("完了:articles")
    except Exception as e:
        print("失敗:articles")
        print(e)
        db.rollback()