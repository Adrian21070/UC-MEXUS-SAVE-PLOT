
from matplotlib import projections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import griddata
from scipy import interpolate
from matplotlib import cm
"""
def func(x, y):

    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

columns = 10
rows = 5
lateral_length = 1
depth_length = 2
x_axis =(list(range(0,columns))*rows)
x_axis = np.array([x_axis])*lateral_length
#x_axis = np.array([element * lateral_length for element in x_axis])
column_with_interval = np.arange(0,rows*depth_length,depth_length)
y_axis = (list(range(0,rows))*columns)
y_axis = np.array([y_axis])*depth_length
y_axis = np.array([np.concatenate([([t]*columns) for t in column_with_interval], axis=0)])
print(x_axis[0,2])
points = np.concatenate((x_axis.T, y_axis.T), axis=1)
#print(points[1,1])
z = np.sin(points[:,0] - points[:,1])

grid_x, grid_y = np.mgrid[0:columns*lateral_length-lateral_length:200j, 0:rows*(depth_length)-depth_length:200j]

rng = np.random.default_rng()

#points = rng.random((1000, 2))

#values = func(points[:,0], points[:,1])


grid_z0 = griddata(points, z, (grid_x, grid_y), method='cubic')

#grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')

#grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

"""
"""
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
si = [105 for ii in range(len(z))]
ax.scatter(points[:,0], points[:,1], z, s=si)


ax.plot_surface(grid_x, grid_y, grid_z0,cmap=cm.inferno)
plt.show()
#plt.imshow(func(grid_x, grid_y).T, extent=(0,8,0,9), origin='lower')

#plt.plot(points[:,0], points[:,1], 'k.', ms=1)

plt.gcf().set_size_inches(6, 6)

plt.show()"""
x = np.arange(0, 11, 2)

y = np.array([14, 12, 16 ,18, 10, 13])

tck = interpolate.splrep(x, y, s=0)

f = interpolate.interp1d(x, y, kind='quadratic')

xnew = np.arange(0, 10.1, 0.1)

ynew = interpolate.splev(xnew, tck, der=0)
ynew2 = f(xnew)
plt.figure()
plt.scatter(x,y, s=40, c='r')
plt.plot(xnew, ynew, '--', xnew, ynew2, ':', c='b',linewidth=2)
#plt.plot(x, y, 'x', xnew, ynew, xnew, np.sin(xnew), x, y, 'b')

#plt.legend(['Linear', 'Cubic Spline', 'True'])

#plt.axis([-0.05, 6.33, -1.05, 1.05])

plt.title('Cubic-spline interpolation')

plt.show()


"""
import PySimpleGUI as sg


    #Simple test harness to demonstate how to use the CalendarButton and the get date popup
# sg.theme('Dark Red')
layout2 = [[sg.Input(key='Esc', size=(20,1))],
        [sg.Button('Read', key='HTML'), sg.Exit()]]
layout3 = [[sg.Input(key='E23c', size=(20,1))],
        [sg.Button('Hola', key='HTM23'), sg.Exit()]]

#chain = list(range(8,0,-1))
chain = list(range(1,9))
a = {}
it = 0
for i in range(2):
    for j  in range(4):
        a[f'{i},{j}'] = chain[it]
        it += 1  

#a = {f'{key},{key2}':chain for key in range()}

layout8 = [[sg.Frame('Disposición de los sensores', [[sg.Input(a[f'{row},{col}'], key=f'{row},{col}', size=(5,1))
            for col in range(4)] for row in range(2)])],
            [sg.Button('Submit', font=('Times New Roman',12)),sg.Button('Exit', font=('Times New Roman',12))]]

#layout4 = [[sg.Column(layout2, key='-COL1-'), sg.Column(layout3, visible=False, key='-COL2-')]]
window = sg.Window('window', layout8)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'HTML':
        layout = 1
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)
        sg.popup('You chose:', sg.popup_get_date())
window.close()
"""