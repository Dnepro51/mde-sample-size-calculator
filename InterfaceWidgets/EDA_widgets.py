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


def run_eda_analysis(selected_column, data_dict, parent_container=None, on_eda_complete=None):
    """
    Запускает EDA анализ для выбранной колонки.
    
    Args:
        selected_column (str): Название выбранной колонки
        data_dict (dict): Словарь с данными, содержащий DataFrame в ключе 'df'
        parent_container: Родительский контейнер для добавления виджетов
        on_eda_complete (callable): Функция обратного вызова после завершения EDA
    """
    # Получаем данные для выбранной колонки
    series = data_dict['df'][selected_column]
    
    # Создаем контейнер для EDA если не предоставлен родительский
    if parent_container is None:
        eda_container = widgets.VBox()
        display(eda_container)
    else:
        # Создаем новый контейнер для EDA анализа
        eda_container = widgets.VBox()
        
        # Добавляем его в родительский контейнер
        if eda_container not in parent_container.children:
            parent_container.children = list(parent_container.children) + [eda_container]
    
    # Создаем заголовок для EDA
    eda_header = widgets.HTML(f"<h3>EDA анализ для колонки: {selected_column}</h3>")
    
    # Добавляем заголовок в контейнер
    eda_container.children = [eda_header]
    
    try:
        # Запускаем EDA анализ
        eda_results = eda.EDA(series)
        
        # Создаем секцию для статистик
        stats_header = widgets.HTML("<h4>Базовые статистики</h4>")
        base_stats_df = pd.DataFrame([eda_results['statistics']['base_statistics']])
        base_stats_html = widgets.HTML(base_stats_df.to_html())
        
        # Добавляем квантили
        quantiles_header = widgets.HTML("<h4>Квантили</h4>")
        quantiles_df = pd.DataFrame([eda_results['statistics']['quantiles']])
        quantiles_html = widgets.HTML(quantiles_df.to_html())
        
        # Добавляем статистики в контейнер
        eda_container.children = list(eda_container.children) + [
            stats_header,
            base_stats_html,
            quantiles_header,
            quantiles_html
        ]
        
        # Добавляем заголовок для визуализаций
        vis_header = widgets.HTML("<h4>Визуализации</h4>")
        eda_container.children = list(eda_container.children) + [vis_header]
        
        try:
            # Обрабатываем все графики
            for i, graph in enumerate(eda_results['visualizations']['multiplot']):
                try:
                    # Преобразуем обычную фигуру в FigureWidget
                    fig_data = graph.data
                    fig_layout = graph.layout
                    
                    # Создаем FigureWidget с теми же данными и макетом
                    figure_widget = go.FigureWidget(data=fig_data, layout=fig_layout)
                    
                    # Добавляем виджет в контейнер EDA
                    eda_container.children = list(eda_container.children) + [figure_widget]
                except Exception as e:
                    # В случае ошибки с графиком, создаем сообщение об ошибке
                    error_widget = widgets.HTML(f"<span style='color:red'>Ошибка при создании графика {i}: {str(e)}</span>")
                    eda_container.children = list(eda_container.children) + [error_widget]
        except Exception as e:
            error_widget = widgets.HTML(f"<span style='color:red'>Ошибка при обработке визуализаций: {str(e)}</span>")
            eda_container.children = list(eda_container.children) + [error_widget]
                
        # Вызываем callback после завершения EDA если он предоставлен
        if on_eda_complete:
            on_eda_complete()
        
        return eda_results
            
    except Exception as e:
        # В случае общей ошибки, добавляем сообщение об ошибке в контейнер
        error_widget = widgets.HTML(f"<span style='color:red'>Ошибка при анализе EDA: {str(e)}</span>")
        eda_container.children = list(eda_container.children) + [error_widget]
