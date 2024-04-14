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
from models.category import Category
import hashlib



db = database.SessionLocal()
  
def seed():
    category_names = [
        '雑記',
        'プログラミング',
        'TypeScript',
        'AWS',
        '趣味',
    ]
    try:
        print("開始:categories")
        categories = [Category(category_name=name) for name in category_names]
        
        for category in categories:
            db.add(category)
        db.commit()
        print("完了:categories")
    except Exception as e:
        print("失敗:categories")
        print(e)
        db.rollback()