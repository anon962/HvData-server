from sqlalchemy import Column, String

import uuid


class UuidMixin:
    uuid: str = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))

    def __init__(self, **kwargs):
        if 'uuid' not in kwargs:
            kwargs['uuid'] = str(uuid.uuid4())
        super().__init__(**kwargs)