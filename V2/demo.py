import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg

"""
z = [2,5,4,7,9,10,2,5,3]
x = np.linspace(0, len(z), len(z))

fig, ax = plt.subplots(1, 1, dpi=100, figsize=(7,5))

ax.plot(x,z)

ax.set_xticks([1,5,7], labels=['2022_04_06_12:00','b','c'])
col = ax.get_lines()[0].get_color()

ax.legend(['Linea'], loc='center right')
ax.tick_params(axis='both',
                   labelsize=11-2)
plt.show()
"""
sg.popup_no_wait('En proceso de descarga de información...\nFavor de esperar', title='UCMexus')
sg.popup_auto_close('',auto_close_duration=0.1, keep_on_top=False)
# Here, have some windows on me....
[sg.popup_no_wait('No-wait Popup', relative_location=(-500+100*x, -500)) for x in range(10)]
answer = sg.popup_yes_no('Do not worry about all those open windows... they will disappear at the end', 'Are you OK with that?')

if answer == 'No':
    sg.popup_cancel('OK, we will destroy those windows as soon as you close this window')

sg.popup_no_buttons('Your answer was', answer, relative_location=(0, -200), non_blocking=True)
text = sg.popup_get_text('This is a call to PopopGetText')
sg.popup_get_file('Get file')
sg.popup_get_folder('Get folder')
sg.popup('Simple popup')
sg.popup_no_titlebar('No titlebar')
sg.popup_no_border('No border')
sg.popup_no_frame('No frame')
sg.popup_cancel('Cancel')
sg.popup_auto_close('This window will Autoclose and then everything else will close too....')
#a = sg.popup_no_wait('Sensores en proceso de descarga...',)

#a.close()