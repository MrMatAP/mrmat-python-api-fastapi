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
from sqlalchemy import ForeignKey, String, UniqueConstraint, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from mrmat_python_api_fastapi import ORMBase


class Owner(ORMBase):
    __tablename__ = 'owners'
    __schema__ = 'mrmat-python-api-fastapi'
    uid: Mapped[str] = mapped_column(String, primary_key=True)

    client_id: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    resources: Mapped[list["Resource"]] = relationship('Resource', back_populates='owner')


class Resource(ORMBase):
    __tablename__ = 'resources'
    __schema__ = 'mrmat-python-api-fastapi'
    uid: Mapped[str] = mapped_column(String, primary_key=True)
    owner_uid: Mapped[str] = mapped_column(String, ForeignKey('owners.uid'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    owner: Mapped["Owner"] = relationship('Owner', back_populates='resources')
    __table_args__ = (UniqueConstraint('owner_uid', 'name', name='no_duplicate_names_per_owner'),)
