from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User as UserModel

class UserService:
    def user_existence_confirmation(self, user_name: str):
        db: Session = SessionLocal()
        user = db.query(UserModel)\
                 .where(UserModel.user_name == user_name)\
                 .first()         
        db.close()
        if user == None:
            return None
        else:
            return user
        