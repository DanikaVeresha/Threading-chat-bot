import random
import asyncio
import logging
import config
import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from pymongo.mongo_client import MongoClient


router = Router()


uri = "mongodb+srv://desh2808:desh2808@clusterserverbot.1urry1n.mongodb.net/" \
      "?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.db_binance
collections_users = db.document_users
collections_lectures = db.document_lectures

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"Здравствуйте, {msg.from_user.username} Я ваш чат-бот, я помогу Вам получить "
                     f"доступ к просмотру лекций. Для начала Вам необходимо пройти "
                     f"быструю регистрацию, введите в поле свой email, в дальнейшем "
                     f"Вам будет предоставлен  по нему уникальный доступ")


@router.message()
async def message_handler(msg: Message):
    ID = random.randint(1, 1000000)
    if msg.text == '/add':
        date = datetime.datetime.now()
        access_data = [
            {'Date': date,
             'ID_for_user': ID,
             'link': input('Введите ссылку на свой гуглдиск: ')}
        ]
        collections_lectures.insert_many(access_data)
        await msg.answer(f"Ссылка для получения доступа по идентификационному номеру {ID}")
    else:
        user_info = collections_users.find_one({'ID': msg.from_user.id})
        access_link = collections_lectures.find({})
        for document in access_link:
            if user_info is None:
                user_ID = msg.from_user.id
                user_name = msg.from_user.username
                user_email = msg.text
                data = [
                    {'ID': user_ID,
                     'name': user_name,
                     'email': user_email,
                     'access': document,
                     'date_enter': datetime.datetime.now()}
                ]
                collections_users.insert_many(data)
                await msg.answer(f"Поздравляем {msg.from_user.username}! "
                                 f"Ваш доступ к просмотру лекций: {document['link']} — перейдите по "
                                 f"этой ссылке. Желаем Вам успехов в изучении материала!")
            else:
                await msg.answer(f"Извините, {msg.from_user.username}, Вы уже зарегистрированы и Вам уже "
                                 f"предоставлен доступ к лекциям, пожалуйста, посмотрите свою стенограмму "
                                 f"в чате выше и перейдите по предоставленным ранее ссылкам. "
                                 f"Благодарим за обращение!")


async def main():
    bot = Bot(token=conf.code_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

