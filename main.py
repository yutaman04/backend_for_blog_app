from http.client import HTTPException
import os
import shutil
import sys
from fastapi import Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.schema.graphql_schema import Query
from api.service.article_image import ArticleImageService
from models.article_image import ArticleImage
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトルートのパスを取得
project_root = os.path.abspath(os.path.join(current_dir, '.'))

# プロジェクトルートをPythonパスに追加
sys.path.append(project_root)
print(project_root)


from sqlalchemy import Null
import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI, File,Request, UploadFile
from sqlalchemy.orm import Session
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
    
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/api/graphql", graphql_app)
# 画像用のディレクトリを静的ファイルとして公開する
app.mount("/api/images", StaticFiles(directory="images"), name="images")


# @app.post("/api/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     with open(file.filename, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"filename": file.filename}

# 以下の画像取得系APIは、公開ディレクトリを使用しない場合にblobで返す場合の例
# 今回は静的ファイルを直接公開するので使用しないが後学のため残しておく
# @app.get("/api/article-image/download/{article_id}/{file_name}")
# async def download_target_article_file(article_id: str, file_name: str):
#     article_image_proc = ArticleImageService()
    
#     response = article_image_proc.get_image(article_id, file_name)
#     if response == False:
#         return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 content={"message": "File not found"},
#             )
#     else:    
#         return response
    
# @app.get("/api/article-image/download/{article_id}")
# async def download_article_files(article_id: str):
#     article_image_proc = ArticleImageService()
    
#     response = article_image_proc.get_images(article_id)
#     if response == False:
#         return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 content={"message": "File not found"},
#             )
#     else:    
#         return response


    