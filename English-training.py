""" English_training ver 1.9
Программа для разучивания английских слов. Выводит список слов для перевода.
"""
# https://www.en365.ru/top1000.htm - словарь

import random   # для раднома
import csv      # для чтения таблици

menu_sel = ""   # обнулённая глобальная переменная - выбор из меню
errors = 0      # обнулённый счётчик ошибок пользователя

# длина колонок
len_col_0 = 15
len_col_1 = 15

# читаем из таблици данные в наш список списков dict_words
dict_words = []
read_file = open('dict.csv', 'r')
for row in csv.reader(read_file):
    dict_words.append(row)
read_file.close()

# копируем исходный список, так как требуется его перемешивать.
copy_dict_words = dict_words.copy()


def menu_select():
    """ Выводит меню и принемает с клавиатуры выбор пользователья.
    Если от 0 до 3 то возврат, иначе по новой.
    Работает с глобальной переменной.
    """
    # распечатываем меню
    print("0 - Выход")
    print("1 - С русского на английский")
    print("2 - С английского на русский")
    print("3 - Распечатать список") 
    # берём глобальную пеперенную
    global menu_sel
    # ввод и проверка, иначе поновой
    menu_sel = input("Ваш выбор: ")
    if menu_sel == "0" or menu_sel == "1" or menu_sel == "2" or menu_sel == "3":
        print()
        return (menu_sel)
    else:
        print()
        menu_select()


def print_dict():
    """Распечатывает исходный словарь"""
    # берём глобальную пеперенную ширины колонок
    global len_col_0
    global len_col_1
    
    for i in dict_words:
        # вычисляем дедостающее кол-во пробелов для ширины колонок
        # для 1 и 2 колонки
        dobavka_col_0 = len_col_0 - len(i[0])
        dobavka_col_1 = len_col_1 - len(i[1])
        
        # формируем и выводим строку со всеми колонками
        print(i[0] + (" " * dobavka_col_0) +
              i[1] + (" " * dobavka_col_1) +
              i[2])        
        
    print()
    # длина списка
    print("Всего слов:", len(dict_words), "\n")


def translate_RusToEng():
    """ Принимает скопированный ранее списко.
    Пользователь вводит перевод с РУС на ENG.
    Проверяет каждый ввод.
    """
    for i in copy_dict_words:
        # ели есть примечание, выводим его (то есть ячейка не пустая)
        ###if len(i[3]) != 0:
        ###    print(i[3])
            
        answer_user = input("".join(i[2])+" - ")
        if answer_user == i[0]:
            print("Правильно", "\n")            
        # прерывание упражнения при вводе "0"
        elif answer_user == "0":
            break_fun()
            break
        else:
            print("Ошибка.", "Правильный ответ:", i[0], "\n")
            # увеличиваем съётчик ошибок
            global errors
            errors += 1


def translate_EngToRus():
    """ Принимает скопированный ранее списко.
    Пользователь вводит перевод с ENG на РУС.
    Проверяет каждый ввод.
    """
    for i in copy_dict_words:
        # ели есть примечание, выводим его (то есть ячейка не пустая)
        if len(i[3]) != 0:
            print(i[3])
            
        answer_user = input("".join(i[0])+" - ")
        if answer_user == i[2]:
            print("Правильно", "\n")                    
        # прерывание упражнения при вводе "0"
        elif answer_user == "0":
            break_fun()
            break
        else:
            print("Ошибка.", "Правильный ответ:", i[2], "\n")
            # увеличиваем съётчик ошибок
            global errors
            errors += 1

            

def break_fun():
    """Прерывание упражнения при вводе '0'"""
    global menu_sel            
    menu_sel = ""
    print("Упражнение прервано. \n")


def start():
    """Запускающая функция"""
    # берём глобальную переменную
    global menu_sel
    # перемешивает скопированную последовательность
    random.shuffle(copy_dict_words)
    # доступ к голобальной переменной хранящей ошибки
    global errors
    
    # если ничего не выбранно
    if menu_sel == "":
        menu_select()
        start()
    elif menu_sel == "1":
        translate_RusToEng()
        # печать околичества ошибок
        print ('Ошибок:', errors, 'из', len(dict_words), '\n')
        # обнуление
        errors = 0        
        # обнуляем выбор
        menu_sel=""
        start()        
    elif menu_sel == "2":
        translate_EngToRus()
        # печать околичества ошибок
        print ('Ошибок:', errors, 'из', len(dict_words), '\n')
        # обнуление
        errors = 0        
        # обнуляем выбор
        menu_sel=""
        start()        
    elif menu_sel == "3":
        print_dict()
        # обнуляем выбор
        menu_sel=""
        start()        
    else:
        print("До свидания!", "\n")


print("\nEnglish training ver 1.9 \n")
start() 
