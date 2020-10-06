from flask import Flask, request
import requests
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
import re
import os
import discord
import asyncio
import redis
global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
client = discord.Client()
# start the flask app
app = Flask(__name__)

client.login(TOKEN)


# @client.event
# async def foo():  # change this to the event in which you wish to call it from
#     print("INSIDE :::")
#     print("GUILDS : {}".format(client.guilds))
#     for guild in client.guilds:
#         for channel in guild.channels:
#             # change messagedata to whatever it is you want to send.
#             print("CHANNEL : ".format(channel))


redis_host = "localhost"
redis_password = ""
redis_port = 6379


@app.route('/posts', methods=['POST'])
def requested():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port,
                              password=redis_password, decode_responses=True)
    except Exception as e:
        print(e)
    print("INSIDE")
    data = request.json
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(foo())
    # for guild in client.guilds:
    #     for channel in guild.channels:
    #         print("CHANEL : ", channel)
    print("COMING data : ", data)
    bot.sendMessage(511188118, text=data)
    bot.sendMessage(chat_id="@pyyboot", text=data)
    return 'ok'


@ app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it  to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print("UPDATING : ", update)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message : ", text)

    if text == "/start":
        bot_welcome = "WELCOME TO THE BOT "

        # send the welcoming message to the
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(
                text.strip())
            print("TEXT : ", text)
            # url = requests.get("https://httpbin.org/get").json()
            # reply with a photo to the name the user sent
            # not that you can send photos by url and telegram will fetch it for you
            bot.sendMessage(chat_id=chat_id, text=text,
                            reply_to_message_id=msg_id)
            bot.sendPhoto(chat_id=chat_id, photo=url,
                          reply_to_message_id=msg_id)
        except Exception as e:
            print("Exception : ", e)
            bot.sendMessage(chat_id=chat_id, text="ERROR OCCURING : {}".format(
                e), reply_to_message_id=msg_id)
    return 'ok'


@ app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object ot link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup falied"


@ app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread

    app.run(threaded=True)
