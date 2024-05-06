import datetime
from sqlalchemy import Column, DateTime, Integer, Null, String, Boolean, func, Text
from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    create_user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default = func.now(), nullable=True)
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    