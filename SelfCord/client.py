from functools import cached_property
from .channel import *
from .http_client import HTTPClient
from .guild import Guild
from .message import Message
from .session import Session
from .user import User
from .exceptions import HTTPException, InvalidGuildNameException
from .types import Channel


class Client:
    """
    Represents a Client object.
    """

    def __init__(self, token: str):
        self.token = token
        self.__http = HTTPClient(token)

    def __str__(self):
        return f"Client(token={self.token})"

    __repr__ = __str__

    @cached_property  # Think about a better approach than caching user info
    def user(self) -> User | HTTPException:
        return self._get_client_user()

    @cached_property  # Maybe shouldn't be cached considering it can change at any second
    def sessions(self) -> list[Session] | HTTPException:
        return self._get_client_sessions()

    def _get_client_user(self) -> User | HTTPException:
        endpoint = f"users/@me"
        response = self.__http.request("GET", endpoint)

        try:
            client_data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            return User(
                client_data["id"],
                client_data["username"],
                client_data["global_name"],
                client_data["avatar"],
                self.__http
            )
        else:
            raise HTTPException(client_data)

    def _get_client_sessions(self) -> list[Session] | HTTPException:
        endpoint = f"auth/sessions"
        response = self.__http.request("GET", endpoint)

        try:
            client_sessions = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            sessions = []
            for session in client_sessions["user_sessions"]:
                session = Session(
                    session["id_hash"],
                    session["approx_last_used_time"],
                    session["client_info"],
                    self.__http
                )
                sessions.append(session)
            return sessions
        else:
            raise HTTPException(client_sessions)

    def get_guild(self, guild_id: int) -> Guild | HTTPException:
        """
        Fetches a guild by its ID.

        :param guild_id: The guild's ID.
        :return: A Guild object or raises HTTPException.
        """
        endpoint = f"guilds/{guild_id}"
        response = self.__http.request("GET", endpoint)

        try:
            guild_data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            return Guild(
                guild_data["id"],
                guild_data["name"],
                self.__http
            )
        else:
            raise HTTPException(guild_data)

    def get_user(self, user_id: int) -> User | HTTPException:
        """
        Fetches a user by its ID.

        :param user_id: The user's ID.
        :return: A User object or raises HTTPException.
        """
        endpoint = f"users/{user_id}/profile"
        response = self.__http.request("GET", endpoint)

        try:
            user_data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            return User(
                user_data["user"]["id"],
                user_data["user"]["username"],
                user_data["user"]["global_name"],
                user_data["user"]["avatar"],
                self.__http
            )
        else:
            raise HTTPException(user_data)

    def get_channel(self, channel_id: int) -> Channel:
        """
        Fetches a channel by its ID.

        :param channel_id: The channel's ID.
        :return: A Channel object relative to the channel type, or raises HTTPException.
        """
        endpoint = f"channels/{channel_id}"
        response = self.__http.request("GET", endpoint)

        try:
            channel_data = response.json()
            channel_type = channel_data.get("type")
            channel_id = channel_data.get("id")
            # TODO: Check if name is missing on some channel types or if it's global
            channel_name = channel_data.get("name")
            channel_nsfw = channel_data.get("nsfw")
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            if channel_type == 0:
                return TextChannel(channel_id, channel_name, channel_nsfw)
            elif channel_type == 1:
                return DMChannel(channel_id)
            elif channel_type == 2:
                return VoiceChannel(channel_id, channel_name)
            elif channel_type == 3:
                return GroupDMChannel(channel_id)
            elif channel_type == 4:
                return GuildCategoryChannel(channel_id)
            elif channel_type == 5:
                return GuildAnnouncementChannel(channel_id)
            elif channel_type == 10:
                return AnnouncementThreadChannel(channel_id)
            elif channel_type == 11:
                return PublicThreadChannel(channel_id)
            elif channel_type == 12:
                return PrivateThreadChannel(channel_id)
            elif channel_type == 13:
                return GuildStageVoiceChannel(channel_id)
            elif channel_type == 14:
                return GuildDirectoryChannel(channel_id)
            elif channel_type == 15:
                return GuildForumChannel(channel_id)
            elif channel_type == 16:
                return GuildMediaChannel(channel_id)
            else:
                raise ValueError(f"Unknown channel type: {channel_type}")
        else:
            raise HTTPException(channel_data)

    def get_message(self, channel_id: int, message_id: int):
        endpoint = f"channels/{channel_id}/messages"
        params = {
            "limit": 1,
            "around": message_id
        }
        response = self.__http.request("GET", endpoint, params=params)

        try:
            message_data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 200:
            return Message(
                message_data[0]["id"],
                message_data[0]["content"],
                self.__http
            )
        else:
            raise HTTPException(message_data)

    # Unknown message error, code 10008
    def create_guild(self, guild_name: str, icon: bytes = None) -> Guild | HTTPException | InvalidGuildNameException:
        if not (2 <= len(guild_name) <= 100):
            raise InvalidGuildNameException("Guild name must be between 2 and 100 characters.")
        endpoint = "guilds"
        response = self.__http.request("POST", endpoint, json={"name": guild_name, "icon": icon})

        try:
            guild_data = response.json()
        except ValueError:
            raise HTTPException("Invalid JSON response from server.")

        if response.status_code == 201:
            return Guild(
                guild_data["id"],
                guild_data["name"],
                self.__http
            )
        else:
            raise HTTPException(guild_data)
