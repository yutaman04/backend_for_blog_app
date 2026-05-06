from fastapi import File
from api.service.article_service import ArticleService
from api.service.auth_service import AuthService
from api.schema.graphql_schema import (
    AdminArticleUpload,
    AuthResult,
    AuthVerificationResult,
    CreateAritcle,
    CreateFixedArticle,
    EditArticle,
    DeleteArticle,
    UpdateArticleIsActive,
)
import strawberry
import zoneinfo

zoneinfo.ZoneInfo("Asia/Tokyo")
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
    async def article_image_upload(self, jwt: str, file: Upload) -> AdminArticleUpload:

        # 認証
        if jwt is None:
            raise ValueError("jwt is required for upload article image")

        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return AdminArticleUpload(status="auth_error", filePath="")

        article_service = ArticleService()
        export_file_path = await article_service.article_image_upload(file)

        return AdminArticleUpload(status="success", filePath=export_file_path)

    @strawberry.mutation
    def create_article(
        self,
        jwt: str,
        article_title: str,
        article_body: str,
        category_id: int,
        article_images: list[str],
    ) -> CreateAritcle:
        # 認証
        if jwt is None:
            raise ValueError("jwt is required for create article")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return AdminArticleUpload(status="auth_error", filePath="")
        # jwtからユーザー情報を取得
        jwt_user_info = auth_service.show_jwt_user_info(jwt)

        # 記事をDBに登録する
        if jwt_user_info.userId != None:
            article_service = ArticleService()
            create_article_id = article_service.create_article(
                jwt_user_info.userId,
                article_title,
                article_body,
                category_id,
                article_images,
            )

            return CreateAritcle(status="200", article_id=create_article_id)
        else:
            raise Exception("Faled to create article")

    @strawberry.mutation
    def create_fixed_article(
        self,
        jwt: str,
        article_title: str,
        article_body: str,
        category_id: int,
        article_images: list[str],
    ) -> CreateFixedArticle:
        if jwt is None:
            raise ValueError("jwt is required for create fixed article")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return CreateFixedArticle(status="auth_error", article_id=0)
        jwt_user_info = auth_service.show_jwt_user_info(jwt)

        if jwt_user_info.userId != None:
            article_service = ArticleService()
            create_article_id = article_service.create_fixed_article(
                jwt_user_info.userId,
                article_title,
                article_body,
                category_id,
                article_images,
            )
            return CreateFixedArticle(status="200", article_id=create_article_id)
        else:
            raise Exception("Failed to create fixed article")

    @strawberry.mutation
    def edit_article(
        self,
        jwt: str,
        article_id: int,
        article_title: str,
        article_body: str,
        category_id: int,
        article_images: list[str],
    ) -> EditArticle:
        # 認証
        if jwt is None:
            raise ValueError("jwt is required for edit article")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return EditArticle(status="auth_error", article_id=article_id)

        article_service = ArticleService()
        updated_article_id = article_service.update_article(
            article_id, article_title, article_body, category_id, article_images
        )

        return EditArticle(status="200", article_id=updated_article_id)

    @strawberry.mutation
    def delete_article(self, jwt: str, article_id: int) -> DeleteArticle:
        # 認証
        if jwt is None:
            raise ValueError("jwt is required for delete article")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return DeleteArticle(status="auth_error", article_id=article_id)

        article_service = ArticleService()
        deleted_article_id = article_service.delete_article(article_id)

        return DeleteArticle(status="200", article_id=deleted_article_id)

    @strawberry.mutation
    def update_article_is_active(self, jwt: str, article_id: int, is_active: bool) -> UpdateArticleIsActive:
        # 認証
        if jwt is None:
            raise ValueError("jwt is required for update article is_active")
        auth_service = AuthService()
        auth_reuslt = auth_service.jwt_verification(jwt)
        if auth_reuslt.msg != "success":
            return UpdateArticleIsActive(status="auth_error", article_id=article_id)

        article_service = ArticleService()
        updated_article_id = article_service.update_article_is_active(article_id, is_active)

        return UpdateArticleIsActive(status="200", article_id=updated_article_id)
