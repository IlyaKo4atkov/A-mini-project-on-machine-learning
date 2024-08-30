
from requests import get
response = get("https://storage.yandexcloud.net/academy.ai/the_movies_dataset.zip")

with open('the_movies_dataset.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

!unzip -qo "the_movies_dataset.zip" -d ./the_movies_dataset

# Папка с распакованным датасетом
FILE_PATH = './the_movies_dataset'

import os
os.listdir(FILE_PATH)

import pandas as pd
import numpy as np
df = pd.read_csv(f'{FILE_PATH}/movies_metadata.csv')

#Очистка данных

df = df.drop(['imdb_id'], axis=1)
df = df.drop(['adult'], axis=1)
df = df.drop(['belongs_to_collection'], axis=1)
df = df.drop(['homepage'], axis=1)
df = df.drop(['video'], axis=1)
df = df.drop(['poster_path'], axis=1)
df = df.drop(['production_companies'], axis=1)

#Для дальнейшего анализа даннаые кассового сбора, которые равны 0, пометим как NaN
df['revenue'] = df['revenue'].replace(0, np.nan)

df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['budget'] = df['budget'].replace(0, np.nan)
df[df['budget'].isnull()]

#Создаем функцию которая преобразовывает дату выхода фильма в день недели

day_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
import datetime
def week_day(date):
  try:
    date_1 = str(date).split('-')
    res = datetime.date(int(date_1[0]), int(date_1[1]), int(date_1[2]))
    return day_week[res.weekday()]
  except:
    np.nan
df['day_week'] = df['release_date'].apply(week_day)

#Построение результирующего графика
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,6))
plt.title('Число фильмов по дням недели')
plt.xlabel('Название дней недели')
plt.ylabel('Количество фильмов')
sns.countplot(x='day_week', data = df, order=day_week)