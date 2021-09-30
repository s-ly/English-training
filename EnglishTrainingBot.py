# Телеграм бот t.me/EngTraining_Bot
# Тренирует английские слова.

from os import stat
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext # хранение контекста
from aiogram.contrib.fsm_storage.memory import MemoryStorage # место для хранения контекста в ОЗУ

# дополнительно для форматирования
from aiogram.utils.markdown import text, bold, italic, code, underline, strikethrough
import MyToken         # содержит токен
import dict            # мой модуль, читает словарь из файла
import Texts           # мой модуль, хранит текст
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
storage = MemoryStorage() # место хранения контекста в ОЗУ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    """ Отвечает на команды /start """
    # Второй параметр FSMContext хранит контекст 

    # Инициализация контекста (данных пользователя)
    await InItStateUser(message, state)

    await message.answer("English Training\n" + 
    "Тренируй английские слова!\nДля начала тренировки введи /go, справка /help (с палочкой).")

@dp.message_handler(commands=['status'])
async def userStatus(message: types.Message, state: FSMContext):
    """ Выводит содеожание контекста пользователя"""
    allUserData = await state.get_data()
    
    # если статус 'userName' существует
    if ('userName' in allUserData):
        print(allUserData)
        await message.answer(allUserData)
    else:
        print('Данных нет')
        await message.answer('Данных нет')
        await send_start(message, state) # поновой, как буддто пользователь ввёл "/start"



@dp.message_handler(commands=['go'])
async def send_welcome2(message: types.Message, state: FSMContext):
    """ Отвечает на команды /go. Создаёт строку вопроса. 
    questionRepeat - параметр для повторения вопроса."""

    # Инициализация контекста (данных пользователя)
    await InItStateUser(message, state)

    dictRandomID = None # без этого появлялась ошибка выхода из диапазона (иногда)
    questionWord = None # обнуление старого вопроса (на всякий)
    randomDictStroke = None
    languageSelection = random.randint(0, 1) # случайный выбор языка
    
    # приставка, подставляемая к слову id, что бы понимать направление перевода.
    languageSelectionPrefix = ""

    dictLen = len(dict.dict_words)                   # кол-во слов в словаре
    dictRandomID = random.randint(0, dictLen - 1)    # случайное слово
    await state.update_data(idWord=dictRandomID)     # случайное слово в статус пользователя
    randomDictStroke = dict.dict_words[dictRandomID] # случайная строка

    # фрмирование строки вопроса изходя из случайно выбранного направления перевода
    # если с русского то учитывается кол-во синонимов
    if languageSelection == 0:
        languageSelectionPrefix = "Eng"

        await state.update_data(translatDir='Eng') # направление перевода в статус пользователя

        questionWord = str(randomDictStroke[0])
    elif languageSelection == 1:
        languageSelectionPrefix = "Rus"

        await state.update_data(translatDir='Rus') # направление перевода в статус пользователя

        len_i = 0 # получаемое кол-во синонимов (обнуление)    
        # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
        len_i = await SumSynonym(randomDictStroke) 
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
    # await message.answer(languageSelectionPrefix + "Id:" +  str(dictRandomID) + " " + str(questionWord))
    await message.answer(str(questionWord))
    await state.update_data(questionWord=str(questionWord)) # статус пользователя: вопрос
    await state.update_data(userStatus='userHasQuestion') # статус пользователя: пользователю задан вопрос
    


@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /dict."""
    # Берёт из модуля dict список слов dict_words. 
    # Метод code() делает шрифт моноширным.
    # Формирует строки и конкатинирует их с символом новой строки.
    # Когда количетво как бы строк subStrokeSum в общей строке достигает максимума,
    # выводит в телеграм, затем поновой бежит по списку слов. 
    
    sum_all_strok = 0  # общее кол-во слов
    sum_strok = 0      # ограничитель печатаемых ботом строк
    dict_word_bot = '' # формируемая для отправки боту строка
    sum_all_words = '' # строка для печати кол-ва всех слов в словаре
    subStrokeSum = 50  # кол-во подстрок в строке
    len_col = 15       # ширина колонок
    
    for i in dict.dict_words:        
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
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /help. """
    await message.answer(Texts.answerHelp) # текст из модуля    



@dp.message_handler()
async def send_welcome(message: types.Message, state: FSMContext):
    """ Отвечает на любые сообщения."""
    # Проверяет, нет ли в сообщении ответа (кнопка ответить).
    # Если ответ есть, вызываем CheckingResponse(message) с передачей методу самого сообщения.
    # Иначе предлагаем пользователю посмотреть справку.

    # логирование
    logUser = str(message.chat.username)
    logDate = str(message.date)
    log = logDate + ' ' + logUser
    print(log)

    # Проверяем, есть ли данные пользователя, если есть, какой статус пользователя.
    # Если пользователю задан вопрос, то вызываем метод проверки ответа пользователя.
    allUserData = await state.get_data()

    if ('userName' in allUserData):
        if (allUserData['userStatus'] == 'userHasQuestion'):
            await CheckingResponseState(message, state)
        else:
            await message.answer(Texts.miniHelp)  
    else:
        await message.answer(Texts.miniHelp)  



async def CheckingResponseState(message, state):
    """Проверка ответа пользователя с использованием данных state."""
    allUserData = await state.get_data() # загружаем статусы пользователя
    answerUser = message.text       # ответ пользователя
    answerUser = answerUser.lower() # всё с маленькой буквы

    currentDictStroke = dict.dict_words[allUserData['idWord']] # текущая строка словаря 
    translatDir = allUserData['translatDir'] # текущее направление перевода
    questionWord = allUserData['questionWord'] # текущий вопрос

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
    if translatDir == 'Rus':
        if (answerUser == (currentDictStroke[0])):
            await message.answer("Правильно\n" + correctAnswer) 
        else:
            await message.answer("Ошибка\n" + correctAnswer)             
            await message.answer("Попробуй ещё")
            await message.answer(questionWord) # повтор вопроса
            return # выход из метода
    
    # проверка ответа пользователья если с ENG на RUS в зависимости от кол-ва синонимов
    if translatDir == 'Eng':
        if len_i == 1:
            if (answerUser == (currentDictStroke[2])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(questionWord) # повтор вопроса
                return # выход из метода

        elif len_i == 2:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(questionWord) # повтор вопроса
                return # выход из метода

        elif len_i == 3:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(questionWord) # повтор вопроса
                return # выход из метода
  
        elif len_i == 4:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(questionWord) # повтор вопроса
                return # выход из метода
        
        elif len_i == 5:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])
            or answerUser == (currentDictStroke[6])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer(questionWord) # повтор вопроса
                return # выход из метода

    await send_welcome2(message, state) # поновой, как буддто пользователь ввёл "/go"


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
    
async def InItStateUser(message: types.Message, state: FSMContext):
    """ Инициирует данные пользователя """
    # Инициализация контекста (данных пользователя)
    await state.update_data(userName=message.chat.username)
    await state.update_data(userStatus='registr')
    await state.update_data(idWord='no')
    await state.update_data(translatDir='no')
    await state.update_data(questionWord='no')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)