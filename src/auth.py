from fastapi.security import OAuth2PasswordBearer
from .settings import settingObj as Settings

from enum import Enum
from typing import Annotated
from fastapi import Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt


jwks_client = jwt.PyJWKClient(
    f"https://cognito-idp.{Settings.aws_default_region}.amazonaws.com/{Settings.cognito_user_pool_id}/.well-known/jwks.json"
)

class CognitoTokenUse(Enum):
    ID = "id"
    ACCESS = "access"


class CognitoJWTAuthorizer:
    def __init__(
            self,
            required_token_use: CognitoTokenUse,
            aws_default_region: str,
            cognito_user_pool_id: str,
            cognito_app_client_id: str,
            jwks_client: jwt.PyJWKClient,
    ) -> None:
        self.required_token_use = required_token_use
        self.aws_default_region = aws_default_region
        self.cognito_user_pool_id = cognito_user_pool_id
        self.cognito_app_client_id = cognito_app_client_id
        self.jwks_client = jwks_client

    def __call__(self, authorization: Annotated[str | None, Header()] = None):
        if not authorization:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        split_authorization_tokens: list[str] = authorization.split("Bearer ")

        if len(split_authorization_tokens) < 2:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        token: str = split_authorization_tokens[1]

        try:
            signing_key: jwt.PyJWK = self.jwks_client.get_signing_key_from_jwt(token)
        except jwt.exceptions.InvalidTokenError as e:
            raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                ) from e


        try:
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=f"https://cognito-idp.{self.aws_default_region}.amazonaws.com/{self.cognito_user_pool_id}",
                options={
                    "verify_aud": False,
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iss": True,
                    "require": ["token_use", "exp", "iss", "sub"],
                },
            )
        
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from e
        except jwt.exceptions.InvalidTokenError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            ) from e
        
        if self.required_token_use.value != claims["token_use"]:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        
        if self.required_token_use == CognitoTokenUse.ID:
            if "aud" not in claims:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            if claims["aud"] != self.cognito_app_client_id:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
        elif self.required_token_use == CognitoTokenUse.ACCESS:
            if "client_id" not in claims:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            if claims["client_id"] != self.cognito_app_client_id:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        

        return claims
    

cognito_jwt_authorizer_access_token = CognitoJWTAuthorizer(
    CognitoTokenUse.ACCESS,
    Settings.aws_default_region,
    Settings.cognito_user_pool_id,
    Settings.cognito_app_client_id,
    jwks_client,
)

cognito_jwt_authorizer_id_token = CognitoJWTAuthorizer(
    CognitoTokenUse.ID,
    Settings.aws_default_region,
    Settings.cognito_user_pool_id,
    Settings.cognito_app_client_id,
    jwks_client,
)




