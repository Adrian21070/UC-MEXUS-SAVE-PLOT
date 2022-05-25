import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from PIL import Image

def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im

def gen(path):
    im = Image.open(path)
    return im

im = []
for ii in range(20):
    im.append(gen_frame('Imagenes\\'+f'demo{ii}.png'))
    
#im = [frame.convert('PA') for frame in im]

im[0].save('GIF.gif', save_all=True, append_images=im[1:], loop=0, duration=200, disposal = 2, optimize=True, transparency=True)

"""
def anima(i,x,y):
    ax.clear()
    ax.scatter(x[0:i],y[0:i])
    plt.ylabel('Datos')


fig = plt.figure()
ax = fig.add_axes((0.1, 0.17, 0.8, 0.72))
#ax = plt.gca()
#fig.patch.set_alpha(0.0)
#ax.patch.set_alpha(0.0)

t = np.arange(0,5,0.1)
x = np.cos(t)
y = np.sin(t)

#os.makedirs('Imagenes', exist_ok=True)
ax.scatter(x[0:10],y[0:10])
ax.scatter(x[10:20],y[10:20])
ax.legend(['Promedio', 'Interpolación cuadrática'], loc='upper right', framealpha=0.1)
plt.savefig(f'demo{0}.png', transparent=True)
#for ii in range(len(t)):
#    anima(ii,x,y)
#    ax.scatter()
    #plt.savefig('Imagenes\\'+f'demo{ii}.png', transparent=True)
"""