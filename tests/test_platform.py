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

import fastapi.testclient

from mrmat_python_api_fastapi.apis.platform.v1 import (
    ResourceSchema,
    ResourceInputSchema,
    ResourceListSchema,
    OwnerSchema,
    OwnerInputSchema,
    OwnerListSchema
)

def test_platform_v1(client: fastapi.testclient.TestClient):
    response = client.get('/api/platform/v1/owners')
    assert response.status_code == 200
    assert len(OwnerListSchema.model_validate(response.json(), strict=True).owners) == 0

    owner = OwnerInputSchema(name='test-owner')
    response = client.post('/api/platform/v1/owners', json=owner.model_dump(mode='json'))
    assert response.status_code == 201
    owner_created = OwnerSchema.model_validate(response.json(), strict=True)
    assert owner_created.uid is not None

    response = client.get(f'/api/platform/v1/owners/{owner_created.uid}')
    assert response.status_code == 200
    owner_retrieved = OwnerSchema.model_validate(response.json(), strict=True)
    assert owner_created == owner_retrieved

    response = client.get('/api/platform/v1/resources')
    assert response.status_code == 200
    assert len(ResourceListSchema.model_validate(response.json(), strict=True).resources) == 0

    resource = ResourceInputSchema(name='test-resource', owner_uid=owner_created.uid)
    response = client.post('/api/platform/v1/resources', json=resource.model_dump(mode='json'))
    assert response.status_code == 201
    resource_created = ResourceSchema.model_validate(response.json(), strict=True)
    assert resource_created.uid is not None
    assert resource_created.owner_uid == owner_created.uid

    response = client.get(f'/api/platform/v1/resources/{resource_created.uid}')
    assert response.status_code == 200
    resource_retrieved = ResourceSchema.model_validate(response.json(), strict=True)
    assert resource_created == resource_retrieved

    response = client.get('/api/platform/v1/owners')
    assert response.status_code == 200
    assert len(OwnerListSchema.model_validate(response.json(), strict=True).owners) == 1

    response = client.get('/api/platform/v1/resources')
    assert response.status_code == 200
    assert len(ResourceListSchema.model_validate(response.json(), strict=True).resources) == 1

    owner = OwnerInputSchema(name='modified-owner')
    response = client.put(f'/api/platform/v1/owners/{owner_created.uid}', json=owner.model_dump(mode='json'))
    assert response.status_code == 200
    owner_updated = OwnerSchema.model_validate(response.json(), strict=True)
    assert owner_updated.uid == owner_created.uid
    assert owner_updated.name == 'modified-owner'

    response = client.get(f'/api/platform/v1/resources/{resource_created.uid}')
    assert response.status_code == 200
    resource_retrieved = ResourceSchema.model_validate(response.json(), strict=True)
    assert resource_retrieved.owner_uid == owner_updated.uid

    resource = ResourceInputSchema(name='modified-resource', owner_uid=owner_updated.uid)
    response = client.put(f'/api/platform/v1/resources/{resource_created.uid}', json=resource.model_dump(mode='json'))
    assert response.status_code == 200
    resource_updated = ResourceSchema.model_validate(response.json(), strict=True)
    assert resource_updated.uid == resource_created.uid
    assert resource_updated.owner_uid == owner_updated.uid

    response = client.delete(f'/api/platform/v1/resources/{resource_created.uid}')
    assert response.status_code == 204
    response = client.delete(f'/api/platform/v1/resources/{resource_created.uid}')
    assert response.status_code == 410

    response = client.delete(f'/api/platform/v1/owners/{owner_created.uid}')
    assert response.status_code == 204
    response = client.delete(f'/api/platform/v1/owners/{owner_created.uid}')
    assert response.status_code == 410
