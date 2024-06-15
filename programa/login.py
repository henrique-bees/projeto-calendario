import PySimpleGUI as sg
import sqlite3 as sq
from backend import verificar_registro, verificar_senha


def login():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário: "), sg.I(key="-NAME-")],
        [sg.T("Senha:   "),
         sg.I(key="-SENHA-", password_char="*", size=(36, 2)),
         sg.Button("👁", key="-SHOW_PASSWORD-", border_width=0,
                   button_color=("#343434"))],
        [sg.HorizontalSeparator()],
        [sg.Button("Entrar", button_color="#4169E1", size=(11, 1)),
         sg.Push(),
         sg.Button("Esqueci minha senha", button_color="#4169E1"),
         sg.Push(),
         sg.Button("Nova conta", button_color="#4169E1", size=(11, 1))]
    ]

    layout = [
        [sg.Frame("Login", frame)],
    ]
    window = sg.Window("Login", layout, size=(400, 142))

    while True:
        event, values = window.read()
        if event == "Nova conta":
            window.close()
            return "Voltar"
        elif event == "Esqueci minha senha":
            window.close()
            return "nova senha"
        elif event == "-SHOW_PASSWORD-":
            password_input = window['-SENHA-']
            if password_input.Widget.cget("show") == "*":
                password_input.Widget.config(show="")
            else:
                password_input.Widget.config(show="*")
        elif event == sg.WINDOW_CLOSED:
            exit()
        elif event == "Entrar":
            usuario = values["-NAME-"]
            senha = values["-SENHA-"]

            # Banco de Dados
            conexao = sq.connect("programa/registro.db")
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT nome, senha, id FROM usuarios WHERE nome = ?",
                (usuario,))
            busca = cursor.fetchone()
            conexao.close()
            if busca is not None and busca[1] == senha:
                sg.popup_no_buttons(
                    "Login efetuado com sucesso, bem-vindo",
                    auto_close_duration=3, title="Login efetuado")
                (usuario, senha)
                window.close()
                id = busca[2]
                return id
            else:
                sg.popup_no_buttons(
                    "Usuário ou senha incorretos", title="ERRO")


# Inserindo função de registro

def registro():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "), sg.I(key="-NAME-")],
        [sg.T("Senha:               "),
         sg.I(key="-SENHA-", password_char="*", size=(30, 2)),
         sg.Button("👁", key="-SHOW_PASSWORD-", border_width=0,
                   button_color="#343434")],
        [sg.T("Confirmar Senha:"),
         sg.I(key="-SENHA2-", password_char="*", size=(30, 2)),
         sg.Button("👁", key="-SHOW_CONFIRM_PASSWORD-", border_width=0,
                   button_color="#343434")],
        [sg.HorizontalSeparator()],
        [sg.VerticalSeparator(),
         sg.Text("Requisitos da senha:\n"
                 "⚪ 1 letra maiúscula;\n"
                 "⚪ 1 letra minúscula;\n"
                 "⚪ 1 número;\n"
                 "⚪ 1 caractére especial;\n"
                 "⚪ minímo de 8 caractéres e máximo de 16.",
                 font=("Arial", 9)),
         sg.Push(),
         sg.VerticalSeparator()],
        [sg.HorizontalSeparator()]
    ]

    layout = [
        [sg.Frame("Registro", frame)],
        [sg.Button("Criar conta", button_color="#4169E1", size=(20, 1)),
         sg.Push(),
         sg.Button("Entrar com conta existente", button_color="#4169E1",
                   size=(20, 1))]
    ]
    window = sg.Window("Registro", layout, size=(400, 270))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            quit()
        elif event == "-SHOW_PASSWORD-":
            password_input = window['-SENHA-']
            if password_input.Widget.cget("show") == "*":
                password_input.Widget.config(show="")
            else:
                password_input.Widget.config(show="*")
        elif event == "-SHOW_CONFIRM_PASSWORD-":
            password_input2 = window['-SENHA2-']
            if password_input2.Widget.cget("show") == "*":
                password_input2.Widget.config(show="")
            else:
                password_input2.Widget.config(show="*")
        elif event == "Entrar com conta existente":
            window.close()
            return "login"
        if event == "Criar conta":
            usuario = values["-NAME-"].strip()
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            massa = verificar_registro(usuario)
            if massa == "vazio":
                sg.popup_no_buttons(
                    "Você precisa inserir um usuário")
            elif massa == "existe":
                sg.popup_no_buttons(
                    "Usuário já foi cadastrado")
            elif massa == "não existe":
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
                        sg.popup_no_buttons("Registro realizado com sucesso!",
                                            auto_close=3, title="Conta criada")
                        return "login"
                    else:
                        sg.popup_no_buttons(
                            "Senha invalida, as senhas devem possuir "
                            "pelo menos uma letra maiuscula, uma "
                            "minuscula, um numero, um caractere "
                            "especial, e ter entre 8 e 16 caracteres",
                            title="ERRO")
                else:
                    sg.popup_no_buttons(
                        "As senhas não coincidem ou o usuário é vazio,"
                        " por favor, tente novamente", title="ERRO")


# Inserindo função de criar uma nova senha

