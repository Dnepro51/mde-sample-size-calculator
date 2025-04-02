import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def histogram(series, sample_size=10000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=sample,
        name='Гистограмма распределения метрики',
        nbinsx=100
    ))
    
    fig.update_layout(
        title='Гистограмма распределения',
        xaxis_title='Значения',
        yaxis_title='Количество',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def cdf(pdf_df):
    """
    Создает график кумулятивной функции распределения на основе PDF.
    
    Args:
        pdf_df (pd.DataFrame): DataFrame с колонками 'x' и 'density' из функции pdf_creation
        
    Returns:
        go.Figure: График CDF
    """
    # Вычисляем CDF через интеграл от PDF
    cdf_values = np.cumsum(pdf_df['density']) * (pdf_df['x'].iloc[1] - pdf_df['x'].iloc[0])
    cdf_values = cdf_values / cdf_values.max()  # Нормализуем
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pdf_df['x'],
        y=cdf_values,
        mode='lines',
        name='CDF',
        line=dict(width=2)
    ))
    
    fig.update_layout(
        title='Кумулятивная функция распределения',
        xaxis_title='Значения',
        yaxis_title='Вероятность',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def scatter_plot(series, sample_size=10000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=np.arange(len(sample)),
        y=sample,
        mode='markers',
        name='Точечный график',
        marker=dict(
            size=4,
            opacity=0.6
        )
    ))
    
    fig.update_layout(
        title='Точечный график',
        xaxis_title='Индекс',
        yaxis_title='Значения',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def boxplot(series, sample_size=2000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=sample,
        name='Boxplot',
        boxpoints='outliers'
    ))
    
    fig.update_layout(
        title='Ящик с усами',
        yaxis_title='Значения',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig




