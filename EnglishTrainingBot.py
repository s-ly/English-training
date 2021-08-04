# Телеграм бот t.me/EngTraining_Bot
# Тренирует английские слова.

from aiogram import Bot, Dispatcher, executor, types

# дополнительно для форматирования
from aiogram.utils.markdown import text, bold, italic, code, underline, strikethrough
import MyToken         # содержит токен
import EnglishTraining # мой модуль, читает словарь из файла
import random          # для раднома

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



@dp.message_handler(commands=['go'])
async def send_welcome2(message: types.Message):
    """ Отвечает на команды /go. Создаёт строку вопроса. """
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
    await message.answer("English Training\nVersion 2021.08.04\n" + 
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
    """ Отвечает на любые сообщения. Проверяет, нет ли в сообщении ответа (кнопка ответить).
    Если ответ есть, вызываем CheckingResponse(message) с передачей методу самого сообщения.
    Иначе предлагаем пользователю посмотреть справку."""

    if (message.reply_to_message != None):        
        print("\nЗафиксирован ответ на сообщение.")
        print("дата ответа: " + str(message.reply_to_message.date))
        print("текст ответа: " + str(message.reply_to_message.text))
        print("User: " + (message.reply_to_message.chat.username))
        await CheckingResponse(message) # разбираем ответ пользователя.
    else:
        await message.answer("Хм, непонятно... \nДля справки введи /help (с палочкой).")    



async def CheckingResponse(message):
    """Вызывается при наличии ответа пользователя. Разбирает и проверяет ответ. 
    Обнаруживает в ответе кусок "EngId:" или "RusId:", и так определяет направление перевода,
    иначе прирывает метод. Сообщение распарсивается на части, срезами выделяется id слова,
    загаданное слово и сам ответ пользователя. Потом проверяется ответ пользователя
    на правильность. В результате проверки формируется ответ бота на ответ пользователя.
    В конце снова вызывает метод send_welcome2(message), дающий пользователю
    новое слово-задание."""

    translatDir = None # направление перевода
    
    # поиск признаков направления перевода
    if (message.reply_to_message.text).find("EngId:") == 0:
        translatDir = 2
        print("Направление перевода с Eng на Rus")
    elif (message.reply_to_message.text).find("RusId:") == 0:
        translatDir = 0
        print("Направление перевода с Rus на Eng")
    else:
        await message.answer("Хм, непонятный ответ... \nДля справки введи /help (с палочкой).")
        print("Хм, непонятный ответ...")
        return None

    endId = (message.reply_to_message.text).find(" ")                 # поиск пробела после "id:"
    questionBotWordId = int((message.reply_to_message.text)[6:endId]) # срез id 
    questionBotWord = (message.reply_to_message.text)[(endId + 1):]   # срез загадываемого слова
    answerUser = message.text       # ответ пользователя
    answerUser = answerUser.lower() # всё с маленькой буквы

    print("id загадываемого слова: " + str(questionBotWordId)) # печать id загадываемого слова
    print("Загадываемое слово: "+ questionBotWord)             # печать загадываемого слова    

    # формируем строку правильного ответа
    correctAnswer = ( 
    str((EnglishTraining.dict_words[questionBotWordId])[0]) + 
    " [" + str((EnglishTraining.dict_words[questionBotWordId])[1]) + "] " +
    str((EnglishTraining.dict_words[questionBotWordId])[2]))

    # проверка ответа пользователья
    if (answerUser == (EnglishTraining.dict_words[questionBotWordId])[translatDir]):
        print("Правильно")
        await message.answer("Правильно\n" + correctAnswer) 
    else:
        print("Ошибка")
        await message.answer("Ошибка\n" + correctAnswer)  

    await send_welcome2(message) # поновой, как буддто пользователь ввёл "/go"
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)