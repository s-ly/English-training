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




@dp.message_handler(Text(equals="* Не помню *"))
async def with_puree(message: types.Message, state: FSMContext):
    """ Отвечает на текс '* Не помню *'"""
    # (Text(equals="* Не помню *")) проверяется полное сооьветствие с текстом
    # ReplyKeyboardRemove() - удаляет клавиатуру из меню

    allUserData = await state.get_data() # загружаем статусы пользователя
    questionWord = allUserData['questionWord'] # текущий вопрос
    currentDictStroke = func.dict_words[allUserData['idWord']] # текущая строка словаря 
    
    # Подсчёт кол-ва синонимов в строке словаря (мой метод) 
    len_i = await func.SumSynonym(currentDictStroke) 

    # формируем строку правильного ответа в зависимости от кол-ва синонимов (len_i)
    correctAnswer = await func.CorrectAnswer(currentDictStroke, len_i)

    await message.answer(correctAnswer) # правильный ответ 
    await message.answer('? ' + str(questionWord)) # повтор вопроса




@dp.message_handler(Text(equals="* Подсказка *"))
async def with_puree(message: types.Message, state: FSMContext):
    """ Отвечает на текс '* Подсказка *'"""
    # (Text(equals="* Подсказка *")) проверяется полное сооьветствие с текстом

    allUserData = await state.get_data() # загружаем статусы пользователя
    currentDictStroke = func.dict_words[allUserData['idWord']] # текущая строка словаря 
    translatDir = allUserData['translatDir'] # текущее направление перевода
    tooltip = await func.TooltipGenerator(currentDictStroke, translatDir) # генератор подсказок
    await message.answer(tooltip) 




@dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    """ Отвечает на команды /start """
    # Второй параметр FSMContext хранит контекст 
    # ReplyKeyboardRemove() - удаляет клавиатуру из меню
    
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
    """ Отвечает на команды /go. Создаёт строку вопроса."""
    await func.goFunc(message, state, keyboard)
        



@dp.message_handler(commands=['dict'])
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /dict."""    
    await func.dictFunc(message)




# ReplyKeyboardRemove() - удаляет клавиатуру из меню
@dp.message_handler(commands=['help'])
async def send_test(message: types.Message, state: FSMContext):
    """ Отвечает на команды /help. """
    await message.answer(Texts.answerHelp, reply_markup=ReplyKeyboardRemove()) # текст из модуля    
    await state.update_data(showkeyboard='true') # теперь клава буду вызвана при /go




@dp.message_handler()
async def send_welcome(message: types.Message, state: FSMContext):
    """ Отвечает на любые сообщения."""
    userResponse = await func.RespondsAnyMessages(message, state) 
    if (userResponse == True):
        # Если пользователь ответил правильно, то новый вопрос,
        # как буддто пользователь ввёл "/go"
        await send_welcome2(message, state)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)