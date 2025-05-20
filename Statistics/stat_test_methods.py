"""
Методы статистических тестов для калькулятора размера выборки (MDE)
===================================================================

Данный модуль реализует методы статистических тестов, применяемые в калькуляторе размера выборки для экспериментов с минимальным обнаруживаемым эффектом (MDE).

Возможности модуля:
- Реализация отдельных методов тестирования (t-тест, z-тест)
- Селектор функций для динамического выбора подходящего метода тестирования

Методы, реализованные в этом модуле, используются экспериментальным движком для определения, позволяет ли симулированный эксперимент обнаружить минимальный эффект при заданном размере выборки.

Интерфейс тестовой функции
--------------------------
Все тестовые функции следуют единому интерфейсу:

Args:
    control_sample (array-like): Данные выборки из контрольной группы
    experiment_sample (array-like): Данные выборки из экспериментальной группы с применённым эффектом (MDE)
    alpha (float): Уровень значимости для статистического теста (например, 0.05)

Returns:
    tuple: (p_value, is_significant)
        - p_value (float): P-значение из статистического теста
        - is_significant (bool): Является ли различие статистически значимым

Интеграция с движком экспериментов
---------------------------------
Основной движок экспериментов использует эти функции следующим образом:
1. Получает параметр test_method (например, "t_test") из конфигурационного файла (JSON)
2. Вызывает get_test_method(test_method) для получения нужной тестовой функции
3. В рамках каждой симуляции генерирует выборки и вызывает:
       p_value, is_significant = test_function(control_sample, experiment_sample, alpha)
4. Отслеживает долю симуляций, где is_significant=True, для расчёта мощности теста
"""

from scipy import stats


def t_test(control_sample, experiment_sample, alpha):
    """
    Выполняет t-test для сравнения средних значений двух выборок.
    
    Параметры:
    control_sample : numpy.ndarray
        Выборка контрольной группы из rv_discrete.sample().    
    experiment_sample : numpy.ndarray
        Выборка экспериментальной группы из rv_discrete.sample().
    alpha : float
        Уровень значимости.
    Возвращает:
    tuple
        (p_value, p_value < alpha)
    """
    from scipy import stats
    
    stat, p_value = stats.ttest_ind(control_sample, experiment_sample)
    
    return p_value, p_value < alpha

def z_proportion_test(control_sample, experiment_sample, alpha):
    """
    Выполняет z-test для сравнения двух пропорций.
    Параметры:
    control_sample : numpy.ndarray
        Выборка контрольной группы из rv_discrete.sample().
    experiment_sample : numpy.ndarray
        Выборка экспериментальной группы из rv_discrete.sample().
    alpha : float
        Уровень значимости.
    Возвращает:
    tuple
        (p_value, p_value < alpha)
    """
    import numpy as np
    from scipy import stats
    
    count1 = np.sum(control_sample)
    count2 = np.sum(experiment_sample)
    nobs1 = len(control_sample)
    nobs2 = len(experiment_sample)
    
    stat, p_value = stats.proportions_ztest([count1, count2], [nobs1, nobs2])
    
    return p_value, p_value < alpha


# Словарь доступных тестов
test_methods = {
    't_test': t_test,
    'z_proportion_test': z_proportion_test,
}

def get_test_method(method_name):
    return test_methods[method_name]