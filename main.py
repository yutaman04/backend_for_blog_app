import os
import sys
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, '.'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)
print(project_root)


import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI,Request
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from database import SessionLocal
from models.category import Category as CategoryModel
from models.article import Article as ArticleModel

@strawberry.type
class Category:
    id: int
    categoryName: str
    
@strawberry.type
class Ariticle:
    id: int
    categoryId: int
    title: str
    content: str
    isActive: bool
    createUserId: int
    createdAt: str
    updatedAt: str

@strawberry.type
class Query:
    @strawberry.field
    def categories(self) -> list[Category]:
        db: Session = SessionLocal() 
        data = db.query(CategoryModel).all()
            
        return [Category(id=cat.id, categoryName=cat.category_name) for cat in data]
    @strawberry.field
    def articles(self) -> list[Ariticle]:
        db: Session = SessionLocal()
        data = db.query(ArticleModel).all()
        print(data[0].title)
        return [Ariticle(
                        id=article.id,
                        categoryId=article.category_id,
                        title=article.title,
                        content=article.content,
                        isActive=article.is_active,
                        createUserId=article.create_user_id,
                        createdAt=article.created_at,
                        updatedAt=article.updated_at
                    ) for article in data]
    
    
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/api/graphql", graphql_app)

@app.get("/api")
async def root(request:Request):
    print(request.headers)
    return {"message": "Hello World"}

@app.get("/no-proxy-header")
async def noProxyHeader(request:Request):
    print(request.headers)
    return {"message": "no proxy header"}