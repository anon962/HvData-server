from . import Base
from config import paths
from .user import User
from .uuid_mixin import UuidMixin

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

import enum, sqlalchemy, uuid


class LotteryType(enum.Enum):
    WEAPON = str(paths.HV_LOTTO_WEAPON)
    ARMOR = str(paths.HV_LOTTO_ARMOR)

class Lottery(Base, UuidMixin):
    __tablename__ = 'lottery'

    id: int = Column(Integer, primary_key=True)
    type: LotteryType = Column(sqlalchemy.Enum(LotteryType), primary_key=True)

    tickets: int = Column(Integer, nullable=False)

    items = relationship('LotteryItem', back_populates='lottery')
    
class LotteryItem(Base, UuidMixin):
    __tablename__ = 'lottery_item'
    __table_args__ = (
        # composite foreign keys need to be at least this ugly
        ForeignKeyConstraint(['id', 'type'], [Lottery.id, Lottery.type]),
    )

    id: int = Column(Integer, primary_key=True)
    type: LotteryType = Column(sqlalchemy.Enum(LotteryType), primary_key=True)

    name: str = Column(String, nullable=False)
    place: int = Column(Integer, primary_key=True)
    quantity: int = Column(Integer, nullable=False)

    raw_winner: str = Column(String, nullable=False)
    winner_id: User = Column(Integer, ForeignKey('user.id'))
    winner: User = relationship('User', backref='lottery_items')

    lottery: Lottery = relationship('Lottery', back_populates='items')
