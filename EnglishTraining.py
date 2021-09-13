""" English_training ver 2.0 aplha 2.
Программа для разучивания английских слов. Выводит список слов для перевода.
Также является модулем для EnglishTrainingBot.py
"""

import random   # для раднома
import csv      # для чтения таблици
import colorama # для цвета шрифта 
from colorama import Fore, Back, Style

colorama.init()

menu_sel = ""   # обнулённая глобальная переменная - выбор из меню
errors = 0      # обнулённый счётчик ошибок пользователя

# длина колонок
len_col_0 = 15
len_col_1 = 15
len_col_2 = 15

# читаем из таблици данные в наш список списков dict_words
dict_words = []
# read_file = open('dict_test.csv', 'r')
read_file = open('dict.csv', 'r')
for row in csv.reader(read_file):
    dict_words.append(row)
read_file.close()

# копируем исходный список, так как требуется его перемешивать.
copy_dict_words = dict_words.copy()



def menu_select() -> str:
    """ Выводит меню и принемает с клавиатуры выбор пользователья.
    Если от 0 до 3 то возврат, иначе по новой. Работает с глобальной переменной.
    """
    # распечатываем меню
    print("0 - Выход")
    print("1 - С русского на английский")
    print("2 - С английского на русский")
    print("3 - Распечатать список") 
    
    global menu_sel
    
    # ввод и проверка, иначе поновой
    menu_sel = input("Ваш выбор: ")
    if menu_sel == "0" or menu_sel == "1" or menu_sel == "2" or menu_sel == "3":
        print()
        return (menu_sel)
    else:
        print()
        menu_select() # выбираем снова



def print_dict():
    """Распечатывает исходный словарь"""
    # берём глобальную пеперенную ширины колонок
    global len_col_0
    global len_col_1
    global len_col_2    
    
    for i in dict_words:
        # вычисляем недостающее кол-во пробелов для ширины колонок
        # для 1 и 2 колонки
        dobavka_col_0 = len_col_0 - len(i[0])
        dobavka_col_1 = len_col_1 - len(i[1])
        dobavka_col_2 = len_col_2 - len(i[2])
        
        # формируем и выводим строку со всеми колонками
        print(i[0] + (" " * dobavka_col_0) +
              "[" + i[1] + "]" + (" " * dobavka_col_1) +
              i[2] + (" " * dobavka_col_2) +              
              i[3])           
        
    print()    
    print("Всего слов:", len(dict_words), "\n") # длина списка



def translate_RusToEng():
    """ Принимает скопированный ранее списко.
    Пользователь вводит перевод с РУС на ENG.
    Проверяет каждый ввод. """

    for i in copy_dict_words:            
        answer_user = input("".join(i[2])+" - ")
        if answer_user == i[0]:
            print("Правильно.", i[1], i[3], "\n")        
        elif answer_user == "0":
            break_fun() # прерывание упражнения при вводе "0"
            break
        else:
            print(Fore.RED + "Ошибка." + Style.RESET_ALL, 
            "Правильный ответ:", i[0], i[1], i[3],"\n")
            # увеличиваем съётчик ошибок
            global errors
            errors += 1



def translate_EngToRus():
    """ Принимает скопированный ранее списко.
    Пользователь вводит перевод с ENG на РУС.
    Проверяет каждый ввод. """
    
    for i in copy_dict_words:
        answer_user = input("".join(i[0])+" - ")
        if answer_user == i[2]:
            print("Правильно", i[1], i[3], "\n")        
        elif answer_user == "0":
            break_fun() # прерывание упражнения при вводе "0"
            break
        else:
            print(Fore.RED + "Ошибка." + Style.RESET_ALL, 
            "Правильный ответ:", i[2], i[1], i[3],"\n")            
            global errors
            errors += 1 # увеличиваем съётчик ошибок

            

def break_fun():
    """Прерывание упражнения при вводе '0'"""
    global menu_sel            
    menu_sel = ""
    print("Упражнение прервано. \n")



def start():
    """Запускающая функция"""
    print("\nEnglish training ver 2.0 alpha \n")    
    global menu_sel
    # перемешивает скопированную последовательность    
    random.shuffle(copy_dict_words) 
    global errors # хранитт ошибки
    
    # если ничего не выбранно
    if menu_sel == "":
        menu_select()
        start()
    elif menu_sel == "1":
        translate_RusToEng()        
        # печать околичества ошибок        
        print ('Ошибок:', errors, 'из', len(dict_words), '\n') 
        errors = 0 # обнуление        
        menu_sel="" # обнуляем выбор
        start()        
    elif menu_sel == "2":
        translate_EngToRus()
        # печать околичества ошибок        
        print ('Ошибок:', errors, 'из', len(dict_words), '\n') 
        errors = 0 # обнуление        
        menu_sel="" # обнуляем выбор
        start()        
    elif menu_sel == "3":
        print_dict()        
        menu_sel="" # обнуляем выбор
        start()        
    else:
        print("До свидания!", "\n")



if __name__ == '__main__':
    start()
