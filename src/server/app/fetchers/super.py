from classes.parsers import SuperParser
from classes.models import SuperAuction

from sqlalchemy import select
from sqlalchemy.orm import Session, subqueryload

import contextlib, time


class SuperFetcher:
    db_session: Session
    super_parser: SuperParser

    _last_list_scan: float = 0

    def super_auction(self, id: int):
        with self.db_session.begin() as session:
            stmt = select(SuperAuction).where(SuperAuction.id == id).options(subqueryload('*'))
            auc = session.execute(stmt).scalar()

            if auc is None:
                aucs = self.super_parser.fetch_list()
                [session.merge(x) for x in aucs]
                
                auc = next(x for x in aucs if x.id == id)
                if auc is None:
                    raise IndexError
            else:
                session.expunge_all()

            if len(auc.items) == 0:
                auc.items = self.super_parser.fetch_items(id=id)
                [session.merge(x) for x in auc.items]

        return auc
    
    @contextlib.contextmanager
    def super_list(self):
        with self.db_session.begin() as session:
            stmt = select(SuperAuction).order_by(SuperAuction.end_date.desc())
            latest: SuperAuction = session.execute(stmt).scalar()

            elapsed = time.time() - latest.end_date
            if elapsed > 6.25 * 86400:
                if time.time() - self._last_list_scan > 15*60:
                    aucs = self.super_parser.fetch_list()
                    [session.merge(x) for x in aucs]

                    self._last_list_scan = time.time()
            
            aucs = session.execute(stmt).scalars().all()
            yield aucs