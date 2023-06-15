from . import Base
from .user import User
from .uuid_mixin import UuidMixin

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SuperAuction(UuidMixin, Base):
    __tablename__ = 'super_auction'
    
    id: int = Column(Integer, primary_key=True)

    end_date: Float = Column(Float, nullable=False)
    items = relationship('SuperAuctionItem', back_populates='auction')
    number: str = Column(String, nullable=False)

class SuperAuctionItem(UuidMixin, Base):
    __tablename__ = 'super_auction_item'

    auction_id: int = Column(Integer, ForeignKey('super_auction.id'), primary_key=True)
    auction = relationship('SuperAuction', back_populates='items')

    category: str = Column(String, primary_key=True)
    number: int = Column(Integer, primary_key=True)

    description: str = Column(String)
    name: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)
    quantity: int = Column(Integer, nullable=False)

    equip_id: int = Column(Integer, ForeignKey('equip.id'))
    equip_key: str = Column(String, ForeignKey('equip.key'))

    buyer_raw: str = Column(String)
    buyer_id: int = Column(Integer, ForeignKey('user.id'))
    buyer: User = relationship('User', backref='super_auction_buys', foreign_keys=[buyer_id])

    seller_raw: str = Column(String, nullable=False)
    seller_id: int = Column(Integer, ForeignKey('user.id'))
    seller: User = relationship('User', backref='super_auction_sells', foreign_keys=[seller_id])
