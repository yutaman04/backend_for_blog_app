from pathlib import Path
from fastapi.responses import FileResponse
import os

class ArticleImageService:
    current = Path()
    image_base_path = "./images/[article_id]"
    
    
    # 以下の画像取得系処理は、公開ディレクトリを使用しない場合にblobで返す場合の例
    # 今回は静的ファイルを直接公開するので使用しないが後学のため残しておく
    # # 指定した記事ファイルをダウンロードする
    # def get_image(self, article_id: str, file_name: str):
    #     # 画像へのファイルパスを生成
    #     target_file_path =  self.image_base_path.replace('[article_id]', article_id) + "/"+ file_name
    #     # ファイルの存在確認
    #     is_file_exist = os.path.exists(target_file_path)
    #     if is_file_exist:
    #         return FileResponse(path=target_file_path, filename=file_name)
    #     else:
    #         return False
    
    # # 指定した記事のファイルをすべてダウンロードする
    # def get_images(self, article_id: str):
    #     target_dir_path = self.image_base_path.replace('[article_id]', article_id)
    #     # ファイルが指定ディレクトリにあるか
    #     is_file_exist = os.path.exists(target_dir_path)
    #     if is_file_exist == False:
    #         return False
        
    #     file_response_list = []
    #     article_images = os.listdir(target_dir_path)
    #     for image_file_name in article_images:
    #         target_file_path = target_dir_path + '/' + image_file_name
    #         file_response_list.append(FileResponse(path=target_file_path, filename=image_file_name))
        
    #     return file_response_list
    