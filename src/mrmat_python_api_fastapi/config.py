#  MIT License
#
#  Copyright (c) 2022 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from typing import Optional
import os
import json
import secrets


class Config:
    """
    A class to deal with application configuration
    """
    secret_key: str = secrets.token_urlsafe(16)
    db_url: str = 'sqlite://'

    @staticmethod
    def from_json_file(file: Optional[os.PathLike] = os.getenv('APP_CONFIG')):
        runtime_config = Config()
        if file and os.path.exists(file):
            with open(file, 'r', encoding='UTF-8') as c:
                file_config = json.load(c)
            runtime_config.secret_key = file_config.get('secret_key', secrets.token_urlsafe(16))
            runtime_config.db_url = file_config.get('db_url', 'sqlite://')
        return runtime_config
