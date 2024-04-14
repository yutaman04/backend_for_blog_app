import datetime
from sqlalchemy import Column, DateTime, Integer, Null, String, Boolean, func
from datetime import timedelta
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default = func.now(), nullable=True)
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)