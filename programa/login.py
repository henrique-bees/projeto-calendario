import PySimpleGUI as sg
import sqlite3 as sq
from backend import verificar_senha, criar_sessao


def login():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário: "), sg.I(key="-NAME-")],
        [sg.T("Senha:   "), sg.I(key="-SENHA-", password_char="*")],
        [sg.HorizontalSeparator()],
        [sg.Button("Esqueci minha senha")],
    ]

    layout = [
        [sg.Frame("Login", frame)],
        [sg.Ok(), sg.B("Voltar")],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0))
        )]
    ]
    window = sg.Window("Login", layout, size=(400, 160))

    event, values = window.read()
    if event == "Voltar":
        window.close()
        return event
    elif event == "Esqueci minha senha":
        window.close()
        return event
    elif event == "Ok":
        usuario = values["-NAME-"]
        senha = values["-SENHA-"]

        # Banco de Dados
        conexao = sq.connect("programa/registro.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, senha FROM usuarios WHERE nome = ?",
                       (usuario,))
        busca = cursor.fetchone()
        conexao.close()
        if busca is not None and busca[1] == senha:
            sg.popup_timed("Login efetuado com sucesso",
                           auto_close_duration=2)
            criar_sessao(usuario, senha)
            window.close()
            return event
        else:
            sg.popup_timed("Usuário ou senha incorretos",
                           auto_close_duration=2)
            return False


def registro():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "), sg.I(key="-NAME-")],
        [sg.T("Senha:               "), sg.I(key="-SENHA-",
                                             password_char="*")],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-",
                                        password_char="*")],
        [sg.HorizontalSeparator()],
        [sg.Button("Já possuo um login")],
    ]

    layout = [
        [sg.Frame("Registro", frame)],
        [sg.Ok(), sg.B("Cancel")],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0))
        )]
    ]
    window = sg.Window("Registro", layout, size=(400, 185))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            window.close()
            return False
        elif event == "Já possuo um login":
            window.close()
            return True
        if event == "Ok":
            usuario = values["-NAME-"]
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha == senha2:
                valido = verificar_senha(senha)
                if valido:
                    conexao = sq.connect("programa/registro.db")
                    cursor = conexao.cursor()
                    cursor.execute(
                        "INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
                        (usuario, senha))
                    conexao.commit()
                    conexao.close()
                    window.close()
                    sg.popup_timed("Registro realizado com sucesso!",
                                   auto_close=2)
                    return True
                else:
                    sg.popup_timed("Senha invalida, as senhas devem possuir "
                                   "pelo menos uma letra maiuscula, uma "
                                   "minuscula, um numero, um caractere "
                                   "especial, e ter entre 8 e 16 caracteres",
                                   auto_close_duration=2)
                    return False
            else:
                sg.popup_timed(
                    "As senhas não coincidem, por favor, tente novamente",
                    auto_close_duration=2)
                return False


def nova_senha():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "),
         sg.I(key="-USUARIO-")],
        [sg.HorizontalSeparator()],
        [sg.T("Senha:               "),
         sg.I(key="-SENHA-", password_char="*")],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-", password_char="*")],
    ]

    layout = [
        [sg.Frame("Nova Senha", frame)],
        [sg.Ok(), sg.B("Voltar")],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0)
                                ))]
    ]
    window = sg.Window("Recuperação de senha", layout, size=(400, 145))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            return event
        if event == "Voltar":
            window.close()
            return event
        elif event == "Ok":
            usuario = values["-USUARIO-"]
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha == senha2:
                valido = verificar_senha(senha)
                if valido:
                    conexao = sq.connect("programa/registro.db")
                    cursor = conexao.cursor()
                    cursor.execute(
                        "UPDATE usuarios SET senha = ? WHERE nome = ?",
                        (senha, usuario))
                    conexao.commit()
                    conexao.close()
                    window.close()
                    sg.popup_timed("A nova senha foi cadastrada com sucesso!",
                                   auto_close_duration=2)
                    return event
            else:
                sg.popup_timed(
                    "As senhas não coincidem, por favor, tente novamente",
                    auto_close_duration=2)


# nova_senha()
# login()
# registro()
