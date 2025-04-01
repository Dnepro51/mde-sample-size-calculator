import ipywidgets as widgets
import json
import os
from DataLoader.data_loader import load_data_from_digger, load_data_from_csv
from IPython.display import display, clear_output
import time
import threading

# Определяем путь к файлу с учетными данными
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials_path = os.path.join(project_root, 'login_pass_for_tests.json')

# ============= Глобальные переменные =============
current_method = 'digger'  # Текущий выбранный метод загрузки данных
form_container = widgets.Output()  # Контейнер для отображения форм

# ============= Создание карточек выбора метода =============
digger_card = widgets.Button(
    description='Загрузка из Digger',
    icon='search',
    tooltip='Загрузка данных из API Digger',
    layout=widgets.Layout(
        width='200px',
        height='150px',
        border='2px solid rgb(146, 230, 167)',
        border_radius='8px',
        margin='10px'
    ),
    style=dict(
        button_color='#e7eeff',
        font_weight='bold'
    )
)

file_card = widgets.Button(
    description='Загрузка из CSV',
    icon='upload',
    tooltip='Загрузка локального CSV файла',
    layout=widgets.Layout(
        width='200px',
        height='150px',
        border='2px solid #dee2e6',
        border_radius='8px',
        margin='10px'
    ),
    style=dict(
        button_color='white',
        font_weight='bold'
    )
)

# ============= Создание элементов ввода =============
# Поля ввода для Digger
login_input = widgets.Text(
    value=json.load(open(credentials_path))['login'],
    description='Логин:',
    placeholder='i.ivanov',
    style=dict(description_width='100px')
)

password_input = widgets.Password(
    value=json.load(open(credentials_path))['password'],
    description='Пароль:',
    style=dict(description_width='100px')
)

query_input = widgets.Text(
    description='ID запроса/Ссылка:',
    placeholder='Введите идентификатор запроса',
    style=dict(description_width='100px')
)

# Поле загрузки файла
file_upload = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Выберите файл:',
    layout=widgets.Layout(width='400px')
)

# Добавляем виджет для отображения статуса
loading_status = widgets.HTML(
    value='',
    layout=widgets.Layout(margin='10px 0px')
)

# Создаем контейнер для виджета статуса
status_container = widgets.VBox([
    loading_status
], layout=widgets.Layout(display='none'))  # Скрываем по умолчанию

# ============= Создание кнопок действий =============
digger_execute_button = widgets.Button(
    description='Выполнить запрос',
    icon='play',
    style=dict(button_color='#4CAF50', font_weight='bold'),
    layout=widgets.Layout(width='200px', margin='10px 0px')
)

file_process_button = widgets.Button(
    description='Обработать файл',
    icon='play',
    style=dict(button_color='#4CAF50', font_weight='bold'),
    layout=widgets.Layout(width='200px', margin='10px 0px')
)

# ============= Создание форм =============
digger_form = widgets.VBox([
    widgets.HTML(value='<h3>Авторизация в Digger</h3>'),
    login_input,
    password_input,
    query_input,
    digger_execute_button
])

file_form = widgets.VBox([
    widgets.HTML(value='<h3>Загрузка файла CSV</h3>'),
    file_upload,
    widgets.Output(),
    file_process_button
])

# ============= Создание контейнеров =============
cards_container = widgets.HBox([
    digger_card, file_card
], layout=widgets.Layout(
    justify_content='center',
    margin='20px 0px'
))

config_output = widgets.Output()  # Контейнер для вывода конфигурации

# ============= Вспомогательные функции =============
def update_card_styles():
    """Обновляет стили карточек в зависимости от выбранного метода"""
    digger_card.style.button_color = 'white'
    file_card.style.button_color = 'white'
    digger_card.layout.border = '2px solid #dee2e6'
    file_card.layout.border = '2px solid #dee2e6'
    
    if current_method == 'digger':
        digger_card.style.button_color = '#e7eeff'
        digger_card.layout.border = '2px solid #4a6baf'
    else:
        file_card.style.button_color = '#e7eeff'
        file_card.layout.border = '2px solid #4a6baf'

