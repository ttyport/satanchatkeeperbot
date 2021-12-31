#!/usr/bin/env python3

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from json import load
from random import choice
from scripts.captcha_generator import generate_captcha, delete_captcha
from datetime import datetime
from os import path
from scripts.configurator import create_config

if not path.exists("../data/config.json"):
    print("Looks like you haven't configured bot yet, so..")
    create_config()

config = dict(load(open("../data/config.json")))

TOKEN = config["token"]
phrases = config["phrases"]
timeout = config["timeout"]

unapproved_users = dict()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я хранитель сотоночата, или же просто Ибрагим. Если на вас набигают - я защищу.")


@dp.message_handler(lambda message: "ибрагим" in message.text.lower())
async def ibragim(message: types.Message):
    phrase = choice(phrases)
    await message.reply(phrase)


@dp.message_handler(content_types=["new_chat_members"])
async def captcha(message: types.Message):
    print(datetime.now(), f"User @{message.from_user.username} joined the group. Captcha sent, timer is running")
    username = message.new_chat_members[0].username
    solution = generate_captcha(username)
    await bot.send_photo(message.chat.id, types.InputFile(f"../data/{username}.png"), f"Добро пожаловать, @{username}!\nЧтобы "
                                                                              f"доказать, что ты не бот - ответь на "
                                                                              f"это сообщение решением капчи.\n"
                                                                              f"У тебя одна минута.")

    unapproved_users[username] = solution
    await set_timeout(message.chat.id, username, message.from_user.id)
    await bot.delete_message(message.chat.id, message.message_id)
    delete_captcha(message.from_user.username)


@dp.message_handler(lambda message: message.from_user.username in unapproved_users.keys())
async def check_captcha(message: types.Message):
    if message.reply_to_message:
        if unapproved_users[message.from_user.username] in message.text:
            await message.reply(f"@{message.from_user.username}, проздравляю, ты прошел афганскую войну!")
            print(datetime.now(), f"User @{message.from_user.username} passed captcha.")
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await bot.delete_message(message.chat.id, message.message_id)
            unapproved_users.pop(message.from_user.username)
        else:
            await bot.delete_message(message.chat.id, message.message_id)
    else:
        await bot.delete_message(message.chat.id, message.message_id)


async def set_timeout(chat_id, username, user_id):
    await asyncio.sleep(timeout)
    if username in unapproved_users:
        await bot.ban_chat_member(chat_id, user_id)
        print(datetime.now(), f"User @{username} timed out captcha. Banned.")
        await bot.send_message(chat_id, f"Прости, @{username}, но нам придется попрощаться.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
