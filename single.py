from sanic import Sanic, Request, response
from aiogram import Bot, Dispatcher
from aiogram.types import Update, ContentTypes, Message

APP_URL = "https://21cd-61-64-6-47.jp.ngrok.io"
# deinfe parameter
BOT_TOKEN = "5509354767:AAEJbXnhEI5cwrXAUMEsGcF4le5I9I0QAac"
BOT_WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
BOT_WEBHOOK_URL = f"{APP_URL}{BOT_WEBHOOK_PATH}"

# define sanic app & aiogram bot
app = Sanic(__name__)
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

# register route to revice webhook update.
@app.post(f"/bot/<token:str>")
async def on_webhook(request: Request, token: str):
    Bot.set_current(bot)
    # check the message is from telegram
    if token != BOT_TOKEN:
        return response.empty(200)

    update = Update(**request.json)
    # dispatch update message
    await dp.process_update(update)
    # must return status code 200.
    return response.empty(200)

# listen aiogram message event.
@dp.message_handler(content_types=ContentTypes.ANY)
async def on_message(message: Message):
    await message.reply("Hello")


@app.get(f"/me")
async def me(request: Request):
    me_info = await bot.get_me()
    return response.json(me_info.to_python())

@app.main_process_start
async def startup(app: Sanic):
    # send request to telegram for change webhook.
    await bot.set_webhook(BOT_WEBHOOK_URL)

@app.before_server_stop
async def dispose(app: Sanic):
    await bot.delete_webhook()

if __name__ == '__main__':
    app.run()