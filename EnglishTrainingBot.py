# Телеграм бот t.me/EngTraining_Bot
# Тренирует английские слова.

from os import stat
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext # хранение контекста
from aiogram.contrib.fsm_storage.memory import MemoryStorage # место для хранения контекста в ОЗУ

# необходимо делать проверку на полное совпадение текста. через специальный фильтр Text 
from aiogram.dispatcher.filters import Text

# для кнопок
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup

# дополнительно для форматирования
from aiogram.utils.markdown import text, bold, italic, code, underline, strikethrough
import MyToken         # содержит токен
import func            # мой модуль, содержит функции для бота
import Texts           # мой модуль, хранит текст
import log             # мой модуль, лог
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

# создаём коавиатуру и добавляем кнопки
# resize_keyboard=True - уменьшает кнопки
# one_time_keyboard=True - скрыть кнопку после нажатия
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('* Не помню *')
button2 = KeyboardButton('* Подсказка *')
keyboard.add(button1, button2)




# (Text(equals="* Не помню *")) проверяется полное сооьветствие с текстом
# ReplyKeyboardRemove() - удаляет клавиатуру из меню
@dp.message_handler(Text(equals="* Не помню *"))
async def with_puree(message: types.Message, state: FSMContext):
    """ Отвечает на текс '* Не помню *'"""
    allUserData = await state.get_data() # загружаем статусы пользователя
    questionWord = allUserData['questionWord'] # текущий вопрос
    currentDictStroke = func.dict_words[allUserData['idWord']] # текущая строка словаря 
    
    # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
    len_i = await func.SumSynonym(currentDictStroke) 

    # формируем строку правильного ответа в зависимости от кол-ва синонимов (len_i)
    correctAnswer = await func.CorrectAnswer(currentDictStroke, len_i)

    await message.answer(correctAnswer) # правильный ответ 
    await message.answer('? ' + str(questionWord)) # повтор вопроса




# (Text(equals="* Подсказка *")) проверяется полное сооьветствие с текстом
@dp.message_handler(Text(equals="* Подсказка *"))
async def with_puree(message: types.Message, state: FSMContext):
    """ Отвечает на текс '* Подсказка *'"""
    allUserData = await state.get_data() # загружаем статусы пользователя
    currentDictStroke = func.dict_words[allUserData['idWord']] # текущая строка словаря 
    translatDir = allUserData['translatDir'] # текущее направление перевода
    tooltip = await func.TooltipGenerator(currentDictStroke, translatDir) # генератор подсказок
    await message.answer(tooltip) 




# ReplyKeyboardRemove() - удаляет клавиатуру из меню
@dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    """ Отвечает на команды /start """
    # Второй параметр FSMContext хранит контекст 
    
    await func.InItStateUser(message, state)

    await message.answer("English Training\n" + 
    "Тренируй английские слова!\nДля начала тренировки введи /go, справка /help (с палочкой).",
    reply_markup=ReplyKeyboardRemove())
    await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go




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
    await func.InItStateUser(message, state)

    allUserData = await state.get_data() # загружаем статусы пользователя

    dictRandomID = None # без этого появлялась ошибка выхода из диапазона (иногда)
    questionWord = None # обнуление старого вопроса (на всякий)
    randomDictStroke = None
    languageSelection = random.randint(0, 1)         # случайный выбор языка
    dictLen = len(func.dict_words)                   # кол-во слов в словаре
    dictRandomID = random.randint(0, dictLen - 1)    # случайное слово
    await state.update_data(idWord=dictRandomID)     # случайное слово в статус пользователя
    randomDictStroke = func.dict_words[dictRandomID] # случайная строка

    # фрмирование строки вопроса изходя из случайно выбранного направления перевода
    # если с русского то учитывается кол-во синонимов
    if languageSelection == 0:
        await state.update_data(translatDir='Eng') # направление перевода в статус пользователя

        questionWord = str(randomDictStroke[0])

    elif languageSelection == 1:
        await state.update_data(translatDir='Rus') # направление перевода в статус пользователя

        len_i = 0 # получаемое кол-во синонимов (обнуление)    
        # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
        len_i = await func.SumSynonym(randomDictStroke) 
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
    
    # Идея в том, что бы клавиатура всплыла только один раз, а потом не надоедала,
    # а просто была в виде значка, для этого используем FSM параметр showkeyboard='true'.
    if (allUserData['showkeyboard'] == 'true'):
        await message.answer('? ' + str(questionWord),
        reply_markup=keyboard) # параметр передаёт клавиатуру
        
        # подсказка про меню (с формаьтрованием)
        await message.answer(italic('(кнопка с подсказкой -> квадратик справа)'),
        parse_mode=types.ParseMode.MARKDOWN_V2) 

        await state.update_data(showkeyboard='false') # больше показывать клавиатуру не надо
    else:
        await message.answer('? ' + str(questionWord)) # без клавиатуры

    await state.update_data(questionWord=str(questionWord)) # статус пользователя: вопрос
    await state.update_data(userStatus='userHasQuestion') # статус пользователя: пользователю задан вопрос
    
    


