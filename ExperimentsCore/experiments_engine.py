"""
Движок экспериментов для расчета минимального размера выборки
============================================================

Данный модуль реализует основной движок для проведения экспериментов по определению
минимального размера выборки, необходимого для обнаружения заданного эффекта (MDE)
с заданной статистической мощностью.

Основные компоненты:
- Функция run_experiment: основной интерфейс для запуска экспериментов
- Внутренние функции для генерации выборок и оценки мощности

Взаимодействие с другими модулями:
1. Принимает дискретное распределение (rv_discrete) из experiments_core.py
2. Использует методы статистических тестов из Statistics/stat_test_methods.py
3. Использует методы добавления эффекта из Statistics/mde_add_methods.py
4. Принимает конфигурацию из InterfaceWidgets/experiment_config_widgets.py
5. Возвращает результаты для визуализации в DataVisualizations/

Пример использования:
    config = {
        'alpha': 0.05,
        'target_power': 0.8,
        'mde_percent': 5.0,
        'statistic': 'mean',
        'test_method': 't_test',
        'num_emulations': 1000,
        'sample_size': 1000,
        'sample_step': 500
    }
    results = run_experiment(rv_discrete, config)
"""

import numpy as np
import pandas as pd
from Statistics.stat_test_methods import get_test_method
from Statistics.mde_add_methods import get_effect_adder
import ipywidgets as widgets
from IPython.display import display, clear_output

def run_experiment(rv_discrete, config, on_progress_update=None):
    """
    Запускает эксперимент по определению минимального размера выборки.
    
    Параметры:
    rv_discrete : scipy.stats.rv_discrete
        Дискретное распределение для генерации выборок
    config : dict
        Конфигурация эксперимента
    on_progress_update : callable, optional
        Функция обратного вызова для обновления прогресса.
        Принимает параметры: (current_size, power, target_power, iteration, total_iterations)
        
    Возвращает:
    pd.DataFrame
        Результаты эксперимента с колонками:
        - sample_size: размер выборки
        - power: достигнутая мощность
    """
    alpha = config['alpha']
    target_power = config['target_power']
    mde_percent = config['mde_percent']
    statistic = config['statistic']
    test_method = config['test_method']
    num_emulations = config['num_emulations']
    sample_size = config['sample_size']
    sample_step = config['sample_step']

    # Максимальный размер выборки
    max_sample_size = 500000
    
    # Подготовка структуры для результатов
    results = {}  # sample_size -> power
    
    # Получаем функции для теста и добавления эффекта
    test_function = get_test_method(test_method)
    effect_adder = get_effect_adder(statistic)
    
    # Выводим информацию о начале эксперимента
    print(f"Запуск эксперимента с параметрами:")
    print(f"  Статистика: {statistic}")
    print(f"  Тест: {test_method}")
    print(f"  Alpha: {alpha}")
    print(f"  Целевая мощность: {target_power}")
    print(f"  MDE: {mde_percent}%")
    print(f"  Число эмуляций: {num_emulations}")
    print(f"  Начальный размер выборки: {sample_size}")
    print(f"  Шаг увеличения выборки: {sample_step}")
    
    # Внешний цикл - увеличение размера выборки
    current_size = sample_size
    sample_count = 0
    
    while current_size <= max_sample_size:
        print(f"\nТестируем размер выборки: {current_size}")
        
        # Внутренний цикл - эмуляции для текущего размера
        successful_tests = 0
        
        # Отображаем прогресс через каждые 10% эмуляций
        progress_step = max(1, num_emulations // 10)
        
        for i in range(num_emulations):
            # Генерация выборок
            control_sample = rv_discrete.rvs(size=current_size)
            experiment_sample = effect_adder(control_sample, mde_percent)
            
            # Проведение теста
            _, is_significant = test_function(control_sample, experiment_sample, alpha)
            if is_significant:
                successful_tests += 1
                
            # Отображение прогресса внутреннего цикла
            if (i + 1) % progress_step == 0 or i + 1 == num_emulations:
                percent_done = (i + 1) / num_emulations * 100
                print(f"  Прогресс: {i + 1}/{num_emulations} эмуляций ({percent_done:.1f}%)", end="\r")
        
        # Расчет мощности для текущего размера
        power = successful_tests / num_emulations
        results[current_size] = power
        
        # Выводим результат текущего размера выборки
        print(f"\n  Результат: Мощность {power:.4f} при размере выборки {current_size}")
        
        # Обновляем прогресс через callback, если он предоставлен
        sample_count += 1
        if on_progress_update:
            on_progress_update(current_size, power, target_power, sample_count, 
                              (max_sample_size - sample_size) // sample_step + 1)
        
        # Проверка достижения целевой мощности
        if power >= target_power:
            print(f"\nДостигнута целевая мощность {target_power}!")
            break
            
        # Увеличение размера выборки
        current_size += sample_step
    
    # Создание DataFrame из результатов
    df_results = pd.DataFrame({
        'sample_size': list(results.keys()),
        'power': list(results.values())
    })
    
    print("\nЭксперимент завершен!")
    if power >= target_power:
        print(f"Минимальный размер выборки для достижения мощности {target_power}: {current_size}")
    else:
        print(f"Целевая мощность {target_power} не достигнута даже при максимальном размере выборки {max_sample_size}")
    
    return df_results
