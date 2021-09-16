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

# API_TOKEN = MyToken.myToken # рабочий бот
API_TOKEN = MyToken.testToken # тестовый бот

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
    """ Отвечает на команды /go. Создаёт строку вопроса. 
    questionRepeat - параметр для повторения вопроса."""
    dictRandomID = None # без этого появлялась ошибка выхода из диапазона (иногда)
    questionWord = None # обнуление старого вопроса (на всякий)
    randomDictStroke = None
    languageSelection = random.randint(0, 1) # случайный выбор языка
    # print('-languageSelection-- ' + str(languageSelection))
    
    # приставка, подставляемая к слову id, что бы понимать направление перевода.
    languageSelectionPrefix = ""

    dictLen = len(EnglishTraining.dict_words)        # кол-во слов в словаре
    # print('-dictLen-- ' + str(dictLen))
    dictRandomID = random.randint(0, dictLen - 1)    # случайное слово
    # print('-dictRandomID-- ' + str(dictRandomID))    
    randomDictStroke = EnglishTraining.dict_words[dictRandomID] # случайная строка

    # фрмирование строки вопроса изходя из случайно выбранного направления перевода
    # если с русского то учитывается кол-во синонимов
    if languageSelection == 0:
        languageSelectionPrefix = "Eng"
        questionWord = str(randomDictStroke[0])
    elif languageSelection == 1:
        languageSelectionPrefix = "Rus"
        len_i = 0 # получаемое кол-во синонимов (обнуление)    
        # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
        len_i = await SumSynonym(randomDictStroke) 
        # print('-----------' + str(len_i))
        if len_i == 1:
            questionWord = str(randomDictStroke[2])
        elif len_i == 2:
            questionWord = str(randomDictStroke[2]) + ', ' + str(randomDictStroke[3])
        elif len_i == 3:
            questionWord = (str(randomDictStroke[2]) + ', ' + str(randomDictStroke[3]) 
            + ', ' + str(randomDictStroke[4]))
        elif len_i == 4:
            questionWord = (str(randomDictStroke[2]) + ', ' + str(randomDictStroke[3]) 
            + ', ' + str(randomDictStroke[4]) + ', ' + str(randomDictStroke[5]))
        elif len_i == 5:
            questionWord = (str(randomDictStroke[2]) + ', ' + str(randomDictStroke[3]) 
            + ', ' + str(randomDictStroke[4]) + ', ' + str(randomDictStroke[5])
            + ', ' + str(randomDictStroke[6]))
    await message.answer(languageSelectionPrefix + "Id:" +  str(dictRandomID) + " " + str(questionWord))
    


