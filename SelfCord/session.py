from typing import Dict

from SelfCord import HTTPClient


class Session:
    def __init__(self, id_hash: str, approx_last_used_time: str, client_info: Dict[str, str], http_client: HTTPClient):
        self.id_hash = id_hash
        self.approx_last_used_time = approx_last_used_time
        self.client_info = client_info
        self.__http = http_client

    def __str__(self):
        return f"Session(id_hash={self.id_hash}, approx_last_used_time={self.approx_last_used_time}, client_info={self.client_info})"

    __repr__ = __str__
