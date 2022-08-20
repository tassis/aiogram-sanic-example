from sanic import Sanic
from aiogram import Bot, Dispatcher
from aiogram.types import ContentTypes, Message

SERVICE_CODE = "bot"
DP_CODE = f"{SERVICE_CODE}_dp" 

def get_bot() -> Bot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def get_dp() -> Dispatcher:
    app = Sanic.get_app()
    return getattr(app.ctx, DP_CODE)

def register(app: Sanic):
    # get bot_token from app.config
    token = app.config["BOT_TOKEN"]
    webhook_url = app.config["BOT_WEBHOOK_URL"]

    # define instance
    bot = Bot(token)
    dp = Dispatcher(bot)

    # listen aiogram message event.
    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        await message.reply("Hello")

    
    # set webhook url on startup
    @app.main_process_start
    async def startup(app: Sanic):
        # send request to telegram for change webhook.
        await bot.set_webhook(webhook_url)

    # delete webhook before stop.
    @app.before_server_stop
    async def dispose(app: Sanic):
        await bot.delete_webhook()


    # attach bot & dispatcher to app.ctx
    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, DP_CODE, dp)