# Берёт из модуля func список слов dict_words. 
# Метод code() делает шрифт моноширным.
# Формирует строки и конкатинирует их с символом новой строки.
# Когда количетво как бы строк subStrokeSum в общей строке достигает максимума,
# выводит в телеграм, затем поновой бежит по списку слов. 
@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /dict."""    
    sum_all_strok = 0  # общее кол-во слов
    sum_strok = 0      # ограничитель печатаемых ботом строк
    dict_word_bot = '' # формируемая для отправки боту строка
    sum_all_words = '' # строка для печати кол-ва всех слов в словаре
    subStrokeSum = 50  # кол-во подстрок в строке
    len_col = 15       # ширина колонок
    
    for i in func.dict_words:        
        sum_strok = sum_strok + 1         # сётчик строк
        sum_all_strok = sum_all_strok + 1 # счётчик всех слов в словаре

        # вычисляем недостающее кол-во пробелов для ширины колонок
        dobavka_col_0 = len_col - len(i[0])

        len_i = 0 # получаемое колво синонимов
        len_i = await func.SumSynonym(i) # Подсчёт кол-ва синонимов в строке словаря (мой метод)

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




# ReplyKeyboardRemove() - удаляет клавиатуру из меню
@dp.message_handler(commands=['help'])
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /help. """
    await message.answer(Texts.answerHelp, reply_markup=ReplyKeyboardRemove()) # текст из модуля    
    await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go




# ReplyKeyboardRemove() - удаляет клавиатуру из меню
# Проверяет, нет ли в сообщении ответа (кнопка ответить).
# Если ответ есть, вызываем CheckingResponse(message) с передачей методу самого сообщения.
# Иначе предлагаем пользователю посмотреть справку.
@dp.message_handler()
async def send_welcome(message: types.Message, state: FSMContext):
    """ Отвечает на любые сообщения."""

    # логирование
    logUser = str(message.chat.username)
    logDate = str(message.date)
    logMessage = logDate + ' ' + logUser
    await log.log_message(logMessage) # лог, в моём модуле

    # Проверяем, есть ли данные пользователя, если есть, какой статус пользователя.
    # Если пользователю задан вопрос, то вызываем метод проверки ответа пользователя.
    allUserData = await state.get_data()

    if ('userName' in allUserData):
        if (allUserData['userStatus'] == 'userHasQuestion'):
            # Проверка ответа пользователя
            userResponseStatutes = await func.CheckingResponseState(message, state) 

            if (userResponseStatutes == True):
                # Если пользователь ответил правильно, то новый вопрос,
                # как буддто пользователь ввёл "/go"
                await send_welcome2(message, state) 
        else:
            await message.answer(Texts.miniHelp, reply_markup=ReplyKeyboardRemove())  
            await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go
    else:
        await message.answer(Texts.miniHelp, reply_markup=ReplyKeyboardRemove())  
        await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)