import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

plt.style.use('seaborn-v0_8')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Ищем CSV файл в текущей директории
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

if not csv_files:
    for f in os.listdir('.'):
        print(f"  - {f}")
    exit()
target_file = 'sales_data_2000.csv' if 'sales_data_2000.csv' in csv_files else csv_files[0]

# Загружаем данные
try:
    df = pd.read_csv(target_file)
except Exception as e:
    print(f"Ошибка загрузки: {e}")
    exit()

# Базовая информация
print(f"КОЛОНКИ И ТИПЫ ДАННЫХ:")
for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
    non_null = df[col].count()
    total = len(df)
    null_percent = ((total - non_null) / total * 100)
    print(f"{i:2}. {col:25} | {str(dtype):10} | {non_null:5} не-NULL | {null_percent:5.1f}% NULL")

print(f"ПЕРВЫЕ 10 СТРОК:")
print(df.head(10))

print(f"ОСНОВНЫЕ СТАТИСТИКИ:")
print(df.describe())

# Анализ пропущенных значений
print(f"ПРОПУЩЕННЫЕ ЗНАЧЕНИЯ:")
missing = df.isnull().sum()
if missing.sum() > 0:
    missing_df = pd.DataFrame({
        'Колонка': missing.index,
        'Пропущено': missing.values,
        'Процент': (missing.values / len(df) * 100).round(1)
    })
    missing_df = missing_df[missing_df['Пропущено'] > 0]
    print(missing_df.to_string(index=False))
else:
    print("Нет пропущенных значений")

print("ВИЗУАЛИЗАЦИЯ ДАННЫХ")

# Создаем графики
fig = plt.figure(figsize=(18, 12))

# 1. Гистограммы для числовых колонок
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    print(f"Числовые колонки для анализа: {list(numeric_cols)}")
    
    # Показываем до 4 числовых колонок
    for idx, col in enumerate(numeric_cols[:4], 1):
        ax = plt.subplot(2, 4, idx)
        ax.hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='skyblue')
        ax.set_title(f'Распределение: {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Частота')
        ax.grid(True, alpha=0.3)
        
        # Добавляем среднее и медиану
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Среднее: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'Медиана: {median_val:.2f}')
        ax.legend(fontsize=8)

# 2. Boxplot для выявления выбросов
if len(numeric_cols) > 0:
    ax_box = plt.subplot(2, 4, 5)
    data_to_plot = [df[col].dropna() for col in numeric_cols[:4] if len(df[col].dropna()) > 0]
    if data_to_plot:
        ax_box.boxplot(data_to_plot, labels=numeric_cols[:len(data_to_plot)])
        ax_box.set_title('Boxplot (выбросы)')
        ax_box.set_ylabel('Значения')
        ax_box.grid(True, alpha=0.3)
        plt.setp(ax_box.get_xticklabels(), rotation=45)

# 3. Матрица корреляций
if len(numeric_cols) >= 2:
    ax_corr = plt.subplot(2, 4, 6)
    corr_matrix = df[numeric_cols].corr()
    im = ax_corr.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax_corr.set_title('Матрица корреляций')
    ax_corr.set_xticks(range(len(numeric_cols)))
    ax_corr.set_yticks(range(len(numeric_cols)))
    ax_corr.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=8)
    ax_corr.set_yticklabels(numeric_cols, fontsize=8)
    plt.colorbar(im, ax=ax_corr)
    
    # Добавляем значения корреляций
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            text = ax_corr.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=7)

# 4. Scatter plot для двух самых коррелированных колонок
if len(numeric_cols) >= 2:
    # Находим две самые коррелированные колонки
    corr_values = []
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            corr = abs(df[col1].corr(df[col2]))
            corr_values.append((corr, col1, col2))
    
    if corr_values:
        corr_values.sort(reverse=True)
        best_corr, col1, col2 = corr_values[0]
        
        ax_scatter = plt.subplot(2, 4, 7)
        scatter = ax_scatter.scatter(df[col1], df[col2], alpha=0.5, s=20, color='purple')
        ax_scatter.set_xlabel(col1)
        ax_scatter.set_ylabel(col2)
        ax_scatter.set_title(f'{col1} vs {col2}\nКорреляция: {best_corr:.3f}')
        ax_scatter.grid(True, alpha=0.3)

# 5. Анализ категориальных данных
cat_cols = df.select_dtypes(include=['object']).columns
if len(cat_cols) > 0:
    print(f"Категориальные колонки: {list(cat_cols)}")
    
    # Берем первую категориальную колонку
    cat_col = cat_cols[0]
    ax_pie = plt.subplot(2, 4, 8)
    
    value_counts = df[cat_col].value_counts().head(10)  # Топ-10 категорий
    if len(value_counts) > 0:
        ax_pie.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax_pie.set_title(f'Топ-10 категорий: {cat_col}')
    else:
        ax_pie.text(0.5, 0.5, 'Нет данных', ha='center', va='center')
        ax_pie.set_title(f'Категории: {cat_col}')

plt.tight_layout()
plt.show()

# Дополнительный анализ временных рядов (если есть даты)
date_cols = []
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower() or 'год' in col.lower() or 'месяц' in col.lower():
        date_cols.append(col)

if date_cols:
    print("АНАЛИЗ ВРЕМЕННЫХ РЯДОВ")
    
    date_col = date_cols[0]
    print(f"Найдена колонка с датой/временем: {date_col}")
    
    try:
        # Пытаемся преобразовать в datetime
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        if df[date_col].notna().sum() > 0:
            # Сортируем по дате
            df_sorted = df.sort_values(date_col).dropna(subset=[date_col])
            
            # Ищем числовую колонку для анализа
            num_col_for_time = None
            for col in numeric_cols:
                if col != date_col:
                    num_col_for_time = col
                    break
            
            if num_col_for_time:
                fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
                
                # График временного ряда
                ax1.plot(df_sorted[date_col], df_sorted[num_col_for_time], 
                        marker='o', markersize=3, linewidth=1, alpha=0.7)
                ax1.set_xlabel('Дата')
                ax1.set_ylabel(num_col_for_time)
                ax1.set_title(f'Временной ряд: {num_col_for_time} по времени')
                ax1.grid(True, alpha=0.3)
                plt.setp(ax1.get_xticklabels(), rotation=45)
                
                # Месячный тренд
                df_sorted['month'] = df_sorted[date_col].dt.month
                monthly_avg = df_sorted.groupby('month')[num_col_for_time].mean()
                
                ax2.bar(monthly_avg.index, monthly_avg.values, color='orange', alpha=0.7)
                ax2.set_xlabel('Месяц')
                ax2.set_ylabel(f'Среднее {num_col_for_time}')
                ax2.set_title(f'Средние значения по месяцам: {num_col_for_time}')
                ax2.set_xticks(range(1, 13))
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.show()
    except:
        print("Не удалось проанализировать временные данные")