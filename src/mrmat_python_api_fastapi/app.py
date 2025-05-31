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

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from prometheus_fastapi_instrumentator import Instrumentator

from mrmat_python_api_fastapi.apis.healthz import api_healthz
from mrmat_python_api_fastapi.apis.greeting import api_greeting_v1, api_greeting_v2, api_greeting_v3
from mrmat_python_api_fastapi.apis.platform import api_platform_v1

app = FastAPI(title='MrMat :: Python :: API :: FastAPI')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
app.include_router(api_healthz, prefix='/api/healthz', tags=['health'])
app.include_router(api_greeting_v1, prefix='/api/greeting/v1', tags=['greeting'])
app.include_router(api_greeting_v2, prefix='/api/greeting/v2', tags=['greeting'])
app.include_router(api_greeting_v3, prefix='/api/greeting/v3', tags=['greeting'])
app.include_router(api_platform_v1, prefix='/api/platform/v1', tags=['platform'])

Instrumentator().instrument(app).expose(app)

@app.get('/')
def index():
    return {'Hello': 'World'}

def run() -> int:
    """
    This is the main entry point for the application when running via the CLI wrapper
    Returns:
        - int: The exit code
    """
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
    return 0
