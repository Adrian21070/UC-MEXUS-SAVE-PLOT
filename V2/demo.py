import matplotlib.pyplot as plt
import numpy as np

z = [2,5,4,7,9,10,2,5,3]
x = np.linspace(0, len(z), len(z))

fig, ax = plt.subplots(1, 1, dpi=100, figsize=(7,5))

ax.scatter(x,z)

ax.set_xticks(x, labels=['2022_04_06_12:00','b','c','a','b','c','a','b','c'])

ax.tick_params(axis='both',
                   labelsize=11-2)
plt.show()