from fastapi import File
from api.service.article_service import ArticleService
from api.service.auth_service import AuthService
from api.schema.graphql_schema import AdminArticleUpload, AuthResult, AuthVerificationResult
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