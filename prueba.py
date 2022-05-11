import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt

def asd(z):

    x = 1
    y = 2
    if z == 3:
        w = 2
        return x,y,w
    return x,y

z = 1
x,y,w = asd(z)
print(x,y)