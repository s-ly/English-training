# Модуль содержит функции для бота

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