import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def histogram(series, sample_size=10000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True, random_state=42)
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=sample,
        name='Distribution Histogram',
        nbinsx=100
    ))
    
    fig.update_layout(
        title=f'Histogram (sample {sample_size})',
        xaxis_title='Values',
        yaxis_title='Count',
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
        title='CDF',
        xaxis_title='Values',
        yaxis_title='Probability',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def scatter_plot(series, sample_size=10000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True, random_state=42)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=np.arange(len(sample)),
        y=sample,
        mode='markers',
        name='Scatter Plot',
        marker=dict(
            size=4,
            opacity=0.6
        )
    ))
    
    fig.update_layout(
        title=f'Scatterplot (sample {sample_size})',
        xaxis_title='Index',
        yaxis_title='Values',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def boxplot(series, sample_size=10000):
    # Сэмплируем объекты
    sample = series.sample(n=sample_size, replace=True, random_state=42)
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=sample,
        name='Boxplot',
        boxpoints='outliers'
    ))
    
    fig.update_layout(
        title=f'Boxplot (sample {sample_size})',
        yaxis_title='Values',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig




