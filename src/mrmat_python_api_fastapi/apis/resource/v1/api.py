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

from typing import Union, List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from mrmat_python_api_fastapi.db import get_db
from mrmat_python_api_fastapi.apis import StatusSchema
from .db import Resource, Owner
from .schema import ResourceSchema, ResourceInputSchema, OwnerSchema, OwnerInputSchema

router = APIRouter()


@router.get('/resources',
            name='list_resources',
            summary='List all known resources',
            description='Returns all currently known resources and their metadata',
            response_model=List[ResourceSchema])
async def get_all(db: Session = Depends(get_db)):
    return db.query(Resource).all()


@router.get('/resources/{identity}',
            name='get_resource',
            summary='Get a single resource',
            description='Return a single resource identified by its resource id',
            response_model=Union[ResourceSchema, StatusSchema])
async def get(identity: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).get(identity).one_or_none()
    if not resource:
        return JSONResponse(status_code=404,
                            content=StatusSchema(code=404, msg='Not found').dict())
    return resource


@router.post('/resources',
             name='create_resource',
             summary='Create a resource',
             description='Create a resource owned by the authenticated user',
             response_model=Union[ResourceSchema, StatusSchema])
async def create(data: ResourceInputSchema, db: Session = Depends(get_db)):
    resource = Resource(name=data.name)
    db.add(resource)
    db.commit()
    return resource


@router.put('/resources/{identity}',
            name='modify_resource',
            summary='Modify a resource',
            description='Modify a resource by its resource id',
            response_model=Union[ResourceSchema, StatusSchema])
async def modify(identity: int, data: ResourceInputSchema, db: Session = Depends(get_db)):
    resource = db.query(Resource).get(identity)
    if not resource:
        return JSONResponse(status_code=404,
                            content=StatusSchema(code=404, msg='Not found').dict())
    resource.name = data.name
    db.add(resource)
    db.commit()
    return resource


@router.delete('/resources/{identity}',
               name='remove_resource',
               summary='Remove a resource',
               description='Remove a resource by its resource id',
               status_code=204,
               responses={
                   status.HTTP_204_NO_CONTENT: {'description': 'The resource was removed'},
                   status.HTTP_410_GONE: {'description': 'The resource was already gone'}
               })
async def remove(identity: int, response: Response, db: Session = Depends(get_db)):
    resource = db.query(Resource).get(identity)
    if not resource:
        return JSONResponse(status_code=204,
                            content=StatusSchema(code=404, msg='Not found').dict())
    db.delete(resource)
    db.commit()
    response.status_code = 410
    return {}



@router.get('/owners',
            name='list_owners',
            summary='List all known owners',
            description='Returns all currently known owners and their metadata',
            response_model=List[OwnerSchema])
async def get_all(db: Session = Depends(get_db)):
    return db.query(Owner).all()


@router.get('/owners/{identity}',
            name='get_owner',
            summary='Get a single owner',
            description='Return a single owner identified by its owner id',
            response_model=Union[OwnerSchema, StatusSchema])
async def get(identity: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(identity)
    if not owner:
        return JSONResponse(status_code=404,
                            content=StatusSchema(code=404, msg='Not found').dict())
    return owner


@router.post('/owners',
             name='create_owner',
             summary='Create a owner',
             description='Create a owner',
             response_model=Union[OwnerSchema, StatusSchema])
async def create(data: OwnerInputSchema, db: Session = Depends(get_db)):
    owner = Owner(name=data.name, client_id='TODO')
    db.add(owner)
    db.commit()
    return owner


@router.put('/owners/{identity}',
            name='modify_owner',
            summary='Modify a owner',
            description='Modify a owner by its owner id',
            response_model=Union[OwnerSchema, StatusSchema])
async def modify(identity: int, data: ResourceInputSchema, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(identity)
    if not owner:
        return JSONResponse(status_code=404,
                            content=StatusSchema(code=404, msg='Not found').dict())
    owner.name = data.name
    db.add(owner)
    db.commit()
    return owner


@router.delete('/owners/{identity}',
               name='remove_owner',
               summary='Remove a owner',
               description='Remove a owner by its owner id',
               status_code=204,
               responses={
                   status.HTTP_204_NO_CONTENT: {'description': 'The owner was removed'},
                   status.HTTP_410_GONE: {'description': 'The owner was already gone'}
               })
async def remove(identity: int, response: Response, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(identity)
    if not owner:
        response.status_code = status.HTTP_410_GONE
        return
    db.delete(owner)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
