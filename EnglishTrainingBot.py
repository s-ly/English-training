# Телеграм бот t.me/EngTraining_Bot ver 0.1
# Тренирует английские слова.

from aiogram import Bot, Dispatcher, executor, types

# дополнительно для форматирования
from aiogram.utils.markdown import text, bold, italic, code, underline, strikethrough
import MyToken # содержит токен
import EnglishTraining
import random   # для раднома

# Импрорт токена из файла MyToken.py (лежит в раб каталоге)
# Файл MyToken.py содержит две строки:
# myToken = 'тут токен'
# testToken = 'тут токен'
# При разработке использеум test, для работы my.
# в git его игнорируем, а в место пушим зашифрованный архив.

API_TOKEN = MyToken.myToken # рабочий бот
# API_TOKEN = MyToken.testToken # тестовый бот

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """ Отвечает на команды /start """
    # await message.reply("English Training\n" + 
    await message.answer("English Training\n" + 
    "Тренируй английские слова!\nДля справки введи /help (с палочкой).")



@dp.message_handler(commands=['test'])
async def send_welcome(message: types.Message):
    """ Отвечает на команды /test """
    await message.answer("test")
    dictLen = len(EnglishTraining.dict_words)        # кол-во слов в словаре
    dictRandomID = (random.randrange(dictLen)) + 1   # случайное слово
    await message.answer("id:" + str(dictRandomID))
    await message.answer(str(EnglishTraining.dict_words[dictRandomID]))
    



@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message):
    """ Отвечает на команды /dict.
    Берёт из модуля EnglishTraining список слов dict_words. 
    Формирует строки и конкатинирует их с символом новой строки.
    Когда количетво как бы строк subStrokeSum в общей строке достигает максимума,
    выводит в телеграм, затем поновой бежит по списку слов. """
    
    sum_strok = 0      # ограничитель печатаемых ботом строк
    dict_word_bot = '' # формируемая для отправки боту строка
    subStrokeSum = 50  # кол-во подстрок в строке
    len_col = 15       # ширина колонок
    
    for i in EnglishTraining.dict_words:
        # сётчик строк
        sum_strok = sum_strok + 1

        # вычисляем недостающее кол-во пробелов для ширины колонок
        dobavka_col_0 = len_col - len(i[0])
        dobavka_col_1 = len_col - len(i[1]) 
        dobavka_col_2 = len_col - len(i[2])

        # формируем и добавляем строку со всеми колонками
        dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
        "[" + i[1] + "]" + (" " * dobavka_col_1) +
        i[2] + (" " * dobavka_col_2) + i[3] + "\n")
        
        # ограничение кол-ва строк, передаваемых ботом за раз
        if (sum_strok == subStrokeSum):
            await message.answer(code(dict_word_bot), parse_mode=types.ParseMode.MARKDOWN_V2)    
            sum_strok = 0      # обнуляем
            dict_word_bot = '' # обнуляем 
            continue           # обрыв цикла и поновой



@dp.message_handler(commands=['help'])
async def send_test(message: types.Message):
    """ Отвечает на команды /help. """
    await message.answer("English Training\nVersion 0.1 2021.07.25\n" + 
    "Тренируй английские слова!\n\nСписок команд (вводи с палочкой):\n" + 
    "/start - запуск, приветствие\n" + 
    "/help - справка\n" + 
    "/dict - показать словарь\n" +
    "/test - тестовая функция\n\n" +
    "Для удобства просмотра словаря, поверни телефон горизонтально.\n")    



@dp.message_handler()
async def send_welcome(message: types.Message):
    """ Отвечает на любые сообщения повторением. """
    # await message.reply(message.text)
    if (message.reply_to_message != None):
        await message.answer("Зафиксирован ответ на сообщение: "
        + message.reply_to_message.text)
        
        print("\nЗафиксирован ответ")
        print(message.reply_to_message.date)
        print(message)
        
        # print(message.reply_to_message)
        # print(message.reply_to_message.text)
    else:
        # await message.answer(message.text)    
        await message.answer("Хм, непонятно... \nДля справки введи /help (с палочкой).")    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)