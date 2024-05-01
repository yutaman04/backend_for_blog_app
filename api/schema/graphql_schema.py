import json
import os
import sys
from typing import Optional
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, './../../'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)


from sqlalchemy import Null
import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI,Request
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from database import SessionLocal
from models.category import Category as CategoryModel
from models.article import Article as ArticleModel
from models.user import User as UserModel
from models.article_image import ArticleImage as ArticleImageModel
from api.service.article_service import ArticleService

@strawberry.type
class Category:
    id: strawberry.ID
    categoryName: str
    


@strawberry.type
class ArticleImage:
    id: strawberry.ID
    articleId: int
    imageName: str
    sortOrder: int
    isActive: bool
    createUserId: int
    createUserName: str
    createUserDisplayName: str
    createdAt: str
    updatedAt: str
    
@strawberry.type
class Article:
    id: strawberry.ID
    categoryId: int
    categoryName: str
    title: str
    content: str
    isActive: bool
    createUserId: int
    createUserName: str
    createUserDisplayName: str
    createdAt: str
    updatedAt: str
    articleImages: Optional[list[ArticleImage]]

@strawberry.type
class Query:
    
    # カテゴリー一覧取得
    @strawberry.field
    def categories(self) -> list[Category]:
        db: Session = SessionLocal() 
        data = db.query(CategoryModel).all()
        db.close()    
        return [Category(id=cat.id, categoryName=cat.category_name) for cat in data]

    # 記事一覧取得
    @strawberry.field
    def articles(self, limit: int = None, offset: int = None) -> list[Article]:
        if limit is None or offset is None:
            raise ValueError("limit and offset is required for fetching an articles")
        
        article_service = ArticleService()
        return article_service.articles(limit, offset)

    # 記事取得
    @strawberry.field
    def article(self, id: strawberry.ID = None) -> Article:
        if id is None:
            raise ValueError("ID is required for fetching an article")
        
        article_service = ArticleService()
        return article_service.article(id)