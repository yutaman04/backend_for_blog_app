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
    normal_category_names = [
        '雑記',
        'プログラミング',
        'TypeScript',
        'AWS',
        '趣味',
    ]
    fixed_category_names = [
        'プロフィール',
        'お問い合わせ',
    ]
    try:
        print("開始:categories")
        categories = [Category(category_name=name, article_type=1) for name in normal_category_names]
        categories += [Category(category_name=name, article_type=2) for name in fixed_category_names]

        for category in categories:
            db.add(category)
        db.commit()
        print("完了:categories")
    except Exception as e:
        print("失敗:categories")
        print(e)
        db.rollback()