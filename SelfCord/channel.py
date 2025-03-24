class BaseChannel:
    def __init__(self, channel_id: int):
        self.id = channel_id

    def __str__(self):
        return f"BaseChannel(id={self.id})"

    __repr__ = __str__


class TextChannel(BaseChannel):
    def __init__(self, channel_id: int, name: str, nsfw: bool, topic: str = None):
        super().__init__(channel_id)
        self.name = name
        self.nsfw = nsfw
        self.topic = topic

    def __str__(self):
        return f"TextChannel(id={self.id}, name={self.name}, nsfw={self.nsfw}, topic={self.topic})"

    __repr__ = __str__


# Check bit-rate
class VoiceChannel(BaseChannel):
    def __init__(self, channel_id: int, name: str, bit_rate: int = 96000):
        super().__init__(channel_id)
        self.name = name
        self.bit_rate = bit_rate


class DMChannel(BaseChannel):
    pass


class GroupDMChannel(BaseChannel):
    pass


class GuildCategoryChannel(BaseChannel):
    pass


class GuildAnnouncementChannel(BaseChannel):
    pass


class AnnouncementThreadChannel(BaseChannel):
    pass


class PublicThreadChannel(BaseChannel):
    pass


class PrivateThreadChannel(BaseChannel):
    pass


class GuildStageVoiceChannel(BaseChannel):
    pass


class GuildDirectoryChannel(BaseChannel):
    pass


class GuildForumChannel(BaseChannel):
    pass


class GuildMediaChannel(BaseChannel):
    pass
