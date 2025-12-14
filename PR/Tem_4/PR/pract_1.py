import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

CSV_PATH = "lab_data.csv"

df = pd.read_csv(CSV_PATH)
print("Перші рядки CSV:")
print(df.head())

# Отримуємо сітку x1, x2 і матрицю Y з таблиці
x1_vals = np.sort(df["x1"].unique())
x2_vals = np.sort(df["x2"].unique())
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Y_target = df["y"].values.reshape(len(x2_vals), len(x1_vals))

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X1, X2, Y_target)
ax.set_title("Еталонна поверхня (з CSV)")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_zlabel("y")
plt.show()

def trimf(x, a, b, c):
    x = np.asarray(x)
    return np.clip(
        np.minimum((x - a) / (b - a + 1e-9),
                   (c - x) / (c - b + 1e-9)),
        0.0,
        1.0
    )

# Діапазони як у методичці
x1_min, x1_max = -7.0, 3.0
x2_min, x2_max = -4.4, 1.7

# x1: Low / Medium / High
def mf_x1_low(x):
    return trimf(x, -7, -7, -2)

def mf_x1_mid(x):
    return trimf(x, -4, -2, 1)

def mf_x1_high(x):
    return trimf(x, -1, 3, 3)

xx1 = np.linspace(x1_min, x1_max, 400)

plt.figure(figsize=(7, 4))
plt.plot(xx1, mf_x1_low(xx1),  label="Низький")
plt.plot(xx1, mf_x1_mid(xx1),  label="Середній")
plt.plot(xx1, mf_x1_high(xx1), label="Високий")
plt.title("Функції належності змінної x1")
plt.xlabel("x1")
plt.ylabel("μ")
plt.grid(True)
plt.legend()
plt.show()

# x2: Low / Medium / High
def mf_x2_low(x):
    return trimf(x, -4.4, -4.4, -1.5)

def mf_x2_mid(x):
    return trimf(x, -3.7, -1.5, 1.2)

def mf_x2_high(x):
    return trimf(x, -0.5, 1.7, 1.7)

xx2 = np.linspace(x2_min, x2_max, 400)

plt.figure(figsize=(7, 4))
plt.plot(xx2, mf_x2_low(xx2),  label="Низький")
plt.plot(xx2, mf_x2_mid(xx2),  label="Середній")
plt.plot(xx2, mf_x2_high(xx2), label="Високий")
plt.title("Функції належності змінної x2")
plt.xlabel("x2")
plt.ylabel("μ")
plt.grid(True)
plt.legend()
plt.show()
x1_line = np.linspace(x1_min, x1_max, 400)
x2_fixed = 0.0   # фіксуємо x2, як у прикладі

y_const_50 = 50 * np.ones_like(x1_line)
y_lin_4x1_x2 = 4 * x1_line - x2_fixed
y_lin_2x1_2x2_1 = 2 * x1_line + 2 * x2_fixed + 1
y_lin_8x1_2x2_8 = 8 * x1_line + 2 * x2_fixed + 8
y_const_0 = np.zeros_like(x1_line)

plt.figure(figsize=(7, 5))
plt.plot(x1_line, y_const_50,      label="y = 50")
plt.plot(x1_line, y_lin_4x1_x2,    label="y = 4x1 - x2")
plt.plot(x1_line, y_lin_2x1_2x2_1, label="y = 2x1 + 2x2 + 1 (x2=0)")
plt.plot(x1_line, y_lin_8x1_2x2_8, label="y = 8x1 + 2x2 + 8 (x2=0)")
plt.plot(x1_line, y_const_0,       label="y = 0")
plt.title('Вікно лінійних залежностей "входи–вихід" (Sugeno)')
plt.xlabel("x1 (при x2 = 0)")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()