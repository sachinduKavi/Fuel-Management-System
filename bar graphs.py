import matplotlib.pyplot as plt


x = ['hello', 'gonsen', 'boola']
y = [100, 200, 300]
y_1 = [150, 100, 250]
plt.bar(x, y)
plt.bar(x, y_1, color='green')
plt.show()
