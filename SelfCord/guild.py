from .http_client import HTTPClient
from .exceptions import HTTPException
from .message import Message


class Guild:
    """
    Represents a Guild object

    Attributes:
        id (int): The guild's ID.
        name (str): The guild's name.
    """

    def __init__(self, guild_id: int, name: str, http_client: HTTPClient):
        self.id = guild_id
        self.name = name
        self.__http = http_client

    def __str__(self):
        return f"Guild(id={self.id}, name={self.name})"

    __repr__ = __str__

    def delete(self) -> bool:
        endpoint = f"guilds/{self.id}"
        response = self.__http.request("DELETE", endpoint)

        if response.status_code == 204:
            return True
        try:
            data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        raise HTTPException(data)

    def search_messages(self, content: str = None, authors: list = None, channels: list = None,
                        include_nsfw: bool = False, offset: int = None, limit: int = 25):
        endpoint = f"guilds/{self.id}/messages/search"
        params = {}

        if content:
            params["content"] = content
        if authors:
            for author in authors:
                params.setdefault("author_id", []).append(author)
        if channels:
            for channel in channels:
                params.setdefault("channel_id", []).append(channel)
        if include_nsfw:
            params["include_nsfw"] = include_nsfw
        if offset:
            params["offset"] = offset

        all_messages = []
        while True:
            response = self.__http.request("GET", endpoint, params=params)

            try:
                messages_data = response.json()
            except ValueError:
                raise HTTPException("Invalid JSON response from server.")

            if response.status_code == 200:
                messages = []
                for message in messages_data["messages"]:
                    message = Message(
                        message[0]["id"],
                        message[0]["content"],
                        self.__http
                    )
                    messages.append(message)

                remaining_limit = limit - len(all_messages)
                if remaining_limit <= 0:
                    break

                for msg in messages[:remaining_limit]:
                    yield msg

                all_messages.extend(messages)

                if len(messages_data["messages"]) == 0:
                    break

                params["offset"] = params.get("offset", 0) + 25

            else:
                raise HTTPException(messages_data)
