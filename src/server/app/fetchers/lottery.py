from classes.parsers import LotteryParser
from classes.models import Lottery, LotteryItem, LotteryType

from sqlalchemy import select
from sqlalchemy.orm import Session, subqueryload

import time


class LotteryFetcher:
    db_session: Session
    lotto_parser: LotteryParser

    def lottery(self, id: int, type: LotteryType):
        with self.db_session.begin() as session:
            stmt = select(Lottery).where(Lottery.id == id, Lottery.type == type).options(subqueryload('*'))
            lotto = session.execute(stmt).scalar()
            
            if lotto is None:
                lotto = self.lotto_parser.fetch_one(type=type, id=id)
                self.lotto_parser.initialize_winners()
                session.merge(lotto)
            else:
                session.expunge_all()

        return lotto

    def lottery_latest(self, type: LotteryType):
        seconds_elapsed = time.time() - LotteryParser.START_DATES[type]
        days_elapsed = int(seconds_elapsed // 86400)
                
        return dict(
            id = 1+days_elapsed,
            start = LotteryParser.START_DATES[type] + days_elapsed*86400
        )