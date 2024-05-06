import hashlib
import os
from dotenv import load_dotenv
import jwt

from api.service.user_service import UserService
from api.schema.graphql_schema import AuthResult

class AuthService:
    load_dotenv()
    
    user_service = UserService()
    
    # JWTの生成
    def create_jwt_token(self, user_name: str):
        encoded = jwt.encode({"user_name": user_name}, os.environ['JWT_SECRET_KEY'], algorithm="HS256")
        return encoded
    
    # パスワード検証
    def password_verification(self, input_pass: str, hashed_pass: str):
        hashed_input_pass = hashlib.sha256(input_pass.encode("utf-8")).hexdigest()
        
        if hashed_input_pass == hashed_pass:
            return True
        
        return False

    # ログイン処理
    def login(self, user_name: str, input_pass: str):
        return_data = AuthResult(msg="success", jwt="")
        # ユーザーの存在確認
        user_data = self.user_service.user_existence_confirmation(user_name)
        if user_data == None:
            return_data.msg = "User not found"
            return return_data
        
        # パスワード検証
        verification_result = self.password_verification(input_pass, user_data.user_password)
        
        # パスワードOKならJWTを設定して返す
        if verification_result:
            jwt = self.create_jwt_token(user_name)
            return_data.jwt = jwt
            return return_data
        else:
            return_data.msg = "Authentication failure"
            return return_data
        