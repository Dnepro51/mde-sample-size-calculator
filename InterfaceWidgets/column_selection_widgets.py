import ipywidgets as widgets
import json
import os
from DataLoader.data_loader import load_data_from_digger
from IPython.display import display, clear_output
import time
import threading



def column_selection_widgets(data_dict, on_column_selected=None):
    """
    Args:
        data_dict: словарь с данными
        on_column_selected: функция обратного вызова, которая будет вызвана 
                          когда пользователь выберет колонку
    """
    print("Инициализация виджетов...")
    # print(f"Callback функция: {on_column_selected}")
    
    # Визуализация данных
    display(data_dict['df'].head())
    
    # Создание виджетов
    column_selector = widgets.Dropdown(
        options=data_dict['columns'],
        description='Выберите колонку для анализа:'
    )
    
    analyze_button = widgets.Button(
        description='Сконфигурировать дискретное распределение',
        icon='play',
        style=dict(button_color='#4CAF50', font_weight='bold'),
        layout=widgets.Layout(width='200px', margin='10px 0px')
    )
    
    # Создаем виджет Output для вывода результатов
    output = widgets.Output()
    
    # Обработка выбора
    def on_analyze_click(b):
        selected_column = column_selector.value
        with output:
            output.clear_output(wait=True)
            # Показываем только превью выбранной колонки, но не выводим текст о выборе
            display(data_dict['df'][selected_column].head())
        if on_column_selected:
            on_column_selected(selected_column, data_dict)
    
    # Привязываем обработчики
    analyze_button.on_click(on_analyze_click)
    
    # Отображение виджетов
    column_selection_container = widgets.VBox([column_selector, analyze_button, output])
    display(column_selection_container)
    
    
    
