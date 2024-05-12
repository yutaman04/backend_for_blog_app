from api.schema.graphql_schema import AdminArticleSummary, Article, Category
import strawberry
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from api.service.admin_service import AdminService
from database import SessionLocal
from models.category import Category as CategoryModel
from api.service.article_service import ArticleService


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
    
    # 管理サマリー取得
    @strawberry.field
    def admin_summary(self, jwt: str) -> AdminArticleSummary:
        if jwt is None:
            raise ValueError("jwt is required for fetching an admin_summary")
        
        admin_service = AdminService(jwt)
        return admin_service.admin_summary()
        