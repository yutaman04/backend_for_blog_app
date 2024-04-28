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
from models.article_image import ArticleImage as ArticleImageModel

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
    def articles(self, limit: int, offset: int) -> list[Article]:
        db: Session = SessionLocal()
        data = db.query(ArticleModel, UserModel)\
                .join(UserModel, UserModel.id == ArticleModel.create_user_id)\
                .limit(limit).offset(offset)
        # data = db.query(ArticleModel, UserModel)\
        #         .join(UserModel, UserModel.id == ArticleModel.create_user_id)\
        #         .all()
        
        return_obj: list[Article] = []
        
        if data:           
            for article in data:
                # 記事の画像を取得
                images = db.query(ArticleImageModel, UserModel)\
                         .join(UserModel, UserModel.id == ArticleImageModel.create_user_id)\
                         .where(ArticleImageModel.article_id == article.Article.id)\
                         .all()
                if images:
                    # 画像がある場合はリストを生成して設定する
                    tmp_article = Article(
                        id=article.Article.id,
                        categoryId=article.Article.category_id,
                        title=article.Article.title,
                        content=article.Article.content,
                        isActive=article.Article.is_active,
                        createUserId=article.Article.create_user_id,
                        createUserName=article.User.user_name,
                        createUserDisplayName=article.User.display_name,
                        createdAt=article.Article.created_at,
                        updatedAt=article.Article.updated_at,
                        articleImages=[ArticleImage(
                                        id=ai.ArticleImage.id,
                                        articleId=ai.ArticleImage.article_id,
                                        imageName=ai.ArticleImage.image_name,
                                        sortOrder=ai.ArticleImage.sort_order,
                                        isActive=ai.ArticleImage.is_active,
                                        createUserId=ai.ArticleImage.create_user_id,
                                        createUserName=ai.User.user_name,
                                        createUserDisplayName=ai.User.display_name,
                                        createdAt=ai.ArticleImage.created_at,
                                        updatedAt=ai.ArticleImage.updated_at,
                                    ) for ai in images]
                    )
                    return_obj.append(tmp_article)
                else:
                    # 画像が無い場合は空の配列を設定
                    tmp_article = Article(
                        id=article.Article.id,
                        categoryId=article.Article.category_id,
                        title=article.Article.title,
                        content=article.Article.content,
                        isActive=article.Article.is_active,
                        createUserId=article.Article.create_user_id,
                        createUserName=article.User.user_name,
                        createUserDisplayName=article.User.display_name,
                        createdAt=article.Article.created_at,
                        updatedAt=article.Article.updated_at,
                        articleImages=[]
                    )
                    return_obj.append(tmp_article)
                    
            return return_obj     
        else:
            raise Exception("Articles not found")

    # 記事取得
    @strawberry.field
    def article(self, id: strawberry.ID) -> Article:
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