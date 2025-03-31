import ipywidgets as widgets
from IPython.display import display

# Глобальные переменные для хранения состояния
current_method = 'digger'
form_container = widgets.Output()

# Создание карточек
digger_card = widgets.Button(
    description='Загрузка из Digger',
    icon='search',
    tooltip='Загрузка данных из API Digger',
    layout=widgets.Layout(
        width='200px',
        height='150px',
        border='2px solid #dee2e6',
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

# Создание форм ввода
login_input = widgets.Text(
    description='Логин:',
    placeholder='i.ivanov',
    style=dict(description_width='100px')
)

password_input = widgets.Password(
    description='Пароль:',
    style=dict(description_width='100px')
)

query_input = widgets.Text(
    description='ID запроса/Ссылка:',
    placeholder='Введите идентификатор запроса',
    style=dict(description_width='100px')
)

file_upload = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Выберите файл:',
    layout=widgets.Layout(width='400px')
)

# Создание форм
digger_form = widgets.VBox([
    widgets.HTML(value='<h3>Авторизация в Digger</h3>'),
    login_input,
    password_input,
    query_input
])

file_form = widgets.VBox([
    widgets.HTML(value='<h3>Загрузка файла CSV</h3>'),
    file_upload,
    widgets.Output()
])

# Контейнер для карточек
cards_container = widgets.HBox([
    digger_card, file_card
], layout=widgets.Layout(
    justify_content='center',
    margin='20px 0px'
))

# Создаем кнопку загрузки
load_button = widgets.Button(
    description='Загрузить данные в калькулятор',
    icon='check',
    style=dict(button_color='#4CAF50', font_weight='bold'),
    layout=widgets.Layout(width='300px', margin='20px 0px')
)

# Создаем контейнер для вывода конфигурации
config_output = widgets.Output()

def update_card_styles():
    """Обновляет стили карточек"""
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

def on_load_button_click(b):
    """Обработчик нажатия кнопки загрузки"""
    with config_output:
        config_output.clear_output()
        print("Текущая конфигурация:")
        #Дебаг-функция для проверки конфигурации, к удалению
        print(get_data_fetch_config())

# Привязка обработчиков к кнопкам
digger_card.on_click(on_digger_click)
file_card.on_click(on_file_click)

# Привязываем обработчик к кнопке
load_button.on_click(on_load_button_click)

def get_data_fetch_config():
    """Возвращает текущую конфигурацию загрузки данных"""
    config = {
        'type': current_method
    }
    
    if current_method == 'digger':
        config.update({
            'auth_login': login_input.value,
            'auth_pass': password_input.value,
            'query_id': query_input.value,
            'csv_file': None
        })
    else:
        uploaded_files = list(file_upload.value.values())
        csv_content = uploaded_files[0]['content'] if uploaded_files else None
        
        config.update({
            'auth_login': None,
            'auth_pass': None,
            'query_id': None,
            'csv_file': csv_content
        })
    
    return config

def display_interface():
    """Отображает весь интерфейс"""
    display(cards_container)
    display(form_container)
    display(load_button)
    display(config_output)
    with form_container:
        display(digger_form)