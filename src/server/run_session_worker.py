from config import env, secrets
from hvpytils import HvSession, HvCookies

from multiprocessing.connection import Listener
from requests import Request

import logging

# @todo error handling


LOG = logging.getLogger('SessionWorker')
LOG.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
LOG.addHandler(handler)

logging.getLogger('HvSession').addHandler(handler)
logging.getLogger('HvSession').setLevel(logging.DEBUG)


login_info = HvCookies(
    ipb_member_id=secrets.hv_session.ipb_member_id, 
    ipb_pass_hash=secrets.hv_session.ipb_pass_hash
)
session = HvSession(cookies=login_info)

with Listener(env.hv_session.address, authkey=secrets.hv_session.authkey) as listener:
    while True:
        try:
            with listener.accept() as conn:
                LOG.debug('Connection started.')
                kwargs = conn.recv()
                
                LOG.info(f'Received {kwargs}')
                resp = session.send(**kwargs)

                conn.send(resp)
                LOG.debug('Connection ended.')
        except ConnectionResetError:
            LOG.info(f'Connection reset.')