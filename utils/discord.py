import discord
from discord import Thread, abc
from discord.ext.commands import Bot  # type: ignore
from typing import Union


async def get_channel(
    bot: Bot, channel_id: int
) -> Union[abc.GuildChannel, abc.PrivateChannel, Thread]:
    try:
        channel_api = await bot.fetch_channel(channel_id)
        return channel_api
    except discord.NotFound:
        raise ValueError(f"Invalid channel_id: `{channel_id}` doesn't exist.")


async def get_user_user(bot: Bot, user_id: int) -> discord.User:
    try:
        user_api = await bot.fetch_user(user_id)
        return user_api
    except discord.NotFound:
        raise ValueError(f"Invalid user_id: `{user_id}` doesn't exist.")
