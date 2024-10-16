from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, Context  # type: ignore
from typing import Any
from logging import info, error as err
from utils.context_manager import ctx_mgr


class StudyTrackerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        info("StudyTrackerCog has been loaded.")

    async def cog_command_error(self, ctx: Context[Any], error: Exception) -> None:
        if isinstance(error, commands.CheckFailure):
            return
        err(f"An excpetion occured: {error}", exc_info=True)
        # await ctx.reply(f"ERROR: {type(error)} {error}")
    
    @command(name="ping")
    async def ping(self, ctx: Context[Bot]):
        ctx_mgr().set_init_context(ctx)
        
        from asyncio import sleep
        from utils.discord import send_message, BaseEmbed

        embed1 = BaseEmbed(title="Ping!")
        await send_message(content="Pong!", embed=embed1)
        await sleep(3)
        embed2 = BaseEmbed(title="Pong!")
        await send_message(content="Ping!", embed=embed2)
        await sleep(3)
        embed3 = BaseEmbed(title="Ping!")
        await send_message(content="Pong!", embed=embed3)

    
    @command(name="add_flashcard")
    async def add_flashcard(self, ctx: Context[Bot]):
        from modules.flashcards import add_flashcard
        
        ctx_mgr().set_init_context(ctx)
        await add_flashcard()
    
    @command(name="list_flashcards")
    async def list_flashcards(self, ctx: Context[Bot]):
        from modules.flashcards import list_flashcards
        
        ctx_mgr().set_init_context(ctx)
        await list_flashcards()
    
    @command(name="flashcard_flash")
    async def flashcard_flash(self, ctx: Context[Bot], card_id: str):
        from modules.flashcards import flashcard_flash
        
        ctx_mgr().set_init_context(ctx)
        await flashcard_flash(card_id)
    