from sanic import Blueprint, Request, response
from aiogram import Bot
from aiogram.types import Update

from .bot import get_bot, get_dp, get_token

bp = Blueprint("bot")

# register route to revice webhook update.
@bp.post(f"/bot/<token:str>")
async def on_webhook(request: Request, token: str):

    # get bot from app.ctx & get token from app.config
    bot = get_bot()
    dp = get_dp()
    _bot_token = get_token()

    # check the message is from telegram
    if token != _bot_token:
        return response.empty(200)

    # set default instance.
    Bot.set_current(bot)
    update = Update(**request.json)
    
    # dispatch update message
    await dp.process_update(update)
    
    # must return status code 200.
    return response.empty(200)