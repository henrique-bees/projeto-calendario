import PySimpleGUI as sg
import calendar as cal

sg.theme("DarkGrey16")


def front():
    flayout = [
        [sg.Text("Bem vindo!", font=("Helvetica", 20))],
        [sg.Button("Visualisar Calendário")], [sg.Button("Sair do aplicativo")]
    ]

    window = sg.Window("Calendary Project App", flayout, size=(500, 200), element_justification="center")
    button, values = window.read()
    if button == "Visualizar Calendário":
        window.close()
    elif button == "Sair do aplicativo":
        window.exit()


front()


def front2():
    sg.theme("DarkGrey16")
    flayout = [
        [sg.Button("Eventos", size=(20, 2))],
        [sg.Button("Alarmes", size=(20, 2))],
        [sg.Button("Tarefas", size=(20, 2))],
        [sg.Button("Notas", size=(20, 2))],
        [sg.Button("Lembretes", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("Calendário", flayout, size=(700, 300), element_justification="left")
    button, values = window.read()
    if button == "Eventos":
        window.close()
    elif button == "Alarmes":
        window.close()
    elif button == "Tarefas":
        window.close()
    elif button == "Notas":
        window.close()
    elif button == "Lembretes":
        window.close()
    elif button == "Sair":
        window.exit()


front2()


def eventos():
    sg.theme("DarkGrey16")

    layout = [
        [sg.Text("Aqui você marcará os seus eventos", font=("Arial", 20))],
        [sg.Button("Voltar para página anterior", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("Eventos", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Voltar para página anterior":
        window.close()
        front2()
    elif button == "Sair":
        window.close()
        exit()


eventos()


def alarmes():
    sg.theme("DarkGrey16")

    layout = [
        [sg.Text("Aqui você marcará os seus alarmes", font=("Arial", 20))],
        [sg.Button("Voltar para página anterior", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("Alarmes", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Voltar para página anterior":
        window.close()
        front2()
    elif button == "Sair":
        window.close()
        exit()


alarmes()


def tarefas():
    sg.theme("DarkGrey16")

    layout = [
        [sg.Text("Aqui você marcará as suas tarefas", font=("Arial", 20))],
        [sg.Button("Voltar para página anterior", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("Tarefas", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Voltar para página anterior":
        window.close()
        front2()
    elif button == "Sair":
        window.close()
        exit()


tarefas()


def notas():
    sg.theme("DarkGrey16")

    layout = [
        [sg.Text("Aqui você marcará as suas anotações", font=("Arial", 20))],
        [sg.Button("Voltar para página anterior", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("Anotações", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Voltar para página anterior":
        window.close()
        front2()
    elif button == "Sair":
        window.close()
        exit()


notas()


def lembretes():
    sg.theme("DarkGrey16")

    layout = [
        [sg.Text("Aqui você marcará os seus lembretes", font=("Arial", 20))],
        [sg.Button("Voltar para página anterior", size=(20, 2))],
        [sg.Button("Sair", size=(20, 2))]
    ]

    window = sg.Window("lembretes", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    if button == "Voltar para página anterior":
        window.close()
        front2()
    elif button == "Sair":
        window.close()
        exit()
lembretes()


