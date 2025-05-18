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
from IPython.display import display, clear_output
import pandas as pd
import ipywidgets as widgets
import plotly.graph_objects as go


def run_eda_analysis(selected_column, data_dict, on_eda_complete=None):
    """
    Запускает EDA анализ для выбранной колонки.
    
    Args:
        selected_column (str): Название выбранной колонки
        data_dict (dict): Словарь с данными, содержащий DataFrame в ключе 'df'
        on_eda_complete (callable): Функция обратного вызова после завершения EDA
    """
    # Получаем данные для выбранной колонки
    series = data_dict['df'][selected_column]
    
    # Создаем виджеты Output для статистик
    stats_output = widgets.Output()
    display(stats_output)
    
    # Создаем виджет Output для визуализаций
    vis_output = widgets.Output()
    display(vis_output)
    
    try:
        # Запускаем EDA анализ
        eda_results = eda.EDA(series)
        
        # Выводим статистики в виде датафреймов
        with stats_output:
            print("Base Statistics:")
            base_stats_df = pd.DataFrame([eda_results['statistics']['base_statistics']])
            display(base_stats_df)
            
            print("Quantiles:")
            quantiles_df = pd.DataFrame([eda_results['statistics']['quantiles']])
            display(quantiles_df)
        
        # Выводим метку "Visualizations:" в виджет
        with vis_output:
            print("Visualizations:")
        
        try:
            # Получаем только гистограмму (первый график)
            histogram_fig = eda_results['visualizations']['multiplot'][0]
            
            # Преобразуем обычную фигуру в FigureWidget
            fig_data = histogram_fig.data
            fig_layout = histogram_fig.layout
            
            # Создаем FigureWidget с теми же данными и макетом
            figure_widget = go.FigureWidget(data=fig_data, layout=fig_layout)
            
            # Отображаем FigureWidget напрямую (он сам является виджетом)
            display(figure_widget)
            
        except Exception as e:
            print(f"Ошибка при отображении гистограммы: {str(e)}")
        
        # Преобразуем и выводим остальные графики как FigureWidget
        for i, graph in enumerate(eda_results['visualizations']['multiplot']):
            if i > 0:  # Пропускаем гистограмму, она уже отображена
                # Преобразуем обычную фигуру в FigureWidget
                fig_data = graph.data
                fig_layout = graph.layout
                
                # Создаем FigureWidget с теми же данными и макетом
                figure_widget = go.FigureWidget(data=fig_data, layout=fig_layout)
                
                # Отображаем FigureWidget напрямую
                display(figure_widget)
                
        # Отображаем виджет для информации о распределении после всех графиков
        # Получаем доступ к distribution_info_output из родительского модуля
        import sys
        distribution_info_output = None
        for module in sys.modules.values():
            if hasattr(module, 'distribution_info_output'):
                distribution_info_output = module.distribution_info_output
                break
        
        # Отображаем виджет только если нашли его
        if distribution_info_output:
            display(distribution_info_output)

        if on_eda_complete:
            on_eda_complete()
        
        return eda_results
    
        
    except Exception as e:
        print(f"Error during EDA analysis: {str(e)}")
        raise
