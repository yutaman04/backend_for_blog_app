import datetime
from numbers import Number
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Null, String, Boolean, func, Text
from database import Base


class ArticleImage(Base):
    __tablename__ = "article_image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('articles.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    image_path = Column(String(4096), nullable=False)
    sort_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    create_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default = func.now(), nullable=True)
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)