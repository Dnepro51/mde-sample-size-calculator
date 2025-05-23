# Калькулятор размера выборки для MDE

Инструмент для расчета минимального размера выборки на основе эмуляции статистических экспериментов с заданной мощностью.

## Возможности

- Загрузка данных из Digger
- Визуализация и расчет базовых статистик (eda-визуализации и df с параметрами)
- Эмуляция экспериментов для расчета минимального размера выборки (т-тест на основе rvs discrete)
- Визуализация мощности в зависимости от размера выборки (plotly)
- Интерактивный интерфейс на базе ipywidgets

## TODO

1. **Загрузка данных из csv**

2. **Новые статистические тесты**
   - z-prop-тест с аналитической формулой
   - Аналитический калькулятор z-теста в интерфейсе
   - Efron bootstrap для различных статистик

3. **Модификация распределений**
   - Exponential tilt для RVS-объекта (модификация вероятностей, а не значений)

4. **Расширение набора метрик**
   - Квантили с разными уровнями
   - Метрики вариации и разброса

5. **Оптимизация производительности**
   - Интеграция с Polars для ускорения вычислений
   - Параллелизация симуляций
