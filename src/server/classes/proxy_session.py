from hvpytils import HvSession

from multiprocessing.connection import Client


class ProxySession(HvSession):
    """
    The login process and all other requests are performed remotely. 
    You do not need to supply HV cookies / credentials to this class. Instead, supply the remote server address and authkey.
    """

    RATE_LIMIT = 0

    authkey: str
    server_address: tuple[str, int]

    def __init__(self, server_address: tuple[str, int], authkey: str, **kwargs):
        super().__init__(credentials=('',''), **kwargs)

        self.server_address = server_address
        self.authkey = authkey

    def send(self, method: str, url: str, **kwargs):
        with Client(self.server_address, authkey=self.authkey) as conn:
            conn.send(dict(method=method, url=url, **kwargs))
            resp = conn.recv()
            return resp

        return super().prepare_request(method, url, **kwargs)
    
    def login(self):
        # ClientSession's don't need to be logged in. The remote session handles this.
        pass