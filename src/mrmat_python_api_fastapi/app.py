#  MIT License
#
#  Copyright (c)  2025 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
import logging

import httpx
import jwt
from fastapi import FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from mrmat_python_api_fastapi.oidc import MrMatOIDC, OIDCException, OIDCRegistration
from mrmat_python_api_fastapi import app_config
from mrmat_python_api_fastapi.apis.healthz import api_healthz
from mrmat_python_api_fastapi.apis.greeting import (
    api_greeting_v1,
    api_greeting_v2,
    api_greeting_v3,
)
from mrmat_python_api_fastapi.apis.platform import api_platform_v1

logger = logging.getLogger(__name__)

# def _register_client(registration_token: str, base_url: str) -> None:
#     claims = jwt.decode(registration_token, options={"verify_signature": False})
#     issuer: str = claims["iss"]
#     with httpx.Client() as client:
#         discovery = (
#             client.get(f"{issuer}/.well-known/openid-configuration")
#             .raise_for_status()
#             .json()
#         )
#         reg_data = (
#             client.post(
#                 discovery["registration_endpoint"],
#                 headers={"Authorization": f"Bearer {registration_token}"},
#                 json={
#                     "application_type": "web",
#                     "client_name": "mrmat-python-api-fastapi",
#                     "redirect_uris": [f"{base_url}/docs/oauth2-redirect"],
#                     "grant_types": ["authorization_code"],
#                     "response_types": ["code"],
#                     "contacts": ["imfeldma@mrmat.org"],
#                 },
#             )
#             .raise_for_status()
#             .json()
#         )
#         reg_info = (
#             client.get(
#                 reg_data["registration_client_uri"],
#                 headers={"Authorization": f"Bearer {reg_data['registration_access_token']}"},
#             )
#         )
#     app_config.idp_issuer = issuer
#     app_config.oidc_auth_url = discovery["authorization_endpoint"]
#     app_config.oidc_token_url = discovery["token_endpoint"]
#     app_config.client_id = reg_data["client_id"]
#     app_config.client_secret = reg_data.get("client_secret", "")
#     app_config.save()
#     logger.info("Registered client '%s' with IdP at %s", app_config.client_id, issuer)
# 
# 
# if _registration_token := os.getenv("APP_REGISTRATION_TOKEN"):
#     try:
#         _base_url = os.getenv("APP_BASE_URL", "http://localhost:8000")
#         _register_client(_registration_token, _base_url)
#     except Exception:
#         logger.exception("Client registration with IdP failed")

mrmat_oidc_app = OIDCRegistration(
    application_type='web',
    client_name='mrmat-python-api-fastapi',
    redirect_uris=['http://localhost:8000/docs/oauth2-redirect'],
    grant_types=['authorization_code'],
    response_types=['code'],
    contacts=['imfeldma@mrmat.org']
)
mrmat_oidc = MrMatOIDC(app_registration=mrmat_oidc_app,
                       app_registration_token=os.getenv('APP_REGISTRATION_TOKEN'),
                       app_idp_url=os.getenv('APP_IDP_URL'))

if app_config.oidc_auth_url and app_config.oidc_token_url:
    oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=app_config.oidc_auth_url,
        tokenUrl=app_config.oidc_token_url,
    )
else:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # type: ignore[assignment]

_swagger_ui_init_oauth = (
    {
        "clientId": app_config.client_id,
        "scopes": "openid profile",
        "usePkceWithAuthorizationCodeGrant": True,
    }
    if app_config.client_id
    else None
)

app = FastAPI(
    title="MrMat :: Python :: API :: FastAPI",
    swagger_ui_init_oauth=_swagger_ui_init_oauth,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_healthz, prefix="/api/healthz", tags=["health"])
app.include_router(api_greeting_v1, prefix="/api/greeting/v1", tags=["greeting"])
app.include_router(api_greeting_v2, prefix="/api/greeting/v2", tags=["greeting"])
app.include_router(api_greeting_v3, prefix="/api/greeting/v3", tags=["greeting"])
app.include_router(api_platform_v1, prefix="/api/platform/v1", tags=["platform"])

Instrumentator().instrument(app).expose(app)


@app.get("/")
def index():
    return {"Hello": "World"}


def run() -> int:
    """
    This is the main entry point for the application when running via the CLI wrapper
    Returns:
        - int: The exit code
    """
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    return 0
