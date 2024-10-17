from discord.ext import commands
from discord.ext.commands import command, Bot, Cog, Context  # type: ignore
from discord import Embed
from typing import Any
from logging import info, error as err
from database.database import Database
from utils.context_manager import ctx_mgr

current_task_id=None
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
    
    @command(name="add_task")
    async def add_task(self, ctx: Context[Bot],*,name: str):
        from modules.tasks import add_task
        ctx_mgr().set_init_context(ctx)
        await add_task(name=name)

        
    @command(name="set_task")
    async def set_current_task(self, ctx: Context[Bot],*,name: str):
        query=("SELECT task_id FROM Tasks WHERE name=%s")
        id=Database.fetch_one(query,name)
        global current_task_id
        current_task_id=id
        await ctx.send(f"Current task set to name: {name}, id: {current_task_id}")

    @command(name="set_task_by_id")
    async def settask(self, ctx: Context[Bot], *, id):
        query=("SELECT name FROM Tasks WHERE task_id=%s")
        name=Database.fetch_one(query,id)
        global current_task_id
        current_task_id = id
        await ctx.send(f"Current task set to name: {name}, id: {current_task_id}")
     

    @command(name="add_description")
    async def add_description(self, ctx: Context[Bot],*, description: str):
        from modules.tasks import add_description
        id=current_task_id
        if(id==None):
            await ctx.send("Please set the  task.")
            await ctx.send("Use set_task <task_name> or set_task_by_id <task_id>")
        ctx_mgr().set_init_context(ctx)
        await add_description(id, description)

    @command(name="list_tasks")
    async def list_tasks(self, ctx: Context[Bot]):
        from modules.tasks import list_tasks
        
        ctx_mgr().set_init_context(ctx)
        await list_tasks()
    
    @command(name="remove_task")
    async def remove_task(self, ctx: Context[Bot],*,name: str):
        from modules.tasks import remove_task
        query=("SELECT task_id FROM Tasks WHERE name=%s")
        id=Database.fetch_one(query,name)
        ctx_mgr().set_init_context(ctx)
        await remove_task(id)

    @command(name="delete_task")
    async def delete_task(self, ctx: Context[Bot],*,id):
        from modules.tasks import remove_task

        ctx_mgr().set_init_context(ctx)
        await remove_task(id)

    @command(name="mark_as_done")
    async def mark_as_done(self, ctx: Context[Bot],*,name: str):
        from modules.tasks import mark_as_done
        query=("SELECT task_id FROM Tasks WHERE name=%s")
        id=Database.fetch_one(query,name)
        ctx_mgr().set_init_context(ctx)
        await mark_as_done(id)

    @command(name="mark_as_started")
    async def mark_as_started(self, ctx: Context[Bot],*,name: str):
        from modules.tasks import mark_as_started
        query=("SELECT task_id FROM Tasks WHERE name=%s")
        id=Database.fetch_one(query,name)
        ctx_mgr().set_init_context(ctx)
        await mark_as_started(id)

    @command(name="mark_as_started_by_id")
    async def mark_as_started_by_id(self, ctx: Context[Bot],*,id: str):
        from modules.tasks import mark_as_started
        
        ctx_mgr().set_init_context(ctx)
        await mark_as_started(id)
    
    @command(name="mark_as_done_by_id")
    async def mark_as_done_by_id(self, ctx: Context[Bot],*,id: str):
        from modules.tasks import mark_as_done
        
        ctx_mgr().set_init_context(ctx)
        await mark_as_done(id)

    @command(name="set_due_date")
    async def set_due_date(self, ctx: Context[Bot],*,due_date: str):
        from modules.tasks import set_due_date
        id=current_task_id
        if(id==None):
            await ctx.send("Please set the  task.")
            await ctx.send("Use set_task <task_name> or set_task_by_id <task_id>")
        ctx_mgr().set_init_context(ctx)
        await set_due_date(id, due_date)


    @command(name="help")
    async def help_command(self, ctx: Context[Bot]):
        embed = Embed(title="Study Tracker Commands", description="List of available commands and their usage", color=0x00ff00)

        commands_info = {
            
            "ping": "Responds with 'Pong!' and alternates messages.",
            "add_flashcard": "Adds a new flashcard.",
            "list_flashcards": "Lists all flashcards.",
            "flashcard_flash": "Flashes a specific flashcard by ID.",
            "add_task": "Adds a new task with a specified name.",
            "set_task": "Sets the current task by name.",
            "set_task_by_id": "Sets the current task by ID.",
            "add_description": "Adds a description to the current task.",
            "list_tasks": "Lists all tasks.",
            "remove_task": "Removes a task by name.",
            "delete_task": "Deletes a task by ID.",
            "mark_as_done": "Marks a task as done by name.",
            "mark_as_started": "Marks a task as started by name.",
            "mark_as_started_by_id": "Marks a task as started by ID.",
            "mark_as_done_by_id": "Marks a task as done by ID.",
            "set_due_date": "Sets a due date for the current task.",
            "query": "Queries the Gemini API with your question and returns a response.",
            "pm": "Sends a private message to you asking how the bot can help and you can talk to it.",
            "gemini enable": "Enables Gemini to respond to every message in the server.",
            "gemini disable": "Disables Gemini from responding to every message in the server."
        }

        for command_name, description in commands_info.items():
            embed.add_field(name=f"${command_name}", value=description, inline=False)

        await ctx.send(embed=embed)
 
