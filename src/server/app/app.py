from classes.proxy_session import ProxySession
from classes.models import Base
from classes.parsers import LotteryParser, SuperParser, UserParser
from config import env, paths, secrets
from .fetchers import Fetcher
from .routers.lottery import router as LotteryRouter
from .routers.super import router as SuperRouter

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine


app = FastAPI(debug=True)
app.include_router(LotteryRouter)
app.include_router(SuperRouter)

@app.on_event('startup')
async def on_startup():
    state = app.state

    db_path = str(paths.DATA_DIR / "hvdata.sqlite").replace('\\','\\\\')
    engine = create_engine(f'sqlite:///{db_path}', echo=0)
    db_session = sessionmaker(engine, future=True)
    hv_session = ProxySession(server_address=env.hv_session.address, authkey=secrets.hv_session.authkey)

    Base.metadata.create_all(engine)

    state.lotto_parser = LotteryParser(session=hv_session)
    state.super_parser = SuperParser(session=hv_session)
    state.user_parser = UserParser(session=hv_session)
    state.db_fetcher = Fetcher(
        db_session=db_session, 
        lotto_parser=state.lotto_parser,
        super_parser=state.super_parser,
        user_parser=state.user_parser
    )
