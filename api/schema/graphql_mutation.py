from api.service.auth_service import AuthService
from api.schema.graphql_schema import AuthResult, AuthVerificationResult
import strawberry
import zoneinfo
zoneinfo.ZoneInfo('Asia/Tokyo')


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