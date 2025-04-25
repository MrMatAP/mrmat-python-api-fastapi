#  MIT License
#
#  Copyright (c) 2025 Mathieu Imfeld
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

import pathlib
import pytest
import fastapi.testclient

from mrmat_python_api_fastapi import app_config, ORMBase
from mrmat_python_api_fastapi.app import app
from mrmat_python_api_fastapi.db import get_db

@pytest.fixture(scope='session')
def build_path():
    build = pathlib.Path(__file__).parent.parent.resolve() / 'build'
    build.mkdir(exist_ok=True)
    return build

@pytest.fixture(scope='session')
def test_db_path(build_path) -> pathlib.Path:
    test_db_path = build_path / "test.db"
    if test_db_path.exists():
        test_db_path.unlink()
    return test_db_path

@pytest.fixture(scope='session')
def client(test_db_path) -> fastapi.testclient.TestClient:
    app_config.db_url = f'sqlite:///{test_db_path}'
    session = get_db()
    with session.begin():
        ORMBase.metadata.create_all(session.bind)
    return fastapi.testclient.TestClient(app)
