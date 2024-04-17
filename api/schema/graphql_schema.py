import os
import sys
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, './../../'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)
print(project_root)


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

@strawberry.type
class Category:
    id: strawberry.ID
    categoryName: str
    
@strawberry.type
class Article:
    id: strawberry.ID
    categoryId: int
    title: str
    content: str
    isActive: bool
    createUserId: int
    createUserName: str
    createUserDisplayName: str
    createdAt: str
    updatedAt: str

@strawberry.type
class Query:
    # カテゴリー一覧取得
    @strawberry.field
    def categories(self) -> list[Category]:
        db: Session = SessionLocal() 
        data = db.query(CategoryModel).all()
            
        return [Category(id=cat.id, categoryName=cat.category_name) for cat in data]

    # 記事一覧取得（ページネート無）
    @strawberry.field
    def articles(self) -> list[Article]:
        db: Session = SessionLocal()
        data = db.query(ArticleModel, UserModel).join(UserModel, UserModel.id == ArticleModel.create_user_id).all()

        if data:
            return [Article(
                    id=article.Article.id,
                    categoryId=article.Article.category_id,
                    title=article.Article.title,
                    content=article.Article.content,
                    isActive=article.Article.is_active,
                    createUserId=article.Article.create_user_id,
                    createUserName=article.User.user_name,
                    createUserDisplayName=article.User.display_name,
                    createdAt=article.Article.created_at,
                    updatedAt=article.Article.updated_at
                ) for article in data]
        else:
            raise Exception("Articles not found")

    # 記事取得
    @strawberry.field
    def article(self, info, id: strawberry.ID) -> Article:
        db: Session = SessionLocal()
        article = db.query(ArticleModel, UserModel).join(UserModel, UserModel.id == ArticleModel.create_user_id).filter(ArticleModel.id == id).first()
        
        if article:
            return Article(
                    id=article.Article.id,
                    categoryId=article.Article.category_id,
                    title=article.Article.title,
                    content=article.Article.content,
                    isActive=article.Article.is_active,
                    createUserId=article.Article.create_user_id,
                    createUserName=article.User.user_name,
                    createUserDisplayName=article.User.display_name,
                    createdAt=article.Article.created_at,
                    updatedAt=article.Article.updated_at
                )
        else:
            raise Exception("Article not found")