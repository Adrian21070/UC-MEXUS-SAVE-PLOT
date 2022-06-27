import PySimpleGUI as sg

#g1 = sg.DEFAULT_BASE64_LOADING_GIF
g1 = r'D:\Sensores//82em.gif'
while True:
    if not sg.popup_animated(g1, message='Right Click To Exit GIF Windows That Follow\nLeft click to move to next one', no_titlebar=False, time_between_frames=100, text_color='black'):
        break
sg.popup_animated(None)
#gifs = [g1]
#layout = [[sg.Image(background_color='white', key='-IMAGE-', right_click_menu=['UNUSED', 'Exit'])],[sg.Text('sAmPlE TexT',key='smptex')]]

#window = sg.Window('Title',layout, finalize=True)
#image =  window['-IMAGE-']               #type: sg.Image
#while True:
#    event, values = window.read(timeout=10)
#    if event in (None,'Exit'):
#        break
#    #image.update_animation_no_buffering(g1, 100)
#    image.update_animation(g1, 100)