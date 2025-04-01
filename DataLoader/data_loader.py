# Модуль, принимающий конфигурацию загрузки данных и возвращающий датафрейм
import digger as dg
import pandas as pd
from IPython.display import display
import time
import io

def load_data_from_digger(config):
    """
    Загружает данные из Digger в датафрейм
    1. Авторизация в Digger происходит через библиотеку digger
    2. Запрос данных происходит через библиотеку digger
    Входные параметры:
        config:
            auth_login: логин для авторизации в Digger
            auth_pass: пароль для авторизации в Digger
            query_id: id запроса в Digger
    Возвращает:
        dict: 
            df: датафрейм с данными из Digger,
            columns: список колонок в датафрейме
    """
    # Авторизация в Digger
    dg.set_auth(config['auth_login'], config['auth_pass'])

    # Запрос данных из Digger
    df = dg.get_df(int(config['query_id']))

    # Показываем информацию о датафрейме
    df.info()

    # Список колонок в датафрейме
    columns = df.columns.tolist()

    return {'df': df, 'columns': columns}

def load_data_from_csv(config):
    """
    Загружает данные из CSV в датафрейм
    Входные параметры:
        config:
            file_content: содержимое CSV файла
    Возвращает:
        dict: 
            df: датафрейм с данными из CSV,
            columns: список колонок в датафрейме
    """
    # Читаем CSV из содержимого файла
    df = pd.read_csv(io.BytesIO(config['file_content']))
    
    # Список колонок в датафрейме
    columns = df.columns.tolist()
    
    return {'df': df, 'columns': columns}


