from classes.models import Lottery, LotteryItem, LotteryType, User
from classes.parsers import LotteryParser
from . import _roll

from enum import Enum
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import random, uuid


class LotteryTypeDto(str, Enum):
    WEAPON = 'weapon'
    ARMOR = 'armor'

class LotteryUserDto(BaseModel):
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

class LotteryItemDto(BaseModel):
    name: str
    place: int
    quantity: int
    winner: LotteryUserDto
        
    @classmethod
    def serialize(cls, it: LotteryItem):
        if it.winner:
            winner = LotteryUserDto.serialize(it.winner)
        else:
            winner = dict(name=it.raw_winner)

        return dict(
            name = it.name,
            place = it.place,
            quantity = it.quantity,
            winner = winner
        )

class LotteryDto(BaseModel):
    id: int
    type: LotteryTypeDto
    tickets: int
    items: list[LotteryItemDto]

    @classmethod
    def serialize(cls, l: Lottery):
        return JSONResponse(content=dict(
            id = l.id,
            type = getattr(LotteryTypeDto, l.type.name).value,
            tickets = l.tickets,
            items = [LotteryItemDto.serialize(x) for x in l.items]
        ))

class LatestLotteryDto(BaseModel):
    id: int
    start: int

def _sample_lotto(grand_prize='grand prize'):
    users = _roll.users()
    uuids = [uuid.uuid4() for i in range(5)]

    return dict(
        id=random.randint(1,10000),
        type=LotteryTypeDto.WEAPON,
        tickets=random.randint(10**4, 10**8),
        items=[
            dict(
                name=grand_prize,
                place=0,
                quantity=1,
                winner=dict(name='프레이', uuid=uuids.pop())
            ),
            dict(
                name='Golden Lottery Tickets',
                place=1,
                quantity=4,
                winner=dict(name=users.pop(), uuid=uuids.pop())
            ),
            dict(
                name='Caffeinated Candies',
                place=2,
                quantity=16,
                winner=dict(name=users.pop(), uuid=uuids.pop())
            ),
            dict(
                name='Chaos Tokens',
                place=3,
                quantity=160,
                winner=dict(name=users.pop(), uuid=uuids.pop())
            ),
            dict(
                name='Chaos Tokens',
                place=4,
                quantity=160,
                winner=dict(name=users.pop(), uuid=uuids.pop())
            )
        ]
    )

class examples:
    get_weapon = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'value': {
                                **_sample_lotto(grand_prize='Peerless Hallowed Oak Staff of Heimdall'),
                                'type': LotteryTypeDto.WEAPON
                            }
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Lottery Id'
        }
    }

    get_armor = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'value': {
                                **_sample_lotto(grand_prize='Peerless Mystic Phase Robe of Fenrir'),
                                'type': LotteryTypeDto.ARMOR
                            }
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Lottery Id'
        }
    }

    get_latest_armor = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'description': 'The first armor lottery started at 1396094400s epoch time.',
                            'value': dict(
                                id = 101,
                                start = LotteryParser.START_DATES[LotteryType.ARMOR] + 100*86400
                            )
                        }
                    }
                }
            }
        }
    }

    get_latest_weapon = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'description': 'The first weapon lottery started at 1379116800s epoch time.',
                            'value': dict(
                                id = 101,
                                start = LotteryParser.START_DATES[LotteryType.WEAPON] + 100*86400
                            )
                        }
                    }
                }
            }
        }
    }