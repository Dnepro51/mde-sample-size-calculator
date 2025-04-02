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
    # Визуализации
    # Статистики

def eda_stats(series):
    # Получаем результаты статистических функций
    base_stats_result = base_statistics(series)
    quantiles_result = quantiles(series)
    iqr_result = iqr(series)

    return {
        'base_statistics': base_stats_result, 
        'quantiles': quantiles_result, 
        'iqr': iqr_result
    }

def eda_visualizations(series):
    # Получаем результаты визуализаций
    histogram_fig = histogram(series)
    cdf_fig = cdf(series)
    scatter_fig = scatter_plot(series)
    boxplot_fig = boxplot(series)

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


