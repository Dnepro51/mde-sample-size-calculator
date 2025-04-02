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
    #    'boxplot': {}}}


import Statistics.statistics as stats
import DataVisualizations.visualizations as vis

def eda_stats(series):
    # Получаем результаты статистических функций
    base_stats_result = stats.base_statistics(series)
    quantiles_result = stats.quantiles(series)

    return {
        'base_statistics': base_stats_result, 
        'quantiles': quantiles_result
    }

def eda_visualizations(series,pdf_df):
    # Получаем результаты визуализаций
    histogram_fig = vis.histogram(series)
    cdf_fig = vis.cdf(pdf_df)
    scatter_fig = vis.scatter_plot(series)
    boxplot_fig = vis.boxplot(series)

    return {
        'histogram': histogram_fig, 
        'cdf': cdf_fig, 
        'scatter_plot': scatter_fig, 
        'boxplot': boxplot_fig
    }

def EDA(series):
    stats_results = eda_stats(series)
    vis_results = eda_visualizations(series)

    return {
        'statistics': stats_results, 
        'visualizations': vis_results
    }


