import strawberry
from typing import Optional

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
class JwtUserInfo:
    userId: int
    userName: str
    