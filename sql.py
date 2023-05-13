###################################################################################################
# NOTE
###################################################################################################
# Работа с базой данный.
###################################################################################################


# встроенный модуль работы с БД
import sqlite3 as sql

# имя БД
# bd_name = 'English-training.db'
bd_name = 'English-training_test.db'


def read_dict_words_sql() -> list:
    """Читает слова из БД. Возвращает список кортежей."""

    SQL = f"SELECT eng, transcript_cyrillic, rus_1, rus_2, rus_3, rus_4, rus_5 FROM dict"
    with sql.connect(bd_name) as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    return SQL_result


# def read_texts_sql(name) -> str:
def read_texts_sql(text_name: str) -> str:
    """ Читает разные предложения из БД.    
    Принимает аргумент с названием строчки с текстом в БД.
    [0][0] - вынимает предложение и кортежа и списка. """

    SQL = f"SELECT text FROM texts WHERE name = '{text_name}' "
    with sql.connect(bd_name) as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
        SQL_result = SQL_result[0][0]
    return SQL_result
