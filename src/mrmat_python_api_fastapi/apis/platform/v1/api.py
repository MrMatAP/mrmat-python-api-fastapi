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

import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from mrmat_python_api_fastapi.db import get_db
from mrmat_python_api_fastapi.apis import StatusSchema
from .db import Resource, Owner
from .schema import (
    ResourceSchema,
    ResourceInputSchema,
    ResourceListSchema,
    OwnerSchema,
    OwnerInputSchema,
    OwnerListSchema
)

router = APIRouter()


@router.get('/resources',
            name='list_resources',
            summary='List all known resources',
            description='Returns all currently known resources and their metadata',
            response_model=ResourceListSchema)
async def get_resources(session: Session = Depends(get_db)) -> ResourceListSchema:
    try:
        resources = session.query(Resource).all()
        return ResourceListSchema(resources=[ResourceSchema(uid=r.uid,
                                                            name=r.name,
                                                            owner_uid=r.owner_uid)
                                             for r in resources])
    except SQLAlchemyError as e:
        # Handle the error appropriately, maybe raise an HTTPException
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.get('/resources/{uid}',
            name='get_resource',
            summary='Get a single resource',
            description='Return a single resource identified by its resource id',
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'description': 'The resource was not found',
                    'model': StatusSchema
                },
                status.HTTP_200_OK: {
                    'description': 'The requested resource',
                    'model': ResourceSchema
                }
            })
async def get_resource(uid: str,
                       response: Response,
                       session: Session = Depends(get_db)):
    try:
        resource = session.get(Resource, uid)
        if not resource:
            response.status_code = 404
            return StatusSchema(code=404, msg='The resource was not found')
        return resource
    except SQLAlchemyError as e:
        # Handle the error appropriately, maybe raise an HTTPException
        raise HTTPException(status_code=500, detail="A database error occurred") from e

@router.post('/resources',
             name='create_resource',
             summary='Create a resource',
             description='Create a resource owned by the authenticated user',
             response_model=ResourceSchema)
async def create_resource(data: ResourceInputSchema,
                          response: Response,
                          session: Session = Depends(get_db)):
    try:
        resource = Resource(uid=str(uuid.uuid4()), name=data.name, owner_uid=data.owner_uid)
        session.add(resource)
        session.commit()
        response.status_code = 201
        return resource
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.put('/resources/{uid}',
            name='modify_resource',
            summary='Modify a resource',
            description='Modify a resource by its resource id',
            responses={
                status.HTTP_200_OK: {
                    'description': 'The resource was modified',
                    'model': ResourceSchema
                },
                status.HTTP_404_NOT_FOUND: {
                    'description': 'The resource was not found',
                    'model': StatusSchema
                }
            },
            response_model=ResourceSchema)
async def modify_resource(uid: str,
                          data: ResourceInputSchema,
                          response: Response,
                          session: Session = Depends(get_db)):
    try:
        resource = session.get(Resource, uid)
        if not resource:
            response.status_code = 404
            return StatusSchema(code=404, msg='Not found')
        resource.name = data.name
        session.add(resource)
        session.commit()
        return resource
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.delete('/resources/{uid}',
               name='remove_resource',
               summary='Remove a resource',
               description='Remove a resource by its resource id',
               status_code=204,
               responses={
                   status.HTTP_204_NO_CONTENT: {
                       'description': 'The resource was removed'
                   },
                   status.HTTP_410_GONE: {
                       'description': 'The resource was already gone',
                        'model': StatusSchema
                   }
               })
async def remove_resource(uid: str,
                          response: Response,
                          session: Session = Depends(get_db)):
    try:
        resource = session.get(Resource, uid)
        if not resource:
            response.status_code = 410
            return StatusSchema(code=410, msg='The resource was already gone')
        session.delete(resource)
        session.commit()
        response.status_code = 204
        return {}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred") from e



@router.get('/owners',
            name='list_owners',
            summary='List all known owners',
            description='Returns all currently known owners and their metadata',
            response_model=OwnerListSchema)
async def get_owners(session: Session = Depends(get_db)):
    try:
        owners = session.query(Owner).all()
        return OwnerListSchema(owners=[OwnerSchema(uid=o.uid, name=o.name) for o in owners])
    except SQLAlchemyError as e:
        # Handle the error appropriately, maybe raise an HTTPException
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.get('/owners/{uid}',
            name='get_owner',
            summary='Get a single owner',
            description='Return a single owner identified by its owner id',
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'description': 'The owner was not found',
                    'model': StatusSchema
                },
                status.HTTP_200_OK: {
                    'description': 'The requested owner',
                    'model': OwnerSchema
                }
            },
            response_model=OwnerSchema)
async def get_owner(uid: str,
                    response: Response,
                    session: Session = Depends(get_db)):
    try:
        owner = session.get(Owner, uid)
        if not owner:
            response.status_code = 404
            return StatusSchema(code=404, msg='The owner was not found')
        return owner
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.post('/owners',
             name='create_owner',
             summary='Create a owner',
             description='Create a owner',
             response_model=OwnerSchema)
async def create_owner(data: OwnerInputSchema,
                       response: Response,
                       session: Session = Depends(get_db)):
    try:
        owner = Owner(uid=str(uuid.uuid4()), name=data.name)
        session.add(owner)
        session.commit()
        response.status_code = 201
        return owner
    except SQLAlchemyError as e:
        session.rollback()
        # Handle the error appropriately, maybe raise an HTTPException
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.put('/owners/{uid}',
            name='modify_owner',
            summary='Modify a owner',
            description='Modify a owner by its owner id',
            responses={
                status.HTTP_200_OK: {
                    'description': 'The owner was modified',
                    'model': OwnerSchema
                },
                status.HTTP_404_NOT_FOUND: {
                    'description': 'The owner was not found',
                    'model': StatusSchema
                }
            },
            response_model=OwnerSchema)
async def modify_owner(uid: str,
                       data: OwnerInputSchema,
                       response: Response,
                       session: Session = Depends(get_db)):
    try:
        owner = session.get(Owner, uid)
        if not owner:
            response.status_code = 404
            return StatusSchema(code=404, msg='The owner was not found')
        owner.name = data.name
        session.add(owner)
        session.commit()
        return owner
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred") from e


@router.delete('/owners/{uid}',
               name='remove_owner',
               summary='Remove a owner',
               description='Remove a owner by its owner id',
               status_code=204,
               responses={
                   status.HTTP_204_NO_CONTENT: {
                       'description': 'The owner was removed'
                   },
                   status.HTTP_410_GONE: {
                       'description': 'The owner was already gone',
                       'model': StatusSchema
                   }
               })
async def remove_owner(uid: str,
                       response: Response,
                       session: Session = Depends(get_db)):
    try:
        owner = session.get(Owner, uid)
        if not owner:
            response.status_code = status.HTTP_410_GONE
            return
        session.delete(owner)
        session.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred") from e
