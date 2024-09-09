from asyncio import run
from discord import Intents
from discord.ext import commands
from logging import info

from config import DISCORD_API_TOKEN, ADMIN_CHANNEL_ID
from database import Database
from study_tracker_cog import StudyTrackerCog


async def main():
    Database.establish_connection()

    bot = commands.Bot(command_prefix="$", intents=Intents.all())
    await bot.add_cog(StudyTrackerCog(bot))

    @bot.event
    async def on_ready():  # type: ignore
        assert bot.user is not None
        info(f"Logged in as User: {bot.user.name} ID: {bot.user.id}")
        HQ = await bot.fetch_channel(ADMIN_CHANNEL_ID)
        await HQ.send(f"Logged in as User: {bot.user.name} ID: {bot.user.id}")  # type: ignore

    assert DISCORD_API_TOKEN is not None
    await bot.start(DISCORD_API_TOKEN)


if __name__ == "__main__":
    run(main())
