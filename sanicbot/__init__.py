from sanic import Sanic, Request, response
from aiogram import Bot, Dispatcher
from aiogram.types import Update, ContentTypes, Message

from . import config, bot, view
# define sanic app & aiogram bot
app = Sanic(__name__)
app.update_config(config)

# register bot.
bot.register(app)

# register blueprint
app.blueprint(view.bp)