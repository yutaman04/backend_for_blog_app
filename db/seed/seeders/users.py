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
from models.user import User
import hashlib



db = database.SessionLocal()
  
def seed():
    sample_user_data = {
        "user_name": "sample_user",
        "display_name": "display_name",
        "user_password": hashlib.sha256("password".encode("utf-8")).hexdigest(),
        "email": "test@example.com",
    }
    
    user_data = User()
    user_data.user_name = sample_user_data["user_name"]
    user_data.display_name = sample_user_data["display_name"]
    user_data.user_password = sample_user_data["user_password"]
    user_data.email = sample_user_data["email"]
    
    try:
        print("開始:users")
        db.add(user_data)
        db.commit()
        print("完了:users")
    except Exception as e:
        print("失敗:users")
        print(e)
        db.rollback()