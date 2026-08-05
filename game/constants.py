#EMPTY = 0
#BLACK = 1
#WHITE = 2
import matplotlib.pyplot as plt
import numpy as np

data = [4, 2, 5, 4, 6, 3, 4, 1]

# 1. ЭФР
plt.step(sorted(data), np.arange(1, len(data)+1) / len(data), where='post')
plt.title("Эмпирическая функция распределения")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.show()

# 2. Гистограмма
plt.hist(data, bins=[1, 2, 3, 4, 5, 6, 7], edgecolor='black')
plt.title("Гистограмма частот")
plt.xlabel("Значение")
plt.ylabel("Частота")
plt.show()

# 3. Box Plot
plt.boxplot(data)
plt.title("Ящик с усами")
plt.ylabel("Значение")
plt.show()

# 4. Scatter Plot
plt.scatter(range(1, len(data)+1), data)
plt.title("Диаграмма рассеяния")
plt.xlabel("Индекс элемента")
plt.ylabel("Значение")
plt.show()