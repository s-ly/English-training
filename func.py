# Дочерний модуль, содержит функции для бота

from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext

import csv       # для чтения таблици
import random    # для раднома
import log       # мой модуль, лог
import Texts     # мой модуль, хранит текст
import sql

# для кнопок
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup

# для форматирования
from aiogram.utils.markdown import italic, code


# глобальный список списков слов
dict_words = []

# читаем из таблици данные в наш список списков dict_words
# dict_words = []
# read_file = open('dict_test.csv', 'r')
# for row in csv.reader(read_file):
#     dict_words.append(row)
# read_file.close()


def dict_words_converter():
    """ Создаёт из БД список списков слов.
    
    В начале берём глобальный список и обнуляем его. Потом читаем из БД новй список кортежей.
    Его нужно переделать в список списков. Два временных списка, один для переделки кортежей в список,
    второй для списка этих списков. Если в БД ячейка пустая None, то пишем туда пустую строку.
    Временный список списков присваеваем глобальному, а потом временный список обнуляем. """

    global dict_words
    dict_words = []

    dict_words_sql = sql.read_dict_words_sql()

    new_str = []
    new_dic = []
    for i in dict_words_sql:
        for j in i:
            if j != None:
                new_str.append(j)
            else:
                new_str.append('')
        new_dic.append(new_str)
        new_str = []
    dict_words = new_dic
    new_dic = []     


# Наполняем список списков словами
dict_words_converter()


async def CorrectAnswer(currentDictStroke, len_i):
    """формируем строку правильного ответа в зависимости от кол-ва синонимов (len_i)"""
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

    return correctAnswer




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




async def TooltipGenerator(currentDictStroke, translatDir):
    """генератор подсказок"""
    if (translatDir == 'Rus'):
        word = currentDictStroke[0] # английское слово
    elif (translatDir == 'Eng'):
        word = currentDictStroke[2] # русское слово

    numberOfLetters = len(word) # длинна слова
    firstLetter = word[0]       # первая буква слова
    tooltip = firstLetter + ('*' * (numberOfLetters-1))  
    return tooltip




async def TooltipGenerator2(currentDictStroke, translatDir):
    """генератор дополнительных подсказок"""
    if (translatDir == 'Rus'):
        word = currentDictStroke[0] # английское слово
    elif (translatDir == 'Eng'):
        word = currentDictStroke[2] # русское слово
    numberOfLetters = len(word) # длинна слова

    if (numberOfLetters == 1):
        firstLetter = word[0]        # первая буква слова
        tooltip = firstLetter
        return tooltip
    elif (numberOfLetters == 2):
        firstLetter = word[0]        # первая буква слова
        secondLetter = word[1]       # вторая буква слова
        tooltip = firstLetter + secondLetter
        return tooltip
    elif (numberOfLetters == 3):
        firstLetter = word[0]        # первая буква слова
        secondLetter = word[1]       # вторая буква слова
        lastLetter = word[-1]        # последняя (третья) буква слова
        tooltip = firstLetter + secondLetter + lastLetter
        return tooltip
    else:
        firstLetter = word[0]        # первая буква слова
        secondLetter = word[1]       # вторая буква слова
        lastLetter = word[-1]        # последняя буква слова
        tooltip = firstLetter + secondLetter + ('*' * (numberOfLetters-3)) + lastLetter
        return tooltip




async def InItStateUser(message: types.Message, state: FSMContext):
    """ Инициирует данные пользователя """
    # Инициализация контекста (данных пользователя)
    # если инициализации ещё небыло
    allUserData = await state.get_data() # загружаем статусы пользователя

    if ('userStatus' in allUserData):
        # print('инициация уже была, ')
        # обнуляем только то что нужно (кроме показа клавиатуры)
        await state.update_data(userName=message.chat.username)
        await state.update_data(userStatus='registr')
        await state.update_data(idWord='no')
        await state.update_data(translatDir='no')
        await state.update_data(questionWord='no')
        # print(str(allUserData['showkeyboard']))
    else:
        # print('инициируем')
        # инициируем всё
        await state.update_data(userName=message.chat.username)
        await state.update_data(userStatus='registr')
        await state.update_data(idWord='no')
        await state.update_data(translatDir='no')
        await state.update_data(questionWord='no')
        await state.update_data(showkeyboard='true')




