from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, Context  # type: ignore
from typing import Any


class StudyTrackerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: Context[Any], error: Exception) -> None:
        if isinstance(error, commands.CheckFailure):
            return
        await ctx.reply(f"ERROR: {type(error)} {error}")
    
    @command(name="ping")
    async def ping(self, ctx: Context[Any]) -> None:
        await ctx.reply("Pong!")