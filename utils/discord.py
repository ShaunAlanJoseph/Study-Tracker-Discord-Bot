from discord import Embed, ui, File, NotFound
from typing import Optional, List, Any, Dict
from utils.context_manager import ctx_mgr


async def get_channel(channel_id: int):
    bot = ctx_mgr().get_context_bot()
    try:
        channel_api = await bot.fetch_channel(channel_id)
        return channel_api
    except NotFound:
        raise ValueError(f"Invalid channel_id: `{channel_id}` doesn't exist.")


async def get_user(user_id: int):
    bot = ctx_mgr().get_context_bot()
    try:
        user_api = await bot.fetch_user(user_id)
        return user_api
    except NotFound:
        raise ValueError(f"Invalid user_id: `{user_id}` doesn't exist.")


async def send_message(
    *,
    content: Optional[str] = None,
    embed: Optional[Embed] = None,
    view: Optional[ui.View] = None,
    file: Optional[File] = None,
    files: Optional[List[File]] = None,
    mention_author: bool = False,
):
    message = ctx_mgr().get_active_msg()
    send_new_message = ctx_mgr().get_send_new_msg()

    files = files or []
    if file is not None:
        files.append(file)
    
    kwargs: Dict[str, Any] = {}
    for kwarg in ["embed", "view", "files", "mention_author"]:
        if locals()[kwarg] is not None:
            kwargs[kwarg] = locals()[kwarg]

    if message is None or send_new_message:
        ctx = ctx_mgr().get_init_context()
        message = await ctx.reply(content=content, **kwargs)
    
    else:
        del kwargs["files"]
        kwargs["attachments"] = files
        message = await message.edit(content=content)
    
    ctx_mgr().set_active_msg(message)
