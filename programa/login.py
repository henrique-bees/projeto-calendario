import PySimpleGUI as sg
from time import sleep
import sqlite3 as sq


def login():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário: "), sg.I(key="-NAME-")],
        [sg.T("Senha:   "), sg.I(key="-SENHA-", password_char="*")],
        [sg.HorizontalSeparator()],
        [sg.CB("Esqueci minha senha", key="-CB1-")],
    ]	

    layout = [
        [sg.Frame("Login", frame)],
        [sg.Ok(), sg.Cancel()],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0)
            ))]
    ]
    window = sg.Window("Login", layout, size=(400,160))

    event,values = window.read()
    if event == "Cancel":
        exit()
    if event == "Ok":
        usuario = ["-NAME-"]
        senha = values["-SENHA-"]
        fsenha = values["-CB1-"]
        conexao = sq.connect("./programa/registro.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, senha FROM usuarios")
        busca = cursor.fetchall()
        if usuario not in busca or senha not in busca:
            sg.popup_timed("usuário ou senha incorretos",auto_close_duration=2)
        else:
            sg.popup_timed("login efetuado com sucesso", auto_close_duration=2)
        if senha == "":
            if fsenha == True:
                window.close()
                nova_senha()

def registro():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "), sg.I(key="-NAME-")],
        [sg.T("Senha:               "), sg.I(key="-SENHA-", password_char="*")],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-", password_char="*")],
        [sg.HorizontalSeparator()],
        [sg.CB("J possuo um login", key="-ALOGIN-")],
    ]

    layout = [
        [sg.Frame("Registro", frame)],
        [sg.Ok(), sg.Cancel()],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0)
            ))]
    ]
    window = sg.Window("Registro", layout, size=(400,185))
    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WINDOW_CLOSED:
            break

        if event == "Ok":
            usuario = values["-NAME-"]
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha != "" and senha2 != "":
                if senha == senha2:
                    window.close()
                    sg.popup_timed("Registro realizado com sucesso!", auto_close=2)
                    conexao = sq.connect("./programa/registro.db")
                    cursor = conexao.cursor()
                    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                                   id INTEGER PRIMARY KEY,
                                   nome TEXT,
                                   senha TEXT
                                   )""")
                    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
                                   (usuario, senha))
                    conexao.commit()
                    conexao.close()
                    login()
                else:
                    sg.popup_timed("As senhas não coincidem, por favor, tente novamente", auto_close_duration=2)
            else:
                log = values["-ALOGIN-"]
                if log == True:
                    window.close()
                    login()
def nova_senha():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Senha:               "), sg.I(key="-SENHA-", password_char="*")],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-", password_char="*")],
    ]

    layout = [
        [sg.Frame("Nova Senha", frame)],
        [sg.Ok(), sg.Cancel()],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0)
            ))]
    ]
    window = sg.Window("Recuperação de senha", layout, size=(400,120))
    while True:
        event,values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Cancel":
            window.close()
            login()
            break
        if event == "Ok":
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha == senha2:
                window.close()
                sg.popup_timed("A nova senha foi cadastrada com sucesso!", auto_close_duration=2)
                sleep(2)
                login()
            else:
                sg.popup_timed("As senhas não coincidem, por favor, tente novamente", auto_close_duration=2)
# nova_senha()
# login()
registro()
