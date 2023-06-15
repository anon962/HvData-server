from classes.models import SuperAuction, SuperAuctionItem, User
from classes.parsers import SuperParser
from . import _roll

from enum import Enum
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import random


class SuperAuctionUserDto(BaseModel):
    name: str
    id: Optional[int]

    @classmethod
    def serialize(cls, user: User):
        if user is None: 
            return None
        else:
            return dict(
                name = user.current_name,
                id = user.id
            )

class SuperAuctionItemDto(BaseModel):
    category: str
    number: int

    name: str
    description: str
    price: int
    quantity: int

    equip_id: Optional[int]
    equip_key: Optional[str]

    buyer: Optional[SuperAuctionUserDto]
    seller: SuperAuctionUserDto

    @classmethod
    def serialize(cls, it: SuperAuctionItem):
        if it.buyer:
            buyer = SuperAuctionUserDto.serialize(it.buyer)
        else:
            if it.buyer_raw:
                buyer = dict(name=it.buyer_raw)
            else:
                buyer = None

        if it.seller:
            seller = SuperAuctionUserDto.serialize(it.seller)
        else:
            seller = dict(name=it.seller_raw)
        
        return dict(
            category = it.category,
            number = it.number,

            description = it.description,
            name = it.name,
            price = it.price,
            quantity = it.quantity,

            equip_id = it.equip_id,
            equip_key = it.equip_key,

            buyer = buyer,
            seller = seller
        )

class SuperAuctionDto(BaseModel):
    id: int
    end_date: float
    number: str
    items: list[SuperAuctionItemDto]

    @classmethod
    def serialize(cls, auc: SuperAuction, wrap_response=True, include_items=True):
        result = dict(
            id = auc.id,
            end_date = auc.end_date,
            number = auc.number
        )

        if include_items:
            result['items'] = [SuperAuctionItemDto.serialize(x) for x in auc.items]

        if wrap_response:
            result = JSONResponse(content=result)

        return result

def _sample_item():
    users = _roll.users()

    buyer = random.choice([
        None,
        dict(name=users.pop(), id=random.randint(1,10000))
    ])
    
    seller = dict(
        name=users.pop(),
        id=random.randint(1,10000)
    )

    def _sample_mat():
        name = random.choice([
            'High-Grade Cloth',
            'Binding of Slaughter',
            'Energy Drink',
            'Amnesia Shard',
            'Low-Grade Wood',
            'Binding of the Barrier',
            'Binding of Friendship',
            'Happy Pills'
        ])
    
        quantity = random.randint(1,100) * 10**random.randint(0,3)

        if buyer:
            price = random.randint(50, 10000) # in thousands

            per_unit = price / quantity
            if per_unit < 1:
                description = f'{int(per_unit*1000)}c'
            else:
                description = f'{int(per_unit*10)/10}k'
        else:
            price = 0
            description = ''

        return dict(
            category='mat',
            number=random.randint(1,99),
            
            name=name,
            description=description,
            price=price*1000,
            quantity=quantity,

            buyer=buyer,
            seller=seller
        )

    def _sample_equip():
        prefix = random.sample(['Legendary', 'Peerless'], k=1, counts=[50,1])[0]

        name = prefix + ' ' + random.choice([
            'Charged Phase Shoes of Niflheim',
            'Onyx Phase Pants of Surtr',
            'Savage Power Armor of Balance',
            'Hallowed Oak Staff of Heimdall',
            'Fiery Redwood Staff of Surtr',
            'Onyx Shade Leggings of the Shadowdancer',
            'Arctic Rapier of Slaughter',
            'Hallowed Katana of Slaughter',
            'Arctic Redwood Staff of Niflheim',
            'Zircon Power Gauntlets of Protection',
            'Tempestuous Willow Staff of Destruction',
            'Ruby Power Boots of Warding',
            'Jade Force Shield of Dampening',
            'Ethereal Rapier of Slaughter'
        ])

        description = random.choice([
            '500, ADB 46%',
            '333, Wind EDB 15%',
            '415, ADB 93%',
            '492, ADB 3%',
            '385, Forb Prof 25%',
            '385, ADB 52%',
            '398, ADB 100%',
            '439, Holy EDB 59%',
            '354, ADB 91%',
            '475, Divine Prof 101%',
            '500, Elem Prof 97%',
            '331, Str Dex Agi, BLK 59%',
            '452, IW 10, ADB 59%',
            '458, MDB 55%, Cold EDB 47%',
            '482, ADB 79%',
            '421, Elem Prof 68%',
            '341, ADB 88%',
            '400, Elec EDB 40%',
            '422, Dark EDB 92%',
        ])

        return dict(
            category = random.choice(['one','two','sta','shd','clo','lig','hea']),
            number=random.randint(1,99),
            
            name=name,
            description=description,
            price=random.randint(50,80000)*1000 if buyer else 0,
            quantity=1,
            
            equip_id=random.randint(10**4, 10**8),
            equip_key=hex(random.randint(68719476736, 1099511627775))[2:], # (10 0000 0000)_16 to (FF FFFF FFFF)_16

            buyer=buyer,
            seller=seller
        )

    return random.choice([
        _sample_mat(),
        _sample_equip()
    ])

def _sample_auction(num_items=0):
    number = f'{random.randint(11,200)}{random.sample(["", ".5"], k=1, counts=[2,1])[0]}'

    return dict(
        id=random.randint(1,1000),
        end_date=random.random()*(10**9) + 10**9,
        number=number,
        items=[_sample_item() for i in range(num_items)]
    )

class examples:
    get_auction_list = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'value': [
                                _sample_auction()
                                for i in range(7)
                            ]
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Auction Id'
        }
    }

    get_auction = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'description': 'Do not assume the item description is populated with any consistency, especially for mats.',
                            'value': {
                                **_sample_auction(num_items=random.randint(10,20))
                            }
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Auction Id'
        }
    }