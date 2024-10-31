from sklearn.datasets import fetch_openml # Считывание данных с сервера
from sklearn.model_selection import train_test_split # Разбиение данных
from sklearn.preprocessing import StandardScaler # Масштабирование данных
from sklearn.linear_model import LinearRegression # Регрессия
from sklearn.metrics import r2_score, mean_squared_error

from sklearn.preprocessing import PolynomialFeatures

import pandas as pd
import numpy as np


data = fetch_openml(data_id=561, as_frame=True)

print(data.details)
print(data.DESCR)
X, y = data.data, data.target
X = X.select_dtypes(include=[np.number])

print("Пропуски в данных:\n", X.isnull().sum(), sep='')
print("Типы данных в признаках:\n", X.dtypes, sep='')

print("Размеры признаков (X):", X.shape)
print("Размеры целевой переменной (y):", y.shape)

print("Количество столбцов:", X.shape[1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
print("Количество объектов в обучающем наборе:", X_train.shape[0])

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

mean_test_scaled = X_test_scaled.mean()

print("Среднее значение по всей матрице тестовых данных:", round(mean_test_scaled, 3))

model_sklearn = LinearRegression()
model_sklearn.fit(X_train_scaled, y_train)

coef_sklearn = model_sklearn.coef_
intercept_sklearn = model_sklearn.intercept_

print("Коэффициенты из sklearn:", coef_sklearn)
print("Свободный коэффициент из sklearn:", round(intercept_sklearn, 3))

class GradientDescentLinearRegression:
    def __init__(self, learning_rate=0.15, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
    
    def fit(self, X, y):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        self.theta = np.random.randn(X_b.shape[1])
        
        for _ in range(self.n_iterations):
            gradients = 2 / X_b.shape[0] * X_b.T.dot(X_b.dot(self.theta) - y)
            self.theta -= self.learning_rate * gradients
        
        self.coef_ = self.theta[1:]
        self.intercept_ = self.theta[0]

model_custom = GradientDescentLinearRegression(learning_rate=0.15, n_iterations=1000)
model_custom.fit(X_train_scaled, y_train.astype(int).values)

print("Коэффициенты нашей модели:", model_custom.coef_)
print("Свободный коэффициент нашей модели:", round(model_custom.intercept_, 3))

y_pred_sklearn = model_sklearn.predict(X_test_scaled)

r2_sklearn = r2_score(y_test, y_pred_sklearn)
rmse_sklearn = np.sqrt(mean_squared_error(y_test, y_pred_sklearn))

print("Коэффициент детерминации (R²) для модели sklearn:", round(r2_sklearn, 3))
print("Ошибка RMSE для модели sklearn:", round(rmse_sklearn, 3))

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train_scaled)
X_test_poly = poly.transform(X_test_scaled)

scaler_poly = StandardScaler()
X_train_poly_scaled = scaler_poly.fit_transform(X_train_poly)
X_test_poly_scaled = scaler_poly.transform(X_test_poly)

model_poly = LinearRegression()
model_poly.fit(X_train_poly_scaled, y_train)
y_pred_poly = model_poly.predict(X_test_poly_scaled)

r2_poly = r2_score(y_test, y_pred_poly)
rmse_poly = np.sqrt(mean_squared_error(y_test, y_pred_poly))

print("Коэффициент детерминации (R²) для полиномиальной модели:", round(r2_poly, 3))
print("Ошибка RMSE для полиномиальной модели:", round(rmse_poly, 3))