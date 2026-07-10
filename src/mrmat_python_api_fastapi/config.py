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
import json
import secrets


class Config:
    """
    A class to deal with application configuration
    """

    secret_key: str = secrets.token_urlsafe(16)
    db_url: str = "sqlite:///"
    idp_issuer: str = ""
    oidc_auth_url: str = ""
    oidc_token_url: str = ""
    client_id: str = ""
    client_secret: str = ""

    @staticmethod
    def from_context(file: str | None = os.getenv("APP_CONFIG")):
        runtime_config = Config()
        if file and os.path.exists(file):
            with open(file, "r", encoding="UTF-8") as c:
                file_config = json.load(c)
            runtime_config.secret_key = file_config.get(
                "secret_key", secrets.token_urlsafe(16)
            )
            runtime_config.db_url = file_config.get("db_url", "sqlite:///")
            runtime_config.idp_issuer = file_config.get("idp_issuer", "")
            runtime_config.oidc_auth_url = file_config.get("oidc_auth_url", "")
            runtime_config.oidc_token_url = file_config.get("oidc_token_url", "")
            runtime_config.client_id = file_config.get("client_id", "")
            runtime_config.client_secret = file_config.get("client_secret", "")
        if "APP_CONFIG_SECRET_KEY" in os.environ:
            runtime_config.secret_key = os.getenv(
                "APP_CONFIG_SECRET_KEY", secrets.token_urlsafe(16)
            )
        if "APP_CONFIG_DB_URL" in os.environ:
            runtime_config.db_url = os.getenv("APP_CONFIG_DB_URL", "")
        return runtime_config

    def save(self, file: str | None = None) -> None:
        config_file = file or os.getenv("APP_CONFIG", "config.json")
        data = {
            "secret_key": self.secret_key,
            "db_url": self.db_url,
            "idp_issuer": self.idp_issuer,
            "oidc_auth_url": self.oidc_auth_url,
            "oidc_token_url": self.oidc_token_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        with open(config_file, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2)
