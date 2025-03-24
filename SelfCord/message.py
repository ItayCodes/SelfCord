from .http_client import HTTPClient
from .exceptions import HTTPException


class Message:
    def __init__(self, message_id: int, content: str, http_client: HTTPClient):
        self.id = message_id
        self.content = content
        self.__http = http_client

    def __str__(self):
        return f"Message(id={self.id}, content={self.content})"

    __repr__ = __str__
