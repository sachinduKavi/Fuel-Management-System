import numpy as np
import matplotlib.pyplot as plt

month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
Ygirls = [10, 20, 20, 40, 20, 20, 40, 20, 20, 40, 20, 20]
Zboys = [20, 30, 25, 30, 20, 20, 40, 20, 20, 40, 20, 20]

X_axis = np.arange(len(month_list))

plt.bar(X_axis - 0.2, Ygirls, 0.4, label='Girls')
plt.bar(X_axis + 0.2, Zboys, 0.4, label='Boys')

plt.xticks(X_axis, month_list)
plt.xlabel("Groups")
plt.ylabel("Number of Students")
plt.title("Number of Students in each group")
plt.legend()
plt.show()
