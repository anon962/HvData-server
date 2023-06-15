from . import Base
from .uuid_mixin import UuidMixin

from sqlalchemy import Column, Float, Integer, String


class User(UuidMixin, Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)

    avatar: str = Column(String)
    current_name: str = Column(String, nullable=False)
    group: str = Column(String)
    joined: float = Column(Float)
    level: int = Column(Integer)
    signature: str = Column(String)

    last_fetch_profile: float = Column(Float) # https://forums.e-hentai.org/index.php?showuser=###
    last_fetch_search: float = Column(Float) # https://forums.e-hentai.org/index.php?act=members
    last_fetch_post: float = Column(Float) # https://forums.e-hentai.org/index.php?showtopic=###

    def last_update(self, attr: str) -> float:
        attr = attr.strip().lower()

        profile = self.last_fetch_profile
        post = self.last_fetch_post
        search = self.last_fetch_search

        if attr == 'avatar':
            return max(profile, post)
        elif attr == 'current_name':
            return max(profile, post, search)
        elif attr == 'group':
            return max(profile, post, search)
        elif attr == 'joined':
            return max(profile, post, search)
        elif attr == 'level':
            return max(profile, post)
        elif attr == 'signature':
            return max(profile, post)
        else:
            raise ValueError