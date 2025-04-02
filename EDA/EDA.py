# Визуализации:
    # Гистограмма распределения значений
    # CDF (кумулятивная функция распределения)
    # Scatter plot из 10 тысяч сэмплированных точек
    # Boxplot

# Статистики:
    # Базовые статистики (среднее, медиана, стандартное отклонение и пр.)
    # Квантили
    # Интерквартильный размах (IQR)

# На вход модуль получает:
    # pd.Series (df['column_name'])

# На выходе:
    # {'statistics': 
    #   {'base_statistics': {}, 
    #    'quantiles': {}
    #  'visualizations': 
    #   {'histogram': {}, 
    #    'cdf': {}, 
    #    'scatter_plot': {}, 
    #    'boxplot': {},
    #    'multiplot': {}}}


import Statistics.statistics as stats
import DataVisualizations.visualizations as vis
from plotly.subplots import make_subplots


def create_multiplot(figures_dict):
    """
    Подготавливает графики для вертикального отображения.
    
    Args:
        figures_dict (dict): Словарь с графиками
        
    Returns:
        list: Список подготовленных графиков
    """
    # Задаем одинаковый размер для всех графиков
    for key in ['histogram', 'cdf', 'scatter_plot', 'boxplot']:
        figures_dict[key].update_layout(
            height=600,
            width=800,
            template='plotly_white'
        )
    
    # Обновляем названия графиков на английском
    figures_dict['histogram'].update_layout(
        title=f'Histogram (sample {figures_dict["histogram"].data[0].x.shape[0]})'
    )
    figures_dict['cdf'].update_layout(
        title='CDF'
    )
    figures_dict['scatter_plot'].update_layout(
        title=f'Scatterplot (sample {figures_dict["scatter_plot"].data[0].y.shape[0]})'
    )
    figures_dict['boxplot'].update_layout(
        title=f'Boxplot (sample {figures_dict["boxplot"].data[0].y.shape[0]})'
    )
    
    # Возвращаем список графиков для вертикального отображения
    return [
        figures_dict['histogram'],
        figures_dict['cdf'],
        figures_dict['scatter_plot'],
        figures_dict['boxplot']
    ]


def eda_stats(series):
    # Получаем результаты статистических функций
    base_stats_result = stats.base_statistics(series)
    quantiles_result = stats.quantiles(series)

    return {
        'base_statistics': base_stats_result, 
        'quantiles': quantiles_result
    }


def eda_visualizations(series, pdf_df):
    # Получаем результаты визуализаций
    histogram_fig = vis.histogram(series)
    cdf_fig = vis.cdf(pdf_df)
    scatter_fig = vis.scatter_plot(series)
    boxplot_fig = vis.boxplot(series)
    
    # Создаем словарь с графиками
    figures_dict = {
        'histogram': histogram_fig, 
        'cdf': cdf_fig, 
        'scatter_plot': scatter_fig, 
        'boxplot': boxplot_fig
    }
    
    # Добавляем мультиплот
    figures_dict['multiplot'] = create_multiplot(figures_dict)

    return figures_dict


def EDA(series):
    # Получаем PDF для CDF
    pdf_df = stats.pdf_creation(series)
    
    # Получаем статистики и визуализации
    stats_results = eda_stats(series)
    vis_results = eda_visualizations(series, pdf_df)

    return {
        'statistics': stats_results, 
        'visualizations': vis_results
    }


