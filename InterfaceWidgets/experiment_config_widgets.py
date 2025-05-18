import ipywidgets as widgets
from IPython.display import display, clear_output
import json

# ============= Создание виджетов для конфигурации =============
# Заголовок интерфейса
config_header = widgets.HTML(value='<h3>Конфигурация эмуляции экспериментов</h3>')

# Альфа для статистического метода (уровень значимости)
alpha_dropdown = widgets.Dropdown(
    options=[0.01, 0.05, 0.1],
    value=0.05,
    description='Alpha:',
    style=dict(description_width='100px')
)

# Целевая мощность (вероятность отклонить нулевую гипотезу, если она фактически ложна)
target_power_input = widgets.BoundedFloatText(
    value=0.8,
    min=0.01,
    max=0.99,
    step=0.01,
    description='Целевая мощность:',
    style=dict(description_width='150px'),
    layout=widgets.Layout(width='300px')
)

# Кнопка для запуска эмуляции
run_emulation_button = widgets.Button(
    description='Запустить эмуляцию',
    icon='play',
    style=dict(button_color='#4CAF50', font_weight='bold'),
    layout=widgets.Layout(width='200px', margin='20px 0px 10px 0px')
)

# ============= Создание виджета вывода для отображения JSON =============
config_output = widgets.Output(
    layout=widgets.Layout(
        border='1px solid #ddd',
        padding='10px',
        max_height='300px',
        overflow='auto',
        margin='10px 0px'
    )
)

# ============= Создание контейнера для интерфейса =============
config_container = widgets.VBox([
    config_header,
    alpha_dropdown,
    target_power_input,
    # Другие виджеты будут добавлены позже
    run_emulation_button,
    config_output
])

# ============= Функция для сбора и отображения конфигурации =============
def get_current_config():
    """
    Собирает текущую конфигурацию из всех виджетов.
    
    Returns:
        dict: Словарь с конфигурацией эксперимента
    """
    config = {
        'alpha': alpha_dropdown.value,
        'target_power': target_power_input.value,
        # Другие параметры будут добавлены позже
    }
    return config

# ============= Основная функция отображения =============
def display_experiment_config_interface(on_config_created=None):
    """
    Отображает интерфейс конфигурации экспериментов.
    
    Args:
        on_config_created (callable): Функция обратного вызова, которая будет вызвана
                                     после создания конфигурации. Принимает словарь
                                     с созданной конфигурацией.
    """
    # Определяем обработчик нажатия кнопки внутри функции, чтобы он имел доступ к on_config_created
    def on_run_emulation_button_click(b):
        """
        Обработчик нажатия кнопки запуска эмуляции.
        Собирает конфигурацию и отображает её в формате JSON.
        
        Args:
            b: Кнопка, на которую нажали (не используется)
        """
        # Получаем текущую конфигурацию
        config = get_current_config()
        
        # Отображаем конфигурацию в формате JSON
        with config_output:
            config_output.clear_output(wait=True)
            # Выводим чистый JSON без форматирования
            print(json.dumps(config))
        
        # Если есть функция обратного вызова, вызываем её с текущей конфигурацией
        if on_config_created:
            on_config_created(config)
    
    # Привязываем обработчик к кнопке
    run_emulation_button.on_click(on_run_emulation_button_click)
    
    # Отображение интерфейса
    display(config_container)