def get_uploaded_files():
    """Возвращает список загруженных файлов"""
    if isinstance(file_upload.value, dict):
        return list(file_upload.value.values())
    elif isinstance(file_upload.value, (tuple, list)):
        return list(file_upload.value)
    return []

def get_data_fetch_config(method):
    """Возвращает конфигурацию загрузки данных в зависимости от метода"""
    if method == 'digger':
        return {
            'type': 'digger',
            'auth_login': login_input.value,
            'auth_pass': password_input.value,
            'query_id': query_input.value
        }
    else:
        uploaded_files = get_uploaded_files()
        csv_content = uploaded_files[0]['content'] if uploaded_files else None
        return {
            'type': 'file',
            'file_content': csv_content
        }

# ============= Обработчики событий =============
def on_digger_click(b):
    """Обработчик нажатия на карточку Digger"""
    global current_method
    current_method = 'digger'
    update_card_styles()
    with form_container:
        form_container.clear_output()
        display(digger_form)

def on_file_click(b):
    """Обработчик нажатия на карточку File"""
    global current_method
    current_method = 'file'
    update_card_styles()
    with form_container:
        form_container.clear_output()
        display(file_form)

# ============= Основная функция отображения =============
def display_interface(on_data_loaded=None):
    """
    Отображает интерфейс загрузки данных
    Args:
        on_data_loaded: callback-функция, которая будет вызвана после успешной загрузки данных
    """
    def on_digger_execute(b):
        """Обработчик выполнения запроса к Digger"""
        nonlocal on_data_loaded  # Важно! Добавляем nonlocal
        config = get_data_fetch_config('digger')

        with config_output:
            config_output.clear_output()
            errors = []
            if not login_input.value.strip():
                errors.append("Необходимо указать логин.")
            if not password_input.value.strip():
                errors.append("Необходимо указать пароль.")
            if not query_input.value.strip():
                errors.append("Необходимо указать ID запроса или ссылку.")

            if errors:
                for err in errors:
                    print(f"Ошибка: {err}")
            else:
                # Показываем контейнер статуса
                status_container.layout.display = 'flex'
                
                # Показываем статус загрузки
                loading_status.value = '<div style="color: #4CAF50;">Загрузка данных из Digger...</div>'
                
                try:
                    # Загружаем данные
                    data = load_data_from_digger(config)
                    
                    # Обновляем статус
                    loading_status.value = '<div style="color: #4CAF50;">Загрузка завершена!</div>'
                    
                    # Вызываем callback если он предоставлен
                    if on_data_loaded:
                        on_data_loaded(data)
                
                except Exception as e:
                    loading_status.value = f'<div style="color: red;">Ошибка при загрузке: {str(e)}</div>'

    def on_file_process(b):
        """Обработчик обработки файла"""
        nonlocal on_data_loaded
        config = get_data_fetch_config('file')

        with config_output:
            config_output.clear_output()
            uploaded_files = get_uploaded_files()
            if not uploaded_files:
                print("Ошибка: Необходимо загрузить CSV-файл.")
            else:
                # Показываем контейнер статуса
                status_container.layout.display = 'flex'
                
                # Показываем статус загрузки
                loading_status.value = '<div style="color: #4CAF50;">Обработка CSV файла...</div>'
                
                try:
                    # Загружаем данные через функцию из data_loader
                    data = load_data_from_csv(config)
                    
                    # Обновляем статус
                    loading_status.value = '<div style="color: #4CAF50;">Обработка завершена!</div>'
                    
                    # Вызываем callback если он предоставлен
                    if on_data_loaded:
                        on_data_loaded(data)
                
                except Exception as e:
                    loading_status.value = f'<div style="color: red;">Ошибка при обработке: {str(e)}</div>'

    # Привязка обработчиков
    digger_card.on_click(on_digger_click)
    file_card.on_click(on_file_click)
    digger_execute_button.on_click(on_digger_execute)  # Привязываем локальные обработчики
    file_process_button.on_click(on_file_process)      # Привязываем локальные обработчики

    # Отображение интерфейса
    display(cards_container)
    display(form_container)
    display(status_container)
    display(config_output)
    with form_container:
        display(digger_form)