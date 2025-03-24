from .http_client import HTTPClient


class User:
    def __init__(self, user_id: int, username: str, global_name: str | None, avatar: str | None,
                 http_client: HTTPClient):
        self.id = user_id
        self.username = username
        self.global_name = global_name
        self.avatar = avatar
        self.__http = http_client

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, global_name={self.global_name}, avatar={self.avatar})"

    __repr__ = __str__
