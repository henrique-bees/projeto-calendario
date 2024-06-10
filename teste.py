import PySimpleGUI as sg

# Layout da interface
layout = [
    [sg.Button('Botão 1', key='-BOTAO1-', bind_return_key=True)],
    [sg.Button('Botão 2', key='-BOTAO2-')],
    [sg.Button('Botão 3', key='-BOTAO3-')],
    [sg.Text('Pressione "1" para Botão 1, "2" para Botão 2, "3" para Botão 3')]
]

# Criação da janela
window = sg.Window('Bind Teclas para Botões', layout,
                   return_keyboard_events=True)

# Loop principal de eventos
while True:
    event, values = window.read()

    # Saída do loop principal ao fechar a janela
    if event == sg.WIN_CLOSED:
        break

    # Verifica qual botão foi pressionado ou qual tecla foi capturada
    if event == '-BOTAO1-':
        sg.popup('Botão 1 pressionado')
    elif event == '-BOTAO2-':
        sg.popup('Botão 2 pressionado')
    elif event == '-BOTAO3-':
        sg.popup('Botão 3 pressionado')
    elif event == '1':
        window['-BOTAO1-'].click()
    elif event == '2':
        window['-BOTAO2-'].click()
    elif event == '3':
        window['-BOTAO3-'].click()

# Fechamento da janela
window.close()
