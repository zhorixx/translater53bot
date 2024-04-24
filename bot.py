from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

bot = AsyncTeleBot("7068028647:AAE9btQTRixAfCYIMB756mfvIVyQfeXCy", parse_mode=None)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, '------\n'
                       + 'Здравствуй, '
                       + message.from_user.first_name
                       + ' \nПереведу с русского на английский \nИ с других языков на русский '
                       + '\n------')


@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message, '------\n'
                       + 'Просто вводи текст и нажимай отправить\n'
                       + 'Я сам определю какой это язык\n'
                       + 'Если не перевел, попробуй еще раз\n'
                       + 'Перевод гугл'
                       + '\n------')


@bot.message_handler(commands=['developer'])
async def send_welcome(message):
    await bot.reply_to(message, '------\n'
                       + '@zhorixxx'
                       + '\n------')


@bot.message_handler()
async def user_text(message):
    translator = Translator()

    lang = translator.detect(message.text)
    lang = lang.lang

    if lang == 'ru':
        send = translator.translate(message.text)
        await bot.reply_to(message, send.text)


    else:
        send = translator.translate(message.text, dest='ru')
        await bot.reply_to(message, send.text)


@bot.message_handler(content_types=['photo'])
async def handle_image(message):
    translator = Translator()

    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    caption = message.caption

    lang = translator.detect(caption)
    lang = lang.lang

    if lang == 'ru':
        send = translator.translate(caption)


    else:
        send = translator.translate(caption, dest='ru')
    await bot.send_photo(chat_id, photo, caption=send.text)


@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    if not text:
        return

    lang = translator.detect(text)
    lang = lang.lang

    if lang == 'ru':
        send = translator.translate(text)
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))


    else:
        send = translator.translate(text, dest='ru')
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    await bot.answer_inline_query(query.id, results)


asyncio.run(bot.infinity_polling())
