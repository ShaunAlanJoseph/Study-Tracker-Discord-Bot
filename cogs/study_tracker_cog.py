from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, Context  # type: ignore
from typing import Any
from logging import info, error as err


class StudyTrackerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        info("StudyTrackerCog has been loaded.")

    async def cog_command_error(self, ctx: Context[Any], error: Exception) -> None:
        if isinstance(error, commands.CheckFailure):
            return
        err(f"An excpetion occured: {error}", exc_info=True)
        await ctx.reply(f"ERROR: {type(error)} {error}")
    
    @command(name="ping")
    async def ping(self, ctx: Context[Bot]):
        await ctx.reply("Pong!")