async def CheckingResponseState(message, state) -> bool:
    """Проверка ответа пользователя с использованием данных state."""

    # статут ответа пользователя (метот его возврашщает)
    # false - пользователь ошибся и новый вопрос пока задавать не надо
    # true - пользователь ответил правильно, будет новый вопрос
    userResponseStatutes: bool = None

    allUserData = await state.get_data() # загружаем статусы пользователя
    answerUser = message.text       # ответ пользователя
    answerUser = answerUser.lower() # всё с маленькой буквы

    currentDictStroke = dict_words[allUserData['idWord']] # текущая строка словаря 
    translatDir = allUserData['translatDir'] # текущее направление перевода
    questionWord = allUserData['questionWord'] # текущий вопрос

    len_i = 0 # получаемое кол-во синонимов (обнуление)
    
    # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
    len_i = await SumSynonym(currentDictStroke) 

    # формируем строку правильного ответа в зависимости от кол-ва синонимов (len_i)
    correctAnswer = await CorrectAnswer(currentDictStroke, len_i)

    # проверка ответа пользователья если с RUS на ENG
    if translatDir == 'Rus':
        if (answerUser == (currentDictStroke[0])):
            await message.answer("Правильно\n" + correctAnswer)             
        else:
            await message.answer("Ошибка\n" + correctAnswer)             
            await message.answer("Попробуй ещё")
            await message.answer('? ' + str(questionWord)) # повтор вопроса
            userResponseStatutes = False # пользователь ошибся
            return userResponseStatutes
    
    # проверка ответа пользователья если с ENG на RUS в зависимости от кол-ва синонимов
    if translatDir == 'Eng':
        if len_i == 1:
            if (answerUser == (currentDictStroke[2])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer('? ' + str(questionWord)) # повтор вопроса
                userResponseStatutes = False # пользователь ошибся
                return userResponseStatutes

        elif len_i == 2:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer('? ' + str(questionWord)) # повтор вопроса 
                userResponseStatutes = False # пользователь ошибся
                return userResponseStatutes

        elif len_i == 3:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")                
                await message.answer('? ' + str(questionWord)) # повтор вопроса
                userResponseStatutes = False # пользователь ошибся
                return userResponseStatutes
  
        elif len_i == 4:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer('? ' + str(questionWord)) # повтор вопроса
                userResponseStatutes = False # пользователь ошибся
                return userResponseStatutes
        
        elif len_i == 5:
            if (answerUser == (currentDictStroke[2]) or answerUser == (currentDictStroke[3]) 
            or answerUser == (currentDictStroke[4]) or answerUser == (currentDictStroke[5])
            or answerUser == (currentDictStroke[6])):
                await message.answer("Правильно\n" + correctAnswer) 
            else:
                await message.answer("Ошибка\n" + correctAnswer) 
                await message.answer("Попробуй ещё")
                await message.answer('? ' + str(questionWord)) # повтор вопроса
                userResponseStatutes = False # пользователь ошибся
                return userResponseStatutes

    userResponseStatutes = True # пользователь ответил правильно
    return userResponseStatutes




async def goFunc(message: types.Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    """ Отвечает на команды /go. Создаёт строку вопроса."""
    # keyboard: ReplyKeyboardMarkup - принимает клавиатуру

    await InItStateUser(message, state)  # Инициализация контекста (данных пользователя)
    allUserData = await state.get_data() # загружаем статусы пользователя

    dictRandomID = None # без этого появлялась ошибка выхода из диапазона (иногда)
    questionWord = None # обнуление старого вопроса (на всякий)
    randomDictStroke = None
    languageSelection = random.randint(0, 1)         # случайный выбор языка
    dictLen = len(dict_words)                        # кол-во слов в словаре
    dictRandomID = random.randint(0, dictLen - 1)    # случайное слово
    await state.update_data(idWord=dictRandomID)     # случайное слово в статус пользователя
    randomDictStroke = dict_words[dictRandomID]      # случайная строка

    # фрмирование строки вопроса изходя из случайно выбранного направления перевода
    # если с русского то учитывается кол-во синонимов
    if languageSelection == 0:
        await state.update_data(translatDir='Eng') # направление перевода в статус пользователя

        questionWord = str(randomDictStroke[0])

    elif languageSelection == 1:
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




async def dictFunc(message: types.Message):
    """ Отвечает на команды /dict."""    
    # Берёт из модуля func список слов dict_words. 
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
    
    for i in dict_words:        
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




async def RespondsAnyMessages(message: types.Message, state: FSMContext) -> bool:
    """ Отвечает на любые сообщения."""
    # ReplyKeyboardRemove() - удаляет клавиатуру из меню
    # Проверяет, нет ли в сообщении ответа (кнопка ответить).
    # Если ответ есть, вызываем CheckingResponse(message) с передачей методу самого сообщения.
    # Иначе предлагаем пользователю посмотреть справку.

    # логирование
    logUser = str(message.chat.username)
    logDate = str(message.date)
    logMessage = logDate + ' ' + logUser
    await log.log_message(logMessage) # лог, в моём модуле

    # флаг, если подбзователь ответит правило, то = True
    # его вернёт этот метод
    userAnswerCorrect: bool = None

    # Проверяем, есть ли данные пользователя, если есть, какой статус пользователя.
    # Если пользователю задан вопрос, то вызываем метод проверки ответа пользователя.
    allUserData = await state.get_data()

    if ('userName' in allUserData):
        if (allUserData['userStatus'] == 'userHasQuestion'):
            # Проверка ответа пользователя
            userResponseStatutes = await CheckingResponseState(message, state) 

            if (userResponseStatutes == True):
                # Если пользователь ответил правильно, то новый вопрос,
                # как буддто пользователь ввёл "/go"
                userAnswerCorrect = True
        else:
            userAnswerCorrect = False
            await message.answer(Texts.miniHelp, reply_markup=ReplyKeyboardRemove())  
            await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go
    else:
        userAnswerCorrect = False
        await message.answer(Texts.miniHelp, reply_markup=ReplyKeyboardRemove())  
        await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go
    
    return userAnswerCorrect