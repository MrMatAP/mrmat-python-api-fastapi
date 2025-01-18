#  MIT License
#
#  Copyright (c) 2022 MrMat
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

"""
Blueprint for the Healthz API
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthzSchema(BaseModel):
    status: str

class LivenessSchema(BaseModel):
    status: str

class ReadinessSchema(BaseModel):
    status: str

@router.get('/',
            name='Get application health',
            description='Get an indication of application health',
            response_model=HealthzSchema)
async def healthz() -> HealthzSchema:
    return HealthzSchema(status='OK')

@router.get('/liveness/',
            name='Get application liveness',
            description='Get an indication of application liveness',
            response_model=LivenessSchema)
async def liveness() -> LivenessSchema:
    return LivenessSchema(status='OK')

@router.get('/readiness/',
            name='Get application readiness',
            description='Get an indication of application readiness',
            response_model=ReadinessSchema)
async def readiness() -> ReadinessSchema:
    return ReadinessSchema(status='OK')
