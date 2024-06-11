import PySimpleGUI as sg

layout_frame_salvos = [
    [sg.Column([], key='-BUTTON_LIST-')],
    [sg.Listbox(values="", size=(400, 190), key='-LISTBOX-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
]

frame_salvos = sg.Frame(
    "Notas Salvas", layout_frame_salvos, size=(400, 190))

window = sg.Window('Exemplo de Listbox com Duplo Clique')

# Abrindo a janela antes de acessar o widget
window.finalize()

# Obtendo o widget Listbox dentro do Frame
listbox_widget = frame_salvos.find_element('-LISTBOX-').Widget

# Vinculando o evento de duplo clique ao Listbox
listbox_widget.bind('<Double-1>', lambda event: window.write_event_value('-LISTBOX-DOUBLE_CLICK', ''))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-LISTBOX-DOUBLE_CLICK':
        print("Duplo clique no Listbox dentro do Frame")

window.close()
