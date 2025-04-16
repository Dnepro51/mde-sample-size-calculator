import pandas as pd
import numpy as np
from scipy import stats


def base_statistics(series):
    """
    Вычисляет основные статистические показатели для числового ряда.
    
    Args:
        series (pd.Series): Входной числовой ряд
        
    Returns:
        dict: Словарь с основными статистическими показателями
    """
    return {
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'var': series.var(),
        'skewness': series.skew(),
        'kurtosis': series.kurt()
    }


def quantiles(series):
    """
    Вычисляет квантили и размах для числового ряда.
    
    Args:
        series (pd.Series): Входной числовой ряд
        
    Returns:
        dict: Словарь с квантилями и размахом
    """
    return {
        'min': series.min(),
        'max': series.max(),
        'q5%': series.quantile(0.05),
        'q1': series.quantile(0.25),
        'q2': series.quantile(0.5),
        'q3': series.quantile(0.75),
        'q95%': series.quantile(0.95),
        'iqr': series.quantile(0.75) - series.quantile(0.25)
    }


def pdf_creation(series, n_points=100):
    """
    Создает оценку функции плотности вероятности (PDF) для числового ряда.
    
    Args:
        series (pd.Series): Входной числовой ряд
        n_points (int): Количество точек для построения PDF
        
    Returns:
        pd.DataFrame: DataFrame с колонками 'x' и 'density' для построения PDF
    """
    # Очищаем данные от пропущенных значений
    data = series.dropna()
    
    # Создаем точки для построения PDF
    x = np.linspace(data.min(), data.max(), n_points)
    
    # Оцениваем плотность вероятности с помощью kernel density estimation
    kde = stats.gaussian_kde(data)
    y = kde(x)
    
    # Создаем DataFrame
    df = pd.DataFrame({
        'x': x,
        'density': y
    })
    
    return df
