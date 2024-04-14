import os
import sys
import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI,Request
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)
print(project_root)


@strawberry.type
class User:
    name: str
    age: int

@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Shota", age=22)
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