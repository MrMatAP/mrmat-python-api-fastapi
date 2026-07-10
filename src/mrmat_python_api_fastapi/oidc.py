#  MIT License
#
#  Copyright (c)  2026 Mathieu Imfeld
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
import httpx
import pydantic

from mrmat_python_api_fastapi import app_config


class OIDCException(Exception):

    def __init__(self, code:int = 500, msg: str = 'OIDC Exception'):
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    def __str__(self):
        return f'[{self.code}] {self.msg}'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.code}, {self.msg})"

class OIDCDiscovery(pydantic.BaseModel):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    introspection_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    registration_endpoint: str

class OIDCRegistration(pydantic.BaseModel):
    application_type: str = pydantic.Field(default='web')
    client_name: str = pydantic.Field(description='The client name')
    redirect_uris: list[str] = pydantic.Field(default_factory=list, description='A list of URLs to redirect to')
    grant_types: list[str] = pydantic.Field(default_factory=list, description='A list of grant types')
    response_types: list[str] = pydantic.Field(default_factory=list, description='A list of response types')
    contacts: list[str] = pydantic.Field(default_factory=list, description='A list of contacts')

class MrMatOIDC:

    def __init__(self,
                 app_registration: OIDCRegistration,
                 app_registration_token: str | None = os.getenv('APP_REGISTRATION_TOKEN'),
                 app_idp_url: str | None = os.getenv('APP_IDP_URL')):
        if app_registration_token is None:
            raise OIDCException(code=400, msg='Unable to register app without a registration token')
        if app_idp_url is None:
            raise OIDCException(code=400, msg='Unable to register app without IDP URL')
        try:
            with httpx.Client() as client:
                discovery_json = (
                    client.get(f"{app_idp_url}/.well-known/openid-configuration")
                    .raise_for_status()
                    .json())
                self._idp_discovery = OIDCDiscovery.model_validate(discovery_json, extra='ignore')
                self._idp_url = app_idp_url
                self._app_registration = app_registration

                reg_data = client.post(
                    self._idp_discovery.registration_endpoint,
                    headers={'Authorization': f"Bearer {app_registration_token}"},
                    json=app_registration.model_dump()
                    ).raise_for_status(
                ).json()

                reg_info = client.get(
                    reg_data['registration_client_uri'],
                    headers={'Authorization': f"Bearer {reg_data['registration_access_token']}"}
                ).raise_for_status().json()
                pass
        except httpx.HTTPStatusError as hse:
            raise OIDCException(code=400, msg='Failed to discover IdP') from hse
        except pydantic.ValidationError as ve:
            raise OIDCException(code=400, msg='Failed to parse IdP .well-known respoonse') from ve

    @property
    def idp_discovery(self) -> OIDCDiscovery:
        return self._idp_discovery