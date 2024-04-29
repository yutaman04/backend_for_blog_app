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
from db.seed.seeders import categories, users, articles, article_image



db = database.SessionLocal()

def seed():
    print("開始")
    categories.seed()
    users.seed()
    articles.seed()
    article_image.seed()
    print("完了")
        
if __name__ == '__main__':
    BOS = '\033[92m'  # 緑色表示用
    EOS = '\033[0m'

    print(f'{BOS}Seeding data...{EOS}')
    seed()