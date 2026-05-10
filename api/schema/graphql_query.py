from api.schema.graphql_schema import AdminArticleSummary, AdminCategory, Article, Category
import strawberry
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from api.service.admin_service import AdminService
from api.service.category_service import CategoryService
from database import SessionLocal
from models.category import Category as CategoryModel
from api.service.article_service import ArticleService
from enums.article_type import ArticleTypeEnum
from typing import Optional


@strawberry.type
class Query:
    # カテゴリー一覧取得
    @strawberry.field
    def categories(self, article_type: Optional[ArticleTypeEnum] = None) -> list[Category]:
        db: Session = SessionLocal()
        query = db.query(CategoryModel)
        if article_type is not None:
            query = query.filter(CategoryModel.article_type == article_type.value)
        data = query.all()
        db.close()
        return [Category(id=cat.id, categoryName=cat.category_name, articleType=ArticleTypeEnum(cat.article_type)) for cat in data]

    # 記事一覧取得
    @strawberry.field
    def articles(self, limit: int = None, offset: int = None, article_type: Optional[ArticleTypeEnum] = None) -> list[Article]:
        if limit is None or offset is None:
            raise ValueError("limit and offset is required for fetching an articles")

        article_service = ArticleService()
        return article_service.articles(limit, offset, article_type)

    # 記事取得
    @strawberry.field
    def article(self, id: strawberry.ID = None) -> Article:
        if id is None:
            raise ValueError("ID is required for fetching an article")
        
        article_service = ArticleService()
        return article_service.article(id)
    
    # 管理者向けカテゴリー一覧取得
    @strawberry.field
    def admin_categories(self, jwt: str) -> list[AdminCategory]:
        if jwt is None:
            raise ValueError("jwt is required for fetching admin_categories")

        AdminService(jwt)  # 認証チェック
        category_service = CategoryService()
        return category_service.admin_categories()

    # 管理サマリー取得
    @strawberry.field
    def admin_summary(self, jwt: str) -> AdminArticleSummary:
        if jwt is None:
            raise ValueError("jwt is required for fetching an admin_summary")

        admin_service = AdminService(jwt)
        return admin_service.admin_summary()
        