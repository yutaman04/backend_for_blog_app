import datetime
from sqlalchemy.orm import Session
from api.schema.graphql_schema import AdminCategory
from database import SessionLocal
from models.category import Category as CategoryModel
from enums.article_type import ArticleTypeEnum


class CategoryService:
    # 管理者向けカテゴリー一覧取得
    def admin_categories(self) -> list[AdminCategory]:
        db: Session = SessionLocal()
        data = (
            db.query(CategoryModel)
            .where(CategoryModel.deleted_at == None)
            .all()
        )
        db.close()
        return [
            AdminCategory(
                id=cat.id,
                categoryName=cat.category_name,
                articleType=ArticleTypeEnum(cat.article_type),
                isActive=cat.is_active,
                createdAt=cat.created_at,
                updatedAt=cat.updated_at,
            )
            for cat in data
        ]

    # カテゴリー作成
    def create_category(self, category_name: str, article_type: int) -> int:
        db: Session = SessionLocal()
        try:
            category = CategoryModel(
                category_name=category_name,
                article_type=article_type,
                is_active=True,
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            return category.id
        except:
            db.rollback()
            raise
        finally:
            db.close()

    # カテゴリー編集
    def update_category(self, category_id: int, category_name: str) -> int:
        db: Session = SessionLocal()
        try:
            category = (
                db.query(CategoryModel)
                .filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None)
                .first()
            )
            if category is None:
                raise Exception("Category not found")

            category.category_name = category_name
            db.commit()

            return category_id
        except:
            db.rollback()
            raise
        finally:
            db.close()

    # カテゴリー有効フラグ更新
    def update_category_is_active(self, category_id: int, is_active: bool) -> int:
        db: Session = SessionLocal()
        try:
            category = (
                db.query(CategoryModel)
                .filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None)
                .first()
            )
            if category is None:
                raise Exception("Category not found")

            category.is_active = is_active
            db.commit()

            return category_id
        except:
            db.rollback()
            raise
        finally:
            db.close()

    # カテゴリー削除（論理削除）
    def delete_category(self, category_id: int) -> int:
        db: Session = SessionLocal()
        try:
            category = (
                db.query(CategoryModel)
                .filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None)
                .first()
            )
            if category is None:
                raise Exception("Category not found")

            category.is_active = False
            category.deleted_at = datetime.datetime.now()
            db.commit()

            return category_id
        except:
            db.rollback()
            raise
        finally:
            db.close()
