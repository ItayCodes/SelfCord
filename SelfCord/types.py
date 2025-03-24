from .channel import TextChannel, VoiceChannel, DMChannel, GroupDMChannel, \
    GuildCategoryChannel, GuildAnnouncementChannel, AnnouncementThreadChannel, PublicThreadChannel, \
    PrivateThreadChannel, GuildStageVoiceChannel, GuildDirectoryChannel, GuildForumChannel, GuildMediaChannel

Channel = TextChannel | VoiceChannel | DMChannel | GroupDMChannel | \
          GuildCategoryChannel | GuildAnnouncementChannel | AnnouncementThreadChannel | PublicThreadChannel | \
          PrivateThreadChannel | GuildStageVoiceChannel | GuildDirectoryChannel | GuildForumChannel | GuildMediaChannel
