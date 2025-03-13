from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np

dataset = fetch_openml(name="phoneme", version=1, as_frame=True)

print('=' * 100)
print("Описание датасета:")
print(dataset.DESCR)
print('=' * 100)

X = dataset.data
y = dataset.target

# Вывод размеров
print('=' * 100)
print("Размеры матрицы признаков X:", X.shape)
print("Размеры целевой переменной y:", y.shape)
print('=' * 100)

print('=' * 100)
if X.isnull().values.any():
    print("В данных есть пропуски!")
else:
    print("Пропусков в данных нет.")
print('=' * 100)

print('=' * 100)
if np.all(np.issubdtype(dtype, np.number) for dtype in X.dtypes):
    print("Все признаки числовые.")
else:
    print("В данных есть нечисловые признаки!")
print('=' * 100)

y = pd.factorize(y)[0]

classes, counts = np.unique(y, return_counts=True)
print("\nКоличество объектов каждого класса:")
for cls, count in zip(classes, counts):
    print(f"Класс {cls}: {count} объектов")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, shuffle=True
)

# Вывод количества объектов в тестовой выборке
print("Количество объектов в тестовом наборе:", len(X_test))

scaler = MinMaxScaler()


X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
median_value = np.median(X_train_scaled)

print(f"Медианное значение по обучающим данным: {median_value:.3f}")


model = LogisticRegression()
model.fit(X_train_scaled, y_train)
print("Коэффициенты гиперплоскости (веса признаков):")
print(model.coef_)
print(f"Свободный коэффициент (intercept): {model.intercept_:.3f}")
print(model.intercept_)