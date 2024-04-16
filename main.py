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

@strawberry.type
class Category:
    id: int
    categoryName: str

@strawberry.type
class Query:
    @strawberry.field
    def categories(self) -> list[Category]:
        db: Session = SessionLocal() 
        data = db.query(CategoryModel).all()
            
        return [Category(id=cat.id, categoryName=cat.category_name) for cat in data]
    
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