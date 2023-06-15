from classes import errors
from classes.models import SuperAuction, SuperAuctionItem
from ..fetchers import Fetcher
from .super_dto import examples, SuperAuctionDto

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/super',
    tags=["Auctions (superlatanium)"]
)

@router.get('/list', response_model=SuperAuctionDto, responses=examples.get_auction_list)
def _(request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    with fetcher.super_list() as aucs:
        resp = [
            SuperAuctionDto.serialize(x, wrap_response=False, include_items=False)
            for x in aucs
        ]
        return JSONResponse(content=resp)

@router.get('/{id}', response_model=SuperAuctionDto, responses=examples.get_auction)
def _(id: int, request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    auc = fetcher.super_auction(id=id)
    return SuperAuctionDto.serialize(auc)