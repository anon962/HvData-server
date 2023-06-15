from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, subqueryload

from app.fetcher import LotteryFetcher
from classes import ProxySession
from classes.models import Lottery, LotteryType
from classes.parsers import LotteryParser
from config import env, paths, secrets


db_path = str(paths.DATA_DIR / "hvdata.sqlite").replace('\\','\\\\')
engine = create_engine(f'sqlite:///{db_path}', echo=0)
db_session = sessionmaker(engine, future=True)

hv_session = ProxySession(server_address=env.hv_session.address, authkey=secrets.hv_session.authkey)
lotto_parser = LotteryParser(session=hv_session)

fetcher = LotteryFetcher()
fetcher.db_session = db_session
fetcher.lotto_parser = lotto_parser


for type in [LotteryType.ARMOR, LotteryType.WEAPON]:
    latest = fetcher.lottery_latest(type)

    bin_size = 500
    steps = [bin_size*i+1 for i in range(latest['id'] // bin_size + 1)]

    for st in steps:
        with db_session.begin() as session:
            lst = []

            for id in range(st, st+bin_size):
                if id == latest['id']: break
                print(type, str(id).rjust(4,'0'))

                stmt = select(Lottery).where(Lottery.id == id, Lottery.type == type)
                lotto = session.execute(stmt).scalar()

                if lotto is None:
                    lotto = lotto_parser.fetch_one(type=type, id=id)
                    lst.append(lotto)

            print('merging')
            lotto_parser.initialize_winners()
            [session.merge(x) for x in lst]