###################################################################################################
# NOTE
###################################################################################################
# Работа с базой данный.
###################################################################################################


# встроенный модуль работы с БД
import sqlite3 as sql


def read_dict_words_sql() -> list:
    """Читает слова из БД. Возвращает список кортежей."""

    SQL = f"SELECT eng, transcript_cyrillic, rus_1, rus_2, rus_3, rus_4, rus_5 FROM dict"
    with sql.connect('English-training.db') as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    return SQL_result

