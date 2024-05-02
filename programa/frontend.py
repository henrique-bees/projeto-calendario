import PySimpleGUI as sg
import calendar as cal

sg.theme("DarkGrey4")


def eventos():
    sg.theme("DarkGrey4")

    layout = [
        [sg.Text("Aqui você marcará os seus eventos", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],

    ]

    window = sg.Window("Eventos", layout, size=(700, 300),
                       element_justification=("center"))
    button, values = window.read()
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    front2()


def alarmes():
    sg.theme("DarkGrey4")

    layout = [
        [sg.Text("Aqui você marcará os seus alarmes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]

    window = sg.Window("Alarmes", layout, size=(700, 300),
                       element_justification=("center"))
    button, values = window.read()
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    front2()


def tarefas():
    sg.theme("DarkGrey4")

    layout = [
        [sg.Text("Aqui você marcará as suas tarefas", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]

    window = sg.Window("Tarefas", layout, size=(700, 300),
                       element_justification=("center"))
    button, values = window.read()
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    front2()


def anotações():
    sg.theme("DarkGrey4")

    layout = [
        [sg.Text("Aqui você marcará as suas anotações", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]

    window = sg.Window("Anotações", layout, size=(
        700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    front2()


def lembretes():
    sg.theme("DarkGrey4")

    layout = [
        [sg.Text("Aqui você marcará os seus lembretes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]

    window = sg.Window("Lembretes", layout, size=(
        700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    front2()


def front():
    flayout = [
        [sg.Text("Bem vindo!", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Visualizar Calendário", button_color="#2e689f"), sg.Button(
                "Sair do aplicativo", button_color=("#2e689f"))],
        ], element_justification="center", expand_x=True, pad=(0, (120, 0)))],
    ]

    window = sg.Window("Calendary Project App", flayout, size=(
        500, 200), element_justification="center")
    button, values = window.read()
    window.close()

    if button == "Visualizar Calendário":
        window.close()
    elif button == "Sair do aplicativo" or button == sg.WINDOW_CLOSED:
        exit()


front()


def front2():
    sg.theme("DarkGrey4")
    flayout = [
        [sg.Button("Eventos", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Alarmes", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Tarefas", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Anotações", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Lembretes", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Sair", size=(20, 2), button_color=("#2e689f"))]
    ]

    window = sg.Window("Calendário", flayout, size=(
        700, 300), element_justification="left")
    button, values = window.read()
    window.close()
    if button == "Eventos":
        eventos()
    elif button == "Alarmes":
        alarmes()
    elif button == "Tarefas":
        tarefas()
    elif button == "Anotações":
        anotações()
    elif button == "Lembretes":
        lembretes()
    elif button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()


front2()
