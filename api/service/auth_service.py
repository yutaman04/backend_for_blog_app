import os
from dotenv import load_dotenv
import jwt

class AuthService:
    load_dotenv()
    
    # JWTの生成
    def create_jwt_token(self, user_name: str):
        encoded = jwt.encode({"user_name": user_name}, os.environ['JWT_SECRET_KEY'], algorithm="HS256")
        return encoded

    