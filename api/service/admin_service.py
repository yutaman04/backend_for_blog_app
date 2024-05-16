from sqlalchemy import desc
from api.schema.graphql_schema import AdminArticleSummary, Article
from database import SessionLocal
from models.article import Article as ArticleModel
from models.user import User as UserModel
from models.category import Category as CategoryModel
from sqlalchemy.orm import Session
from models.article_image import ArticleImage as ArticleImageModel
from api.schema.graphql_schema import Article, ArticleImage

from api.service.auth_service import AuthService


class AdminService(AuthService):
    def __init__(self, jwt:str):
        auth_result = self.jwt_verification(jwt)
        if(auth_result.msg == self.ERROR_JWT_EXP_ERROR):
            raise Exception(self.ERROR_JWT_EXP_ERROR)
    
    # 管理サマリー取得
    def admin_summary(self):
        db: Session = SessionLocal()
        totalCount = db.query(ArticleModel).where(ArticleModel.deleted_at == None).count()
        disabledArticleCount = db.query(ArticleModel)\
                                 .where(ArticleModel.deleted_at == None)\
                                 .where(ArticleModel.is_active == False)\
                                 .count()
        activeArticleCount = db.query(ArticleModel)\
                                 .where(ArticleModel.deleted_at == None)\
                                 .where(ArticleModel.is_active == True)\
                                 .count()
        data = db.query(ArticleModel, UserModel, CategoryModel)\
                .join(UserModel, UserModel.id == ArticleModel.create_user_id)\
                .join(CategoryModel, CategoryModel.id == ArticleModel.category_id)\
                .where(ArticleModel.is_active == True)\
                .where(ArticleModel.deleted_at == None)\
                .order_by(desc(ArticleModel.created_at))\
                .limit(3)
        db.close()
        
        
        tmp_article_list: list[Article] = []
        if data:
            for article in data:
                # 記事の画像を取得
                image = db.query(ArticleImageModel, UserModel)\
                         .join(UserModel, UserModel.id == ArticleImageModel.create_user_id)\
                         .where(ArticleImageModel.article_id == article.Article.id)\
                         .first()                      
                db.close()
                
                if image:
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
                            totalCount=totalCount,
                            articleImages=[ArticleImage(
                                id=image.ArticleImage.id,
                                articleId=image.ArticleImage.article_id,
                                imageName=image.ArticleImage.image_name,
                                sortOrder=image.ArticleImage.sort_order,
                                isActive=image.ArticleImage.is_active,
                                createUserId=image.ArticleImage.create_user_id,
                                createUserName=image.User.user_name,
                                createUserDisplayName=image.User.display_name,
                                createdAt=image.ArticleImage.created_at,
                                updatedAt=image.ArticleImage.updated_at,
                            )]
                        )
                    tmp_article_list.append(tmp_article)
                else:
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
                            totalCount=totalCount,
                            articleImages=None
                        )
                    tmp_article_list.append(tmp_article)
                
            return AdminArticleSummary(
                totalArticleCount = totalCount,
                disabledArticleCount = disabledArticleCount,
                activeArticleCount = activeArticleCount,
                recentPostsArticle = tmp_article_list
            )
        else:
            return AdminArticleSummary(
                totalArticleCount = totalCount,
                disabledArticleCount = disabledArticleCount,
                activeArticleCount = activeArticleCount,
                recentPostsArticle=None
            )      
