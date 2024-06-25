from fastapi import File
from api.service.article_service import ArticleService
from api.service.auth_service import AuthService
from api.schema.graphql_schema import AdminArticleUpload, AuthResult, AuthVerificationResult, CreateAritcle
import strawberry
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')
from strawberry.file_uploads import Upload


@strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, user_name: str, password: str) -> AuthResult:
        auth_service = AuthService()
        return auth_service.login(user_name, password)
    
    @strawberry.mutation
    def jwt_verification(self, target_jwt: str) -> AuthVerificationResult:
        auth_service = AuthService()
        
        return auth_service.jwt_verification(target_jwt)
    
    @strawberry.mutation
    async def article_image_upload(self, jwt: str,  file: Upload) -> AdminArticleUpload:
        
        # 認証
        if jwt is None:
            raise ValueError("jwt is required for upload article image")
        
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != 'success':
            return AdminArticleUpload(status="auth_error", filePath="")
        
        article_service = ArticleService()
        export_file_path = await article_service.article_image_upload(file)
        
        return AdminArticleUpload(status="success", filePath=export_file_path)
    
    @strawberry.mutation
    def create_article(self, jwt: str , article_title: str, article_body: str, category_id: int, article_images: list[str]) -> CreateAritcle:
         # 認証
        if jwt is None:
            raise ValueError("jwt is required for create article")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != 'success':
            return AdminArticleUpload(status="auth_error", filePath="")
        # jwtからユーザー情報を取得
        jwt_user_info = auth_service.show_jwt_user_info(jwt)
        
        # 記事をDBに登録する
        if jwt_user_info.userId != None:
            article_service = ArticleService()
            create_article_id = article_service.create_article(jwt_user_info.userId, article_title, article_body, category_id, article_images)
            
            return CreateAritcle(status="200", article_id=create_article_id)
        else:
            raise Exception("Faled to create article")
        
