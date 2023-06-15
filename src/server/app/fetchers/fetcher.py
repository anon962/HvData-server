from classes.parsers import LotteryParser, SuperParser, UserParser
from .lottery import LotteryFetcher
from .super import SuperFetcher

from sqlalchemy.orm import Session

import attr


@attr.s(auto_attribs=True)
class Fetcher(LotteryFetcher, SuperFetcher):
    db_session: Session
    lotto_parser: LotteryParser
    super_parser: SuperParser
    user_parser: UserParser