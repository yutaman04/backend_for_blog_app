import datetime
from numbers import Number
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Null, String, Boolean, func, Text
from database import Base
from sqlalchemy.orm import mapped_column


class ArticleImage(Base):
    __tablename__ = "article_image"

    id = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order=-10)
    article_id = mapped_column(Integer, ForeignKey('articles.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, sort_order=10)
    image_name = mapped_column(String(255), nullable=False, sort_order=20)
    sort_order = mapped_column(Integer, nullable=False, sort_order=30)
    is_active = mapped_column(Boolean, default=True, nullable=False, sort_order=35)
    create_user_id = mapped_column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, sort_order=40)
    created_at = mapped_column(DateTime, default = func.now(), nullable=True, sort_order=50)
    updated_at = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=True, sort_order=60)
    deleted_at = mapped_column(DateTime, nullable=True, sort_order=70)