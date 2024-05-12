from sqlalchemy import desc
from api.schema.graphql_schema import AdminArticleSummary, Article
from database import SessionLocal
from models.article import Article as ArticleModel
from models.user import User as UserModel
from models.category import Category as CategoryModel
from sqlalchemy.orm import Session



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
        
        if data:
            return AdminArticleSummary(
                totalArticleCount = totalCount,
                disabledArticleCount = disabledArticleCount,
                activeArticleCount = activeArticleCount,
                recentPostsArticle = [Article(
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
                    ) for article in data ]
            )
        else:
            return AdminArticleSummary(
                totalArticleCount = totalCount,
                disabledArticleCount = disabledArticleCount,
                activeArticleCount = activeArticleCount,
                recentPostsArticle=None
            )      
