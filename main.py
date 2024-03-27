import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI,Request

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