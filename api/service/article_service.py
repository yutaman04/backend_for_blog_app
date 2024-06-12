import os
import time
from typing import Optional
from fastapi import File
import strawberry
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from api.schema.graphql_schema import Article, ArticleImage
from database import SessionLocal
from models.article import Article as ArticleModel
from models.user import User as UserModel
from models.article_image import ArticleImage as ArticleImageModel
from models.category import Category as CategoryModel
from strawberry.file_uploads import Upload
import aiofiles


class ArticleService:
    # 記事一覧取得
    def articles(self, limit: int, offset: int) -> list[Article]:
        db: Session = SessionLocal()
        dataCount = db.query(ArticleModel).where(ArticleModel.is_active == True).count()
        data = db.query(ArticleModel, UserModel, CategoryModel)\
                .join(UserModel, UserModel.id == ArticleModel.create_user_id)\
                .join(CategoryModel, CategoryModel.id == ArticleModel.category_id)\
                .where(ArticleModel.is_active == True)\
                .limit(limit).offset(offset)
        db.close()
        
        return_obj: list[Article] = []
        
        if data:           
            for article in data:
                # 記事の画像を取得
                images = db.query(ArticleImageModel, UserModel)\
                         .join(UserModel, UserModel.id == ArticleImageModel.create_user_id)\
                         .where(ArticleImageModel.article_id == article.Article.id)\
                         .all()
                db.close()
                if images:
                    # 画像がある場合はリストを生成して設定する
                    tmp_article = Article(
                        id=article.Article.id,
                        categoryId=article.Article.category_id,
                        categoryName=article.Category.category_name,
                        title=article.Article.title,
                        content=article.Article.content,
                        isActive=article.Article.is_active,
                        createUserId=article.Article.create_user_id,
                        createUserName=article.User.user_name,
                        createUserDisplayName=article.User.display_name,
                        createdAt=article.Article.created_at,
                        updatedAt=article.Article.updated_at,
                        totalCount=dataCount,
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
                        categoryName=article.Category.category_name,
                        title=article.Article.title,
                        content=article.Article.content,
                        isActive=article.Article.is_active,
                        createUserId=article.Article.create_user_id,
                        createUserName=article.User.user_name,
                        createUserDisplayName=article.User.display_name,
                        createdAt=article.Article.created_at,
                        updatedAt=article.Article.updated_at,
                        totalCount=dataCount,
                        articleImages=[]
                    )
                    return_obj.append(tmp_article)       
            return return_obj
        else:
            raise Exception("Articles not found")
    
    # 特定の記事取得
    def article(self, id: strawberry.ID):
        db: Session = SessionLocal()
        article = db.query(ArticleModel, UserModel, CategoryModel)\
                    .join(UserModel, UserModel.id == ArticleModel.create_user_id)\
                    .join(CategoryModel, CategoryModel.id == ArticleModel.category_id)\
                    .where(ArticleModel.is_active == True)\
                    .filter(ArticleModel.id == id)\
                    .first()
        
        db.close()
        if article:
            # 記事の画像を取得
            images = db.query(ArticleImageModel, UserModel)\
                        .join(UserModel, UserModel.id == ArticleImageModel.create_user_id)\
                        .where(ArticleImageModel.article_id == article.Article.id)\
                        .all()
            db.close()
            if images:
                return Article(
                    id=article.Article.id,
                    categoryId=article.Article.category_id,
                    categoryName=article.Category.category_name,
                    title=article.Article.title,
                    content=article.Article.content,
                    isActive=article.Article.is_active,
                    createUserId=article.Article.create_user_id,
                    createUserName=article.User.user_name,
                    createUserDisplayName=article.User.display_name,
                    createdAt=article.Article.created_at,
                    updatedAt=article.Article.updated_at,
                    totalCount=None,
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
            else:
                return Article(
                        id=article.Article.id,
                        categoryId=article.Article.category_id,
                        categoryName=article.Category.category_name,
                        title=article.Article.title,
                        content=article.Article.content,
                        isActive=article.Article.is_active,
                        createUserId=article.Article.create_user_id,
                        createUserName=article.User.user_name,
                        createUserDisplayName=article.User.display_name,
                        createdAt=article.Article.created_at,
                        updatedAt=article.Article.updated_at,
                        totalCount=None,
                        articleImages=[]
                    )
        else:
            raise Exception("Article not found")
    
    # アップロードファイルを公開ディレクトリに保存する
    async def article_image_upload(self, file: Upload):
        # 保存先パスの生成
        image_base_path = "./images"
        image_extension = os.path.splitext(file[0].filename)
        # ファイル名は現在日時のミリ秒を基に生成
        file_name = "image_" + str(time.time()).replace('.', "") + image_extension[1]
        file_path = os.path.join(image_base_path, file_name)
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file[0].read()
            await out_file.write(content)
        
        return "/api" + file_path[1:]
        
        