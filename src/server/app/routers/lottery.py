from classes import errors
from classes.models import Lottery, LotteryItem, LotteryType
from ..fetchers import Fetcher
from .lottery_dto import examples, LotteryDto, LatestLotteryDto

from fastapi import APIRouter, HTTPException, Request


router = APIRouter(
    prefix='/lottery',
    tags=['Lottery']
)

@router.get('/armor/latest', response_model=LatestLotteryDto, responses=examples.get_latest_armor)
def _(request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    latest = fetcher.lottery_latest(type=LotteryType.ARMOR)
    return latest

@router.get('/weapon/latest', response_model=LatestLotteryDto, responses=examples.get_latest_weapon)
def _(request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    latest = fetcher.lottery_latest(type=LotteryType.WEAPON)
    return latest

@router.get('/armor/{id}', response_model=LotteryDto, responses=examples.get_armor)
def _(id: int, request: Request):
    try:
        fetcher: Fetcher = request.app.state.db_fetcher
        lotto = fetcher.lottery(id=id, type=LotteryType.ARMOR)
        return LotteryDto.serialize(lotto)
    except errors.UnparsablePageError:
        return HTTPException(status_code=422, detail='Out of range')

@router.get('/weapon/{id}', response_model=LotteryDto, responses=examples.get_weapon)
def _(id: int, request: Request):
    try:
        fetcher: Fetcher = request.app.state.db_fetcher
        lotto = fetcher.lottery(id=id, type=LotteryType.WEAPON)
        return LotteryDto.serialize(lotto)
    except errors.UnparsablePageError:
        return HTTPException(status_code=422, detail='Out of range')