import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
"""
x = np.arange(0,10,1)
y = 2*x

fig, ax1 = plt.subplots(1,1,dpi=100)

#ax1 = fig.add_axes((0.1, 0.17, 0.8, 0.72))

ax1.clear()
ax1.scatter(x, y, s=40, c='r')

#axis labels
ax1.set_xlabel('Profundidad',
              fontsize=11,
              fontfamily="Times New Roman")

ax1.set_ylabel('Promedio',
              fontsize=11,
              fontfamily="Times New Roman")

ax1.set_xticks(x)

ax1.tick_params(axis='both',
               labelsize=9)

#subtitle
ax1.set_title(f'Promedio cada {15} minutos\n'+'2022/04/07, 20:15 (hora de inicio)',
             x=0.5,
             y=0.81,
             transform=fig.transFigure,
             fontsize=11,
             fontfamily="Times New Roman")

#superior title
plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
             x=0.5,
             y=0.92,
             transform=fig.transFigure,
             fontsize=14,
             fontweight="regular",
             fontfamily="Times New Roman")

#ax1.annotate('2022/04/07, 20:15 (hora de inicio)',
#        xy=(0.5, 0.8), xytext=(0, 10),
#        xycoords=('axes fraction', 'figure fraction'),
#        textcoords='offset points',
#        size=11, ha='center', va='bottom')
#ax1.set_title('2022/04/07, 20:15 (hora de inicio)')
#plt.suptitle('PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'))

#ax1.set_xlabel('Profundidad (m)')
#ax1.set_ylabel('Valor promedio (ug/m3)')
ax1.legend(['Promedio'], loc='upper right', framealpha=1.0, fontsize=9, prop={'family': 'Times New Roman'})
#ax1.set_xticks(x, fontdict={'family':'Times New Roman', 'size':11})
#plt.setp(ax1.get_yticklabels(), fontsize=11)

ax1.axis([0, max(x)+0.5, 0, max(y)])
#plt.title('PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'), 
#        fontdict={'family': 'Times New Roman', 
#                'size': 14})

plt.subplots_adjust(top=0.8)

plt.show()

x = 1
"""
t = np.arange(0,10,1)
x = np.cos(t)
y = np.sin(t)
z = x*y

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1, projection='3d')

ax1.scatter(x, y, z, s=40, c='r')

#axis labels
ax1.set_ylabel('Profundidad',
              fontsize=11,
              fontfamily="Times New Roman")

ax1.set_xlabel('Carretera',
              fontsize=11,
              fontfamily="Times New Roman")

ax1.set_xticks(x)
ax1.set_yticks(y)
ax1.set_zticks(z)

ax1.tick_params(axis='both',
               labelsize=9)

#subtitle
ax1.set_title(f'Promedio cada {15} minutos\n'+'2022/04/07, 20:15 (hora de inicio)',
             x=0.5,
             y=0.89,
             transform=fig.transFigure,
             fontsize=11,
             fontfamily="Times New Roman")

ax1.set_title(f'Max {1.75}, Min {0.1}',
             x=0.5,
             y=0.05,
             transform=fig.transFigure,
             fontsize=11,
             fontfamily="Times New Roman")

#superior title
plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
             x=0.5,
             y=0.92,
             transform=fig.transFigure,
             fontsize=14,
             fontweight="regular",
             fontfamily="Times New Roman")
ax1.view_init(25, -130)
#ax1.grid(False)
ax1.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax1.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax1.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
plt.show()
x = 1