@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message):
    """ Отвечает на команды /dict.
    Берёт из модуля EnglishTraining список слов dict_words. 
    Метод code() делает шрифт моноширным.
    Формирует строки и конкатинирует их с символом новой строки.
    Когда количетво как бы строк subStrokeSum в общей строке достигает максимума,
    выводит в телеграм, затем поновой бежит по списку слов. """
    
    sum_all_strok = 0  # общее кол-во слов
    sum_strok = 0      # ограничитель печатаемых ботом строк
    dict_word_bot = '' # формируемая для отправки боту строка
    sum_all_words = '' # строка для печати кол-ва всех слов в словаре
    subStrokeSum = 50  # кол-во подстрок в строке
    # subStrokeSum = 6  # кол-во подстрок в строке
    len_col = 15       # ширина колонок
    
    for i in EnglishTraining.dict_words:        
        sum_strok = sum_strok + 1         # сётчик строк
        sum_all_strok = sum_all_strok + 1 # счётчик всех слов в словаре

        # вычисляем недостающее кол-во пробелов для ширины колонок
        dobavka_col_0 = len_col - len(i[0])

        len_i = 0 # получаемое колво синонимов
        len_i = await SumSynonym(i) # Подсчёт кол-ва синонимов в строке словаря (мой метод)

        # формируем и добавляем строку со всеми колонками (без транскрипции)
        # в зависимости от кол-ва синонимов.
        if len_i == 1:      
            dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
            i[2] + "\n")
        if len_i == 2:   
            dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
            i[2] + ', ' + i[3] + "\n")
        if len_i == 3:    
            dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
            i[2] + ', ' + i[3] + ', ' + i[4] + "\n")
        if len_i == 4:     
            dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
            i[2] + ', ' + i[3] + ', ' + i[4] + ', ' + i[5] + "\n")
        if len_i == 5:      
            dict_word_bot = dict_word_bot + (i[0] + (" " * dobavka_col_0) +
            i[2] + ', ' + i[3] + ', ' + i[4] + ', ' + i[5] + ', ' + i[6] + "\n")
        
        
        # ограничение кол-ва строк, передаваемых ботом за раз
        if (sum_strok == subStrokeSum):
            await message.answer(code(dict_word_bot), parse_mode=types.ParseMode.MARKDOWN_V2)    
            sum_strok = 0      # обнуляем
            dict_word_bot = '' # обнуляем 
            continue           # обрыв цикла и поновой

    # формирование строки с общим кол-вом слов в словаре
    sum_all_words = sum_all_words + 'Всего слов в словаре: ' + str(sum_all_strok)
    await message.answer(code(sum_all_words), parse_mode=types.ParseMode.MARKDOWN_V2) 
    sum_all_strok = 0 # обнуляем счётчик всех слов



