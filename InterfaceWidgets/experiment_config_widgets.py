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

# Виджет для отображения рассчитанной статистики
calculated_stat_display = widgets.HTML(
    value='<span style="color:#4a6baf; padding-left:150px;">Текущая статистика: — | Новая статистика: —</span>',
    layout=widgets.Layout(margin='5px 0px')
)

# Объединяем MDE и подсказку в один ряд
mde_container = widgets.HBox([mde_input, mde_helper])

# Контейнер для MDE ввода и отображения новой статистики
mde_with_stat_container = widgets.VBox([
    mde_container,
    calculated_stat_display
])

# Выбор статистики (подготовлено для расширения)
statistic_dropdown = widgets.Dropdown(
    options=[('Среднее', 'mean')],  # В будущем: [('Среднее', 'mean'), ('Медиана', 'median'), ...] 
    value='mean',
    description='Статистика:',
    disabled=False,  # Пока отключаем, т.к. пока доступен только один вариант
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
    mde_with_stat_container,
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
def display_experiment_config_interface(current_statistics=None, on_config_created=None):
    """
    Отображает интерфейс конфигурации экспериментов.
    
    Args:
        current_statistics (dict): Словарь с текущими статистиками распределения
                                 (ключи: 'mean', 'median', и т.д.)
        on_config_created (callable): Функция обратного вызова, которая будет вызвана
                                     после создания конфигурации.
    """
    # Если statistic_dropdown имеет пустое значение, устанавливаем его на mean
    if not statistic_dropdown.value:
        statistic_dropdown.value = 'mean'
        
    # Создадим словарь с переводами статистик для отображения
    stat_translations = {
        'mean': 'Среднее',
        'median': 'Медиана',
        'quantile': 'Квантиль',
        'proportion': 'Доля'
    }
    
    # Если статистики не предоставлены, создаем пустой словарь
    if current_statistics is None:
        current_statistics = {}
    
    # Функция для расчета новой статистики на основе MDE и текущей статистики
    def calculate_new_statistic(stat_type, mde_percent, current_value):
        """
        Рассчитывает новое значение статистики на основе MDE и текущего значения.
        
        Args:
            stat_type (str): Тип статистики ('mean', 'median', и т.д.)
            mde_percent (float): Процент MDE
            current_value (float): Текущее значение статистики
            
        Returns:
            float: Новое значение статистики
        """
        # В зависимости от типа статистики, применяем соответствующую формулу
        if stat_type == 'mean':
            # Для среднего: увеличиваем на процент MDE
            return current_value * (1 + mde_percent/100)
        elif stat_type == 'median':
            # Для медианы: пока используем такую же формулу, как для среднего
            # В будущем здесь может быть другая логика
            return current_value * (1 + mde_percent/100)
        elif stat_type == 'quantile':
            # Для квантиля: пока используем такую же формулу, как для среднего
            # В будущем здесь может быть другая логика
            return current_value * (1 + mde_percent/100)
        elif stat_type == 'proportion':
            # Для доли: увеличиваем абсолютно на MDE/100, но не более 1
            return min(current_value + mde_percent/100, 1.0)
        else:
            # По умолчанию возвращаем текущее значение
            return current_value
    
    # Функция для обновления отображения текущей и новой статистики
    def update_calculated_stat(change=None):
        # Получаем текущий тип статистики
        stat_type = statistic_dropdown.value
        stat_name = stat_translations.get(stat_type, stat_type.capitalize())
        
        # Проверяем, есть ли текущее значение для выбранного типа статистики
        if stat_type in current_statistics and current_statistics[stat_type] is not None:
            current_value = current_statistics[stat_type]
            current_formatted = round(current_value, 4)
            
            try:
                # Получаем текущее значение MDE в процентах
                mde_value = mde_input.value if mde_input.value is not None else 0
                
                # Вычисляем новое значение статистики
                new_value = calculate_new_statistic(stat_type, mde_value, current_value)
                
                # Округляем до 4 десятичных знаков
                new_formatted = round(new_value, 4)
                
                # Обновляем отображение
                calculated_stat_display.value = f'<span style="color:#4a6baf; padding-left:150px;">Текущее {stat_name.lower()}: {current_formatted} | Новое {stat_name.lower()}: <span id="new-stat-value">{new_formatted}</span></span>'
            except (ValueError, TypeError):
                # В случае ошибки, отображаем только текущее значение
                calculated_stat_display.value = f'<span style="color:#4a6baf; padding-left:150px;">Текущее {stat_name.lower()}: {current_formatted} | Новое {stat_name.lower()}: <span id="new-stat-value">—</span></span>'
        else:
            # Если нет текущего значения, отображаем сообщение о недоступности статистики
            calculated_stat_display.value = f'<span style="color:#4a6baf; padding-left:150px;">{stat_name} недоступно для данного распределения</span>'
    
    # Привязываем обработчик к изменению значения MDE
    mde_input.observe(update_calculated_stat, names='value')
    
    # Привязываем обработчик к изменению типа статистики
    statistic_dropdown.observe(update_calculated_stat, names='value')
    
    # Определяем обработчик нажатия кнопки
    def on_run_emulation_button_click(b):
        """
        Обработчик нажатия кнопки запуска эмуляции.
        Собирает конфигурацию и отображает её в формате JSON.
        """
        # Получаем текущую конфигурацию
        config = get_current_config()
        
        # Получаем текущий тип статистики
        stat_type = statistic_dropdown.value
        
        # Добавляем информацию о текущей и новой статистике, если доступно
        if stat_type in current_statistics and current_statistics[stat_type] is not None:
            try:
                mde_value = mde_input.value if mde_input.value is not None else 0
                current_value = current_statistics[stat_type]
                new_value = calculate_new_statistic(stat_type, mde_value, current_value)
                
                # Добавляем в конфигурацию
                config['statistic_type'] = stat_type
                config['current_statistic'] = current_value
                config['new_statistic'] = round(new_value, 4)
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
    
    # Вызываем обновление статистики при инициализации
    update_calculated_stat()
    
    # Отображение интерфейса
    display(config_container)