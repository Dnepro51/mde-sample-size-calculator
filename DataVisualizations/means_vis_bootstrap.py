import numpy as np
import plotly.graph_objects as go
from Statistics.mde_add_methods import get_effect_adder

def visualize_means_distribution(rv_discrete, sample_size, mde_percent, statistic='mean', n_bootstraps=5000):
    effect_adder = get_effect_adder(statistic)
    
    means_control = []
    means_experiment = []
    
    for _ in range(n_bootstraps):
        # Генерация контрольной выборки
        control_sample = rv_discrete.rvs(size=sample_size)
        
        # Генерация экспериментальной выборки с добавлением эффекта
        experiment_sample = effect_adder(control_sample, mde_percent)
        
        # Расчет средних
        means_control.append(np.mean(control_sample))
        means_experiment.append(np.mean(experiment_sample))
    
    # Создание визуализации - двух гистограмм на одном графике
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=means_control,
        opacity=0.7,
        name='Контрольная группа',
        marker=dict(color='blue'),
        nbinsx=30
    ))
    
    fig.add_trace(go.Histogram(
        x=means_experiment,
        opacity=0.7,
        name='Экспериментальная группа (с MDE)',
        marker=dict(color='red'),
        nbinsx=30
    ))
    
    fig.update_layout(
        title=f'Распределение средних (размер выборки: {sample_size}, MDE: {mde_percent}%)',
        xaxis_title='Среднее значение',
        yaxis_title='Частота',
        barmode='overlay'
    )
    
    return fig