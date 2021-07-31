# Телеграм бот t.me/EngTraining_Bot ver 0.1
# Тренирует английские слова.

from aiogram import Bot, Dispatcher, executor, types

# дополнительно для форматирования
from aiogram.utils.markdown import text, bold, italic, code, underline, strikethrough
import MyToken         # содержит токен
import EnglishTraining # мой модуль, читает словарь из файла
import random          # для раднома

""" Импрорт токена из файла MyToken.py (лежит в раб каталоге)
Файл MyToken.py содержит две строки:
myToken = 'тут токен'
testToken = 'тут токен'
При разработке использеум test, для работы my.
в git его игнорируем, а в место пушим зашифрованный архив."""

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



@dp.message_handler(commands=['go'])
async def send_welcome2(message: types.Message):
    """ Отвечает на команды /go """
    languageSelection = random.randint(0, 1) # случайный выбор языка
    
    # приставка, подставляемая к слову id, что бы понимать направление перевода.
    languageSelectionPrefix = ""

    dictLen = len(EnglishTraining.dict_words)        # кол-во слов в словаре
    dictRandomID = (random.randrange(dictLen)) + 1   # случайное слово

    # фрмирование строки вопроса изходя из случайно выбранного направления перевода
    if languageSelection == 0:
        questionWord = (EnglishTraining.dict_words[dictRandomID])[0]
        languageSelectionPrefix = "Eng"
    if languageSelection == 1:
        questionWord = (EnglishTraining.dict_words[dictRandomID])[2]
        languageSelectionPrefix = "Rus"
    await message.answer(languageSelectionPrefix + "Id:" +  str(dictRandomID) + " " + questionWord)
    


@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message):
    """ Отвечает на команды /dict.
    Берёт из модуля EnglishTraining список слов dict_words. 
    Метод code() делает шрифт моноширным.
    Формирует строки и конкатинирует их с символом новой строки.
    Когда количетво как бы строк subStrokeSum в общей строке достигает максимума,
    выводит в телеграм, затем поновой бежит по списку слов. """
    
    sum_strok = 0      # ограничитель печатаемых ботом строк
    dict_word_bot = '' # формируемая для отправки боту строка
    subStrokeSum = 50  # кол-во подстрок в строке
    len_col = 15       # ширина колонок
    
    for i in EnglishTraining.dict_words:        
        sum_strok = sum_strok + 1 # сётчик строк

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
    await message.answer("English Training\nVersion 2021.08.01\n" + 
    "Тренируй английские слова!\n\nСписок команд (вводи с палочкой):\n" + 
    "/start - запуск бота, приветствие\n" + 
    "/help - справка\n" + 
    "/dict - показать словарь\n" +
    "/go - начать тренировку\n\n" +
    "После запуска тренировки бот выдаёт слово для перевода, чтобы ответить, " +
    "нажми на слово и выбери 'ОТВЕТИТЬ', потом пиши ответ и отправляй. " +
    "Для удобства просмотра словаря, поверни телефон горизонтально. " +
    "Если бот не даёт слово, снова введи /go.")    



@dp.message_handler()
async def send_welcome(message: types.Message):
    """ Отвечает на любые сообщения повторением. 
    Отслеживает, нет ли в сообщении ответа (кнопка ответить)"""

    responseSign = "" # признак ответа

    # await message.reply(message.text)
    if (message.reply_to_message != None):        
        print("\nЗафиксирован ответ на сообщение: " + message.reply_to_message.text)
        print(message.reply_to_message.date)
        print(message)

        # поиск признаков направления перевода
        if (message.reply_to_message.text).find("EngId:") == 0:     
            print("Направление перевода с Eng на Rus")
            endId = (message.reply_to_message.text).find(" ") # поиск пробела после "id:"

            questionBotWordId = int((message.reply_to_message.text)[6:endId]) # срез id 
            questionBotWord = (message.reply_to_message.text)[(endId + 1):] # срез загадываемого слова
            answerUser = message.text # ответ пользователя
            answerUser = answerUser.lower() # всё с маленькой буквы
            
            print(str(questionBotWordId)) # печать id загадываемого слова
            print(questionBotWord) # печать загадываемого слова
            print(answerUser)

            # проверка ответа пользователья
            if (answerUser == (EnglishTraining.dict_words[questionBotWordId])[2]):
                print("Правильно")
                await message.answer("Правильно") 
            else:
                print("Ошибка")
                await message.answer("Ошибка, правильный ответ: " + 
                (EnglishTraining.dict_words[questionBotWordId])[2]) 

            await send_welcome2(message) # поновой, как буддто пользователь ввёл "/go"

        if (message.reply_to_message.text).find("RusId:") == 0:   
            print("Направление перевода с Rus на Eng") 
            endId = (message.reply_to_message.text).find(" ") # поиск пробела после "id:"

            questionBotWordId = int((message.reply_to_message.text)[6:endId]) # срез id 
            questionBotWord = (message.reply_to_message.text)[(endId + 1):] # срез загадываемого слова
            answerUser = message.text # ответ пользователя
            answerUser = answerUser.lower() # всё с маленькой буквы
            
            print(str(questionBotWordId)) # печать id загадываемого слова
            print(questionBotWord) # печать загадываемого слова
            print(answerUser)

            # проверка ответа пользователья
            if (answerUser == (EnglishTraining.dict_words[questionBotWordId])[0]):
                print("Правильно")
                await message.answer("Правильно") 
            else:
                print("Ошибка")
                await message.answer("Ошибка, правильный ответ: " + 
                (EnglishTraining.dict_words[questionBotWordId])[0])  

            await send_welcome2(message) # поновой, как буддто пользователь ввёл "/go"
        
        
        # print(message.reply_to_message)
        # print(message.reply_to_message.text)
    else:
        # await message.answer(message.text)    
        await message.answer("Хм, непонятно... \nДля справки введи /help (с палочкой).")    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)