@dp.message_handler(commands=['help'])
async def send_test(message: types.Message):
    """ Отвечает на команды /help. """
    await message.answer("Тренируй английские слова!\n\nСписок команд (вводи с палочкой):\n" + 
    "/start - запуск бота, приветствие\n" + 
    "/help - справка\n" + 
    "/dict - показать словарь\n" +
    "/go - начать тренировку\n\n" +
    "После запуска тренировки бот выдаёт слово для перевода, чтобы ответить, " +
    "нажми на слово и выбери 'ОТВЕТИТЬ', потом пиши ответ и отправляй. " +
    "Для удобства просмотра словаря, поверни телефон горизонтально. " +
    "Если бот не даёт слово, снова введи /go.\n\n"
    "Подробная инструкция:\n" + 
    "Для начала тренировки введите /go (с палочной). Бот напишет сообщение для перевода." +
    " Случайным образом будет предложено перевести или с русского на английский или наоборот." +
    " Например, бот напишет 'EngId:176 mind'. Начало строки 'EngId:176' не имеет значения," +
    " это техническая часть, далее после пробела следует слово для перевода 'mind'." +
    " У этого слова в русском переводе есть несколько вариантов: 'разум', 'ум', 'мнение'." +
    " Вам необходимо написать только одно любое подходящее слово на русском." +
    " Для этого не получится просто написать ответ. Необходимо воспользоваться" +
    " функцией Телеграм 'Ответить'. Ткните в сообщение бота, появится контекстное" +
    " выпадающее меню, в нём выберете 'Ответить' и теперь вводите свой ответ.\n\n" +
    "English Training Bot version 2021.09.16\n" + 
    "Разработка @SergeyLysov")    



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
        # print("Направление перевода с Eng на Rus")
    elif (message.reply_to_message.text).find("RusId:") == 0:
        translatDir = 0
        # print("Направление перевода с Rus на Eng")
    else:
        await message.answer("Хм, непонятный ответ... \nДля справки введи /help (с палочкой).")
        print("Хм, непонятный ответ...")
        return None

    endId = (message.reply_to_message.text).find(" ")                 # поиск пробела после "id:"
    questionBotWordId = int((message.reply_to_message.text)[6:endId]) # срез id 
    questionBotWord = (message.reply_to_message.text)[(endId + 1):]   # срез загадываемого слова
    answerUser = message.text       # ответ пользователя
    answerUser = answerUser.lower() # всё с маленькой буквы

    # print("id загадываемого слова: " + str(questionBotWordId)) # печать id загадываемого слова
    # print("Загадываемое слово: "+ questionBotWord)             # печать загадываемого слова    

    currentDictStroke = EnglishTraining.dict_words[questionBotWordId] # текущая строка словаря (по id)
    len_i = 0 # получаемое кол-во синонимов (обнуление)
    
    # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
    len_i = await SumSynonym(currentDictStroke) 
    
    # формируем строку правильного ответа в зависимости от кол-ва синонимов (len_i)
    correctAnswer = '' # ответ бота
    if len_i == 1:
        correctAnswer = (str(currentDictStroke[0]) + " [" + str(currentDictStroke[1]) + "] " +
        str(currentDictStroke[2]))

    elif len_i == 2:
        correctAnswer = (str(currentDictStroke[0]) + " [" + str(currentDictStroke[1]) + "] " +
        str(currentDictStroke[2]) + ', ' + str(currentDictStroke[3]))

    elif len_i == 3:
        correctAnswer = (str(currentDictStroke[0]) + " [" + str(currentDictStroke[1]) + "] " +
        str(currentDictStroke[2]) + ', ' + str(currentDictStroke[3]) + ', ' + 
        str(currentDictStroke[4]))

    elif len_i == 4:
        correctAnswer = (str(currentDictStroke[0]) + " [" + str(currentDictStroke[1]) + "] " +
        str(currentDictStroke[2]) + ', ' + str(currentDictStroke[3]) + ', ' + 
        str(currentDictStroke[4]) + ', ' + str(currentDictStroke[5]))

    elif len_i == 5:
        correctAnswer = (str(currentDictStroke[0]) + " [" + str(currentDictStroke[1]) + "] " +
        str(currentDictStroke[2]) + ', ' + str(currentDictStroke[3]) + ', ' + 
        str(currentDictStroke[4]) + ', ' + str(currentDictStroke[5]) + ', ' +
        str(currentDictStroke[6]))

    # проверка ответа пользователья если с RUS на ENG
    if translatDir == 0:
        if (answerUser == (currentDictStroke[0])):
            print("Правильно")
            await message.answer("Правильно\n" + correctAnswer) 
        else:
            print("Ошибка")
            await message.answer("Ошибка\n" + correctAnswer)             
            await message.answer("Попробуй ещё")
            await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
            return # выход из метода

    # проверка ответа пользователья если с ENG на RUS в зависимости от кол-ва синонимов
    if translatDir == 2:
        if len_i == 1:
            if (answerUser == (currentDictStroke[2])):
                print("Правильно")
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                print("Ошибка")
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
                return # выход из метода

        elif len_i == 2:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3])):
                print("Правильно")
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                print("Ошибка")
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
                return # выход из метода

        elif len_i == 3:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4])):
                print("Правильно")
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                print("Ошибка")
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
                return # выход из метода
  
        elif len_i == 4:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])):
                print("Правильно")
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                print("Ошибка")
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
                return # выход из метода
        
        elif len_i == 5:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])
            or answerUser == (currentDictStroke[6])):
                print("Правильно")
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                print("Ошибка")
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(message.reply_to_message.text) # повтор предыдущего сообщения
                return # выход из метода

    await send_welcome2(message) # поновой, как буддто пользователь ввёл "/go"



async def SumSynonym(dict_string):
    """Подсчёт кол-ва синонимов в строке словаря."""
    # принимает строку словаря (список), возвращает число
    # подсчитываем кол-во синонимов в каждой строке
    # no_none_sub_i - кол-во непустых ячеек в строке
    # len_i - получаемое колво синонимов
    # Цикл бежит по строке и считает непустые ячейки, потом вычитаем 2, так как первые две ячейки
    # это английское слово и транскрипция. 
    no_none_sub_i = 0
    len_i = 0
    for sub_i in dict_string:
        if(sub_i != ''):
            no_none_sub_i = no_none_sub_i + 1
    len_i = no_none_sub_i - 2
    return len_i
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)