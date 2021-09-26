# Чтение словаря

import csv      # для чтения таблици

# читаем из таблици данные в наш список списков dict_words
dict_words = []
read_file = open('dict.csv', 'r')
for row in csv.reader(read_file):
    dict_words.append(row)
read_file.close()