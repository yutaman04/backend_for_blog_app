from api.service.auth_service import AuthService
from api.schema.graphql_schema import AuthResult
import strawberry
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')


@strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, user_name: str, password: str) -> AuthResult:
        auth_service = AuthService()
        return auth_service.login(user_name, password)
    