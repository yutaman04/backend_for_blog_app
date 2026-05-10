import strawberry
from typing import Optional
from enums.article_type import ArticleTypeEnum


@strawberry.type
class ArticleImage:
    id: strawberry.ID
    articleId: int
    imageName: str
    sortOrder: int
    isActive: bool
    createUserId: int
    createUserName: str
    createUserDisplayName: str
    createdAt: str
    updatedAt: str


@strawberry.type
class Article:
    id: strawberry.ID
    categoryId: int
    categoryName: str
    title: str
    content: str
    articleType: ArticleTypeEnum
    isActive: bool
    createUserId: int
    createUserName: str
    createUserDisplayName: str
    createdAt: str
    updatedAt: str
    totalCount: int
    articleImages: Optional[list[ArticleImage]]


@strawberry.type
class Category:
    id: strawberry.ID
    categoryName: str
    articleType: ArticleTypeEnum


@strawberry.type
class AuthResult:
    msg: str
    jwt: str


@strawberry.type
class AuthVerificationResult:
    msg: str


@strawberry.type
class AdminArticleSummary:
    totalArticleCount: int
    disabledArticleCount: int
    activeArticleCount: int
    recentPostsArticle: list[Article]


@strawberry.type
class AdminArticleUpload:
    status: str
    filePath: str


@strawberry.type
class CreateAritcle:
    status: str
    article_id: strawberry.ID


@strawberry.type
class CreateFixedArticle:
    status: str
    article_id: strawberry.ID


@strawberry.type
class EditArticle:
    status: str
    article_id: strawberry.ID


@strawberry.type
class DeleteArticle:
    status: str
    article_id: strawberry.ID


@strawberry.type
class UpdateArticleIsActive:
    status: str
    article_id: strawberry.ID


@strawberry.type
class AdminCategory:
    id: strawberry.ID
    categoryName: str
    articleType: ArticleTypeEnum
    isActive: bool
    createdAt: str
    updatedAt: str


@strawberry.type
class CreateCategory:
    status: str
    category_id: strawberry.ID


@strawberry.type
class EditCategory:
    status: str
    category_id: strawberry.ID


@strawberry.type
class DeleteCategory:
    status: str
    category_id: strawberry.ID


@strawberry.type
class JwtUserInfo:
    userId: int
    userName: str
