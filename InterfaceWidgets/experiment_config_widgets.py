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

# MDE (минимальное различие, которое мы хотим обнаружить)
mde_input = widgets.BoundedFloatText(
    value=1.0,
    min=0.1,
    max=100.0,
    step=0.5,
    description='MDE:',
    style=dict(description_width='150px'),
    layout=widgets.Layout(width='250px')
)

# Подсказка для MDE
mde_helper = widgets.HTML(
    value='<span style="padding-left:5px; line-height:32px;">%</span>'
)

# Виджет для отображения рассчитанного нового среднего
calculated_mean_display = widgets.HTML(
    value='<span style="color:#4a6baf; padding-left:150px;">Новое среднее: <span id="new-mean-value">—</span></span>',
    layout=widgets.Layout(margin='5px 0px')
)

# Объединяем MDE и подсказку в один ряд
mde_container = widgets.HBox([mde_input, mde_helper])

# Контейнер для MDE ввода и отображения нового среднего
mde_with_mean_container = widgets.VBox([
    mde_container,
    calculated_mean_display
])

# Выбор статистики (пока только среднее)
statistic_dropdown = widgets.Dropdown(
    options=[('mean', 'mean')],
    value='mean',
    description='Статистика:',
    disabled=True,  # Отключаем, т.к. пока доступен только один вариант
    style=dict(description_width='150px')
)

# Выбор метода статистического теста
test_method_dropdown = widgets.Dropdown(
    options=[('T-test', 't_test'), ('Z-test', 'z_test')],
    value='t_test',
    description='Метод теста:',
    style=dict(description_width='150px')
)

# Число прогонов эмуляции (не более 10 000)
num_emulations_input = widgets.BoundedIntText(
    value=1000,
    min=100,
    max=10000,
    step=100,
    description='Число эмуляций:',
    style=dict(description_width='150px'),
    layout=widgets.Layout(width='300px')
)

# Стартовый размер выборки (по умолчанию 1000)
sample_size_input = widgets.IntText(
    value=1000,
    description='Размер выборки:',
    style=dict(description_width='150px'),
    layout=widgets.Layout(width='300px')
)

# Шаг увеличения размера выборки (по умолчанию 500)
sample_step_input = widgets.IntText(
    value=500,
    description='Шаг выборки:',
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
    mde_with_mean_container,
    statistic_dropdown,
    test_method_dropdown,
    num_emulations_input,
    sample_size_input,
    sample_step_input,
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
    # Получаем значение MDE
    mde_value = mde_input.value
    
    # Проверка и преобразование значений
    try:
        sample_size = int(sample_size_input.value)
        sample_step = int(sample_step_input.value)
    except (ValueError, TypeError):
        sample_size = 1000  # значение по умолчанию
        sample_step = 500   # значение по умолчанию
    
    config = {
        'alpha': alpha_dropdown.value,
        'target_power': target_power_input.value,
        'mde_percent': mde_value,
        'statistic': statistic_dropdown.value,
        'test_method': test_method_dropdown.value,
        'num_emulations': num_emulations_input.value,
        'sample_size': sample_size,
        'sample_step': sample_step
    }
    return config

# ============= Основная функция отображения =============
def display_experiment_config_interface(current_mean=None, on_config_created=None):
    """
    Отображает интерфейс конфигурации экспериментов.
    
    Args:
        current_mean (float): Текущее среднее значение из распределения
        on_config_created (callable): Функция обратного вызова, которая будет вызвана
                                     после создания конфигурации. Принимает словарь
                                     с созданной конфигурацией.
    """
    # Инициализируем отображение текущего среднего, если оно предоставлено
    if current_mean is not None:
        current_mean_formatted = round(current_mean, 4)
        calculated_mean_display.value = f'<span style="color:#4a6baf; padding-left:150px;">Текущее среднее: {current_mean_formatted} | Новое среднее: <span id="new-mean-value">{current_mean_formatted}</span></span>'
    
    # Функция для обновления отображения нового среднего значения
    def update_calculated_mean(change):
        if current_mean is not None:
            try:
                # Получаем текущее значение MDE в процентах
                mde_value = mde_input.value if mde_input.value is not None else 0
                
                # Вычисляем новое среднее значение (текущее * (1 + MDE/100))
                new_mean = current_mean * (1 + mde_value/100)
                
                # Округляем до 4 десятичных знаков
                new_mean_formatted = round(new_mean, 4)
                
                # Обновляем отображение
                calculated_mean_display.value = f'<span style="color:#4a6baf; padding-left:150px;">Текущее среднее: {current_mean_formatted} | Новое среднее: <span id="new-mean-value">{new_mean_formatted}</span></span>'
            except (ValueError, TypeError):
                # В случае ошибки, отображаем дефолтное значение
                calculated_mean_display.value = f'<span style="color:#4a6baf; padding-left:150px;">Текущее среднее: {current_mean_formatted} | Новое среднее: <span id="new-mean-value">—</span></span>'
    
    # Привязываем обработчик к изменению значения MDE
    mde_input.observe(update_calculated_mean, names='value')
    
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
        
        # Добавляем информацию о текущем и новом среднем значении, если доступно
        if current_mean is not None:
            try:
                mde_value = mde_input.value if mde_input.value is not None else 0
                new_mean = current_mean * (1 + mde_value/100)
                config['current_mean'] = current_mean
                config['new_mean'] = round(new_mean, 4)
            except (ValueError, TypeError):
                pass
        
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
    
    # Вызываем обновление среднего при инициализации
    if current_mean is not None:
        update_calculated_mean({'new': mde_input.value})
    
    # Отображение интерфейса
    display(config_container)