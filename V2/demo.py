import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg

x = np.linspace(0, 5, 10)
y = np.linspace(0, 5, 10)
X,Y = np.meshgrid(x,y)

z = np.sin(X) + np.cos(Y)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ax.plot_surface(X,Y,z)

#ax.set_xticks([1,5,7], labels=['2022_04_06_12:00','b','c'])
#col = ax.get_lines()[0].get_color()

#ax.legend(['Linea'], loc='center right')
#ax.tick_params(axis='both',
                   #labelsize=11-2)
plt.show()