# Телеграм бот t.me/EngTraining_Bot ver 0.1
# Тренирует английские слова.

from aiogram import Bot, Dispatcher, executor, types
import MyToken # содержит токен

# Импрорт токена из файла MyToken.py (лежит в раб каталоге)
# Файл MyToken.py содержит одну строку: myToken = 'тут токен'
# в git его игнорируем, а в место пушим зашифрованный архив.
API_TOKEN = MyToken.myToken

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ Отвечает на команды /start и /help """
    await message.reply("Hi!")



@dp.message_handler(commands=['test'])
async def send_test(message: types.Message):
    """ Отвечает на команды /test """
    await message.reply("test ok")



@dp.message_handler()
async def send_welcome(message: types.Message):
    """ Отвечает на любые сообщения повторением. """
    # await message.reply(message.text)
    if (message.reply_to_message != None):
        await message.answer("Зафиксирован ответ на сообщение бота: "
        + message.reply_to_message.text)
        # print(message.reply_to_message)
        # print(message.reply_to_message.date)
        print(message.reply_to_message.text)
    else:
        # await message.answer(message.text)    
        await message.answer("Включи мозги!")    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)