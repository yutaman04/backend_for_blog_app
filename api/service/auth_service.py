
import hashlib
import os
import time
from typing import Any
from dotenv import load_dotenv
import jwt

from api.service.user_service import UserService
from api.schema.graphql_schema import AuthResult, AuthVerificationResult

class AuthService:
    load_dotenv()
    user_service = UserService()
    
    SUCCESS = "success"
    ERROR_USER_NOT_FOUND = "User not found"
    ERROR_AUTH_FAIL = "Authentication failure"
    ERROR_JWT_EXP_ERROR = "expiration error"
    
    
    # JWTの生成
    def create_jwt_token(self, user_name: str):
        jwt_expiration = self.calc_jwt_expiration()
        encoded = jwt.encode({"user_name": user_name, "jwt_expiration": jwt_expiration}, os.environ['JWT_SECRET_KEY'], algorithm="HS256")
        return encoded
    
    # パスワード検証
    def password_verification(self, input_pass: str, hashed_pass: str):
        hashed_input_pass = hashlib.sha256(input_pass.encode("utf-8")).hexdigest()
        
        if hashed_input_pass == hashed_pass:
            return True
        
        return False
    
    # JWTの有効期限を算出
    def calc_jwt_expiration(self):
        now = time.time()
        token_expiration = now + float(os.environ['JWT_EXPIRATION_24HOUR'])
        
        return token_expiration

    # ログイン処理
    def login(self, user_name: str, input_pass: str):
        return_data = AuthResult(msg="success", jwt="")
        # ユーザーの存在確認
        user_data = self.user_service.user_existence_confirmation(user_name)
        if user_data == None:
            return_data.msg = self.ERROR_USER_NOT_FOUND
            return return_data
        
        # パスワード検証
        verification_result = self.password_verification(input_pass, user_data.user_password)
        
        # パスワードOKならJWTを設定して返す
        if verification_result:
            jwt = self.create_jwt_token(user_name)
            return_data.jwt = jwt
            return return_data
        else:
            return_data.msg = self.ERROR_AUTH_FAIL
            return return_data
    
    # JWTの検証
    def jwt_verification(self, target_jwt: str):
        ret = AuthVerificationResult(msg="")
        now = time.time()
        try:
            decode_result: dict[str, Any] = jwt.decode(
                jwt=target_jwt,
                key=os.environ['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            if decode_result['jwt_expiration'] >= now:
                ret.msg = self.SUCCESS
            else:
                raise Exception('expiration error')
        except Exception as e:
           ret.msg = self.ERROR_JWT_EXP_ERROR
        finally:
            return ret
    
    
        