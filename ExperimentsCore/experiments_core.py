import numpy as np
import pandas as pd
from scipy import stats

def discrete_dist_creation(series, round_digits=None, adaptive_rounding=True):
    """
    Создает дискретное распределение для числового ряда с адаптивным округлением.
    
    Args:
        series (pd.Series): Входной числовой ряд
        round_digits (int, optional): Количество знаков после запятой для округления.
                                    Если None и adaptive_rounding=True, будет выбрано автоматически.
        adaptive_rounding (bool): Использовать ли адаптивное округление
        
    Returns:
        tuple: (rv_discrete, df_dist, round_digits), где
            rv_discrete - объект с дискретным распределением
            df_dist - DataFrame с значениями и их вероятностями
            round_digits - использованное значение округления
    """
    # Очищаем данные от пропущенных значений
    data = series.dropna()
    
    # Определяем количество знаков для округления
    if adaptive_rounding and round_digits is None:
        # Получаем стандартное отклонение данных
        std_dev = np.std(data)
        
        # Защита от нулевого стандартного отклонения
        if std_dev == 0:
            round_digits = 2  # Значение по умолчанию
        else:
            # Расчёт оптимального числа знаков на основе стандартного отклонения
            round_digits = max(0, -int(np.floor(np.log10(std_dev))) + 2)
            
            # Ограничение максимального количества знаков для практичности
            round_digits = min(round_digits, 6)
    elif round_digits is None:
        round_digits = 2  # Значение по умолчанию
    
    # Округляем значения
    rounded_data = np.round(data, round_digits)
    
    # Подсчитываем частоты округленных значений
    value_counts = pd.Series(rounded_data).value_counts(normalize=True).sort_index()
    
    # Преобразуем в массивы значений и вероятностей
    xk = value_counts.index.values
    pk = value_counts.values
    
    # Создаем дискретное распределение
    rv = stats.rv_discrete(values=(xk, pk))
    
    # Создаем DataFrame для удобства просмотра
    df_dist = pd.DataFrame({
        'value': xk,
        'probability': pk,
        'cumulative_probability': np.cumsum(pk)
    })
    
    return rv, df_dist, round_digits  # Возвращаем также использованное округление