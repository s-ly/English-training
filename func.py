# Дочерний модуль, содержит функции для бота

from aiogram import types
from aiogram.dispatcher import FSMContext

import csv      # для чтения таблици




# читаем из таблици данные в наш список списков dict_words
dict_words = []
read_file = open('dict.csv', 'r')
for row in csv.reader(read_file):
    dict_words.append(row)
read_file.close()




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




# принимает строку словаря (список), возвращает число
# подсчитываем кол-во синонимов в каждой строке
# no_none_sub_i - кол-во непустых ячеек в строке
# len_i - получаемое колво синонимов
# Цикл бежит по строке и считает непустые ячейки, потом вычитаем 2, так как первые две ячейки
# это английское слово и транскрипция. 
async def SumSynonym(dict_string):
    """Подсчёт кол-ва синонимов в строке словаря."""
    no_none_sub_i = 0
    len_i = 0
    for sub_i in dict_string:
        if(sub_i != ''):
            no_none_sub_i = no_none_sub_i + 1
    len_i = no_none_sub_i - 2
    return len_i




async def TooltipGenerator(currentDictStroke, translatDir):
    """генератор подсказок"""
    # tooltip = str(currentDictStroke) + str(translatDir)
    if (translatDir == 'Rus'):
        word = currentDictStroke[0] # английское слово
    elif (translatDir == 'Eng'):
        word = currentDictStroke[2] # русское слово

    numberOfLetters = len(word) # длинна слова
    firstLetter = word[0]       # первая буква слова
    tooltip = firstLetter + ('*' * (numberOfLetters-1))  
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









