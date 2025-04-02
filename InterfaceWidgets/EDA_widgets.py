# Этот виджет служит цели вывода результатов EDA
# В EDA будут входить:

    # Визуализации:
        # Гистограмма распределения значений
        # CDF (кумулятивная функция распределения)
        # Scatter plot из 10 тысяч сэмплированных точек
        # Boxplot

    # Статистики:
        # Базовые статистики (среднее, медиана, стандартное отклонение и пр.)
        # Квантили
        # Интерквартильный размах (IQR)


import EDA.EDA as eda
from IPython.display import display
import pandas as pd


def run_eda_analysis(selected_column, data_dict):
    """
    Запускает EDA анализ для выбранной колонки.
    
    Args:
        selected_column (str): Название выбранной колонки
        data_dict (dict): Словарь с данными, содержащий DataFrame в ключе 'df'
    """
    # Получаем данные для выбранной колонки
    series = data_dict['df'][selected_column]
    
    try:
        # Запускаем EDA анализ
        eda_results = eda.EDA(series)
        
        # Выводим статистики в виде датафреймов
        print("Base Statistics:")
        base_stats_df = pd.DataFrame([eda_results['statistics']['base_statistics']])
        display(base_stats_df)
        
        print("Quantiles:")
        quantiles_df = pd.DataFrame([eda_results['statistics']['quantiles']])
        display(quantiles_df)
        
        # Выводим графики вертикально друг под другом
        print("Visualizations:")
        for graph in eda_results['visualizations']['multiplot']:
            display(graph)
        
        return eda_results
        
    except Exception as e:
        print(f"Error during EDA analysis: {str(e)}")
        raise