def nova_senha_deslogado():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "),
         sg.I(key="-USUARIO-")],
        [sg.HorizontalSeparator()],
        [sg.T("Senha:               "),
         sg.I(key="-SENHA-", password_char="*", size=(29, 2)),
         sg.Button("👁", key="-SHOW_PASSWORD-", border_width=0,
                   button_color=("#343434"))],
        [sg.T("Confirmar Senha:"),
         sg.I(key="-SENHA2-", password_char="*", size=(29, 2)),
         sg.Button("👁", key="-SHOW_CONFIRM_PASSWORD-", border_width=0,
                   button_color=("#343434"))],
    ]

    layout = [
        [sg.Frame("Nova Senha", frame)],
        [sg.Button("Mudar senha", button_color="#4169E1", size=(15, 1)),
         sg.Push(),
         sg.Button("Cancelar", button_color="#4169E1", size=(15, 1))],
    ]
    window = sg.Window("Recuperação de senha", layout, size=(400, 165))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            quit()
        elif event == "-SHOW_PASSWORD-":
            password_input = window['-SENHA-']
            if password_input.Widget.cget("show") == "*":
                password_input.Widget.config(show="")
            else:
                password_input.Widget.config(show="*")
        elif event == "-SHOW_CONFIRM_PASSWORD-":
            password_input2 = window['-SENHA2-']
            if password_input2.Widget.cget("show") == "*":
                password_input2.Widget.config(show="")
            else:
                password_input2.Widget.config(show="*")
        elif event == "Cancelar":
            window.close()
            return "login"
        elif event == "Mudar senha":
            usuario = values["-USUARIO-"].strip()
            print(usuario)
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha == senha2:
                svalido = verificar_senha(senha)
                uvalido = verificar_registro(usuario)
                if uvalido == "existe":
                    if svalido:
                        conexao = sq.connect("programa/registro.db")
                        cursor = conexao.cursor()
                        cursor.execute(
                            "UPDATE usuarios SET senha = ? WHERE nome = ?",
                            (senha, usuario))
                        conexao.commit()
                        conexao.close()
                        window.close()
                        sg.popup_no_buttons(
                            "A nova senha foi cadastrada com sucesso!",
                            auto_close_duration=3, title="Senha modificada")
                        return "login"
                    else:
                        sg.popup_no_buttons(
                            "Senha invalida, as senhas devem possuir "
                            "pelo menos uma letra maiuscula, uma "
                            "minuscula, um numero, um caractere "
                            "especial, e ter entre 8 e 16 caracteres",
                            title="ERRO"
                        )
                elif uvalido == "vazio":
                    sg.popup_no_buttons(
                        "você precisa inserir um usuário para alterar"
                        " a senha.\n", title="ERRO")
                elif uvalido == "não existe":
                    sg.popup_no_buttons(
                        "Você precisa inserir um usuário "
                        "existente para mudar a senha",
                        title="ERRO")

            else:
                sg.popup_no_buttons(
                    "As senhas não coincidem ou o usuário é vazio, por favor,"
                    " tente novamente", title="ERRO")


def nova_senha_logado(id):
    sg.theme("DarkGrey16")
    frame = [
        [sg.Text("Senha Atual:      "),
         sg.Input(key="-SENHAA-")],
        [sg.HorizontalSeparator()],
        [sg.Text("Senha:               "),
         sg.Input(key="-SENHA-", password_char="*", size=(29, 2)),
         sg.Button("👁", key="-SHOW_PASSWORD-", border_width=0,
                   button_color=("#343434"))],
        [sg.Text("Confirmar Senha:"),
         sg.Input(key="-SENHA2-", password_char="*", size=(29, 2)),
         sg.Button("👁", key="-SHOW_CONFIRM_PASSWORD-", border_width=0,
                   button_color=("#343434"))],
    ]
    layout = [
        [sg.Frame("Nova Senha", frame)],
        [sg.Button("Mudar senha", button_color="#4169E1", size=(10, 1)),
         sg.Push(),
         sg.Button("Voltar", button_color="#4169E1", size=(10, 1))],
    ]
    window = sg.Window("Recuperação de senha", layout, size=(400, 165))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            quit()
        elif event == "-SHOW_PASSWORD-":
            password_input = window['-SENHA-']
            if password_input.Widget.cget("show") == "*":
                password_input.Widget.config(show="")
            else:
                password_input.Widget.config(show="*")
        elif event == "-SHOW_CONFIRM_PASSWORD-":
            password_input2 = window['-SENHA2-']
            if password_input2.Widget.cget("show") == "*":
                password_input2.Widget.config(show="")
            else:
                password_input2.Widget.config(show="*")
        elif event == "Voltar":
            window.close()
            return "editar perfil"
        elif event == "Mudar senha":
            senha_atual = values["-SENHAA-"]
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha_atual != "":
                if senha == senha2:
                    valido = verificar_senha(senha)
                    if valido:
                        conexao = sq.connect("programa/registro.db")
                        cursor = conexao.cursor()
                        cursor.execute(
                            "SELECT nome, senha FROM usuarios WHERE id = ?",
                            (id,))
                        usuario = cursor.fetchone()
                        if senha_atual == usuario[1]:
                            cursor.execute(
                                "UPDATE usuarios SET senha = ? WHERE nome = ?",
                                (senha, usuario[0]))
                            conexao.commit()
                            conexao.close()
                            window.close()
                            sg.popup_no_buttons(
                                "A nova senha foi cadastrada com sucesso!",
                                auto_close_duration=3, title="Senha modificada"
                            )
                            return "editar perfil"
                        else:
                            sg.popup_no_buttons("A senha atual está incorreta",
                                                title="ERRO")
                    else:
                        sg.popup_no_buttons(
                            "Senha invalida, as senhas devem possuir "
                            "pelo menos uma letra maiuscula, uma "
                            "minuscula, um numero, um caractere "
                            "especial, e ter entre 8 e 16 caracteres",
                            title="ERRO")
                else:
                    sg.popup_no_buttons(
                        "As senhas não coincidem, por favor, tente novamente",
                        title="ERRO")
            else:
                sg.popup_no_buttons("Você precisa inserir a senha atual",
                                    title="ERRO")


login()
