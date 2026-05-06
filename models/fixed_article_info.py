import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from database import Base


class FixedArticleInfo(Base):
    __tablename__ = "fixed_article_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('articles.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default = func.now(), nullable=True)
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    