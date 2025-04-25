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

import pytest
import fastapi.testclient

from mrmat_python_api_fastapi.apis.greeting.v1 import GreetingV1Output
from mrmat_python_api_fastapi.apis.greeting.v2 import GreetingV2Output

def test_greeting_v1(client: fastapi.testclient.TestClient):
    response = client.get("/api/greeting/v1")
    assert response.status_code == 200
    assert GreetingV1Output.model_validate(response.json(), strict=True).message == 'Hello World'

def test_greeting_v2(client: fastapi.testclient.TestClient):
    response = client.get("/api/greeting/v2")
    assert response.status_code == 200
    assert GreetingV2Output.model_validate(response.json(), strict=True).message == 'Hello Stranger'

@pytest.mark.parametrize('name', ['MrMat', 'Chris', 'Mihal', 'Alexandre', 'Jerome'])
def test_greeting_v2_custom(client: fastapi.testclient.TestClient, name: str):
    response = client.get("/api/greeting/v2", params=dict(name=name))
    assert response.status_code == 200
    assert GreetingV2Output.model_validate(response.json(), strict=True).message == f'Hello {name}'
