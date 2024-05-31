import backend as bc
import PySimpleGUI as sg
import sqlite3 as sq


# Importando biblioteca PySimpleGUI para o front-end
# Importando biblioteca calendario para um possível acréscimo no futuro


# As partes "MAINs" do código ficam no final para todo o conteudo externo,
# (funções) poder ser lido perfeitamente.

# Inserindo função de login                     /:8
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

    while True:
        event, values = window.read()
        if event == "Voltar":
            window.close()
            registro()
        elif event == "Esqueci minha senha":
            window.close()
            nova_senha()
        elif event == "Ok":
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
                sg.popup_timed("Login efetuado com sucesso",
                               auto_close_duration=2)
                (usuario, senha)
                window.close()
                front2()
                return busca[2]
            else:
                sg.popup_timed("Usuário ou senha incorretos",
                               auto_close=2)

# Inserindo função de registro                  /:7


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
            quit()
        elif event == "Já possuo um login":
            window.close()
            login()
        if event == "Ok":
            usuario = values["-NAME-"].strip()
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            massa = bc.verificar_registro(usuario)
            if massa == "vazio":
                sg.popup_timed(
                    "O usuário precisa estar preenchido", auto_close_duration=2
                )
            elif massa == "invalido":
                sg.popup_timed(
                    "Usuário já foi cadastrado", auto_close_duration=2
                )
            elif massa == "valido":
                if senha == senha2:
                    valido = bc.verificar_senha(senha)
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
                        login()
                    else:
                        sg.popup_timed(
                            "Senha invalida, as senhas devem possuir "
                            "pelo menos uma letra maiuscula, uma "
                            "minuscula, um numero, um caractere "
                            "especial, e ter entre 8 e 16 caracteres",
                            auto_close_duration=2)
                else:
                    sg.popup_timed(
                        "As senhas não coincidem ou o usuário é vazio,"
                        " por favor, tente novamente",
                        auto_close_duration=2)

# Inserindo função de criar uma nova senha       /:9


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
    window = sg.Window("Recuperação de senha", layout, size=(400, 155))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            quit()
        if event == "Voltar":
            window.close()
            login()
        elif event == "Ok":
            usuario = values["-USUARIO-"].strip()
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            if senha == senha2 and usuario != "":
                valido = bc.verificar_senha(senha)
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
                    login()
            else:
                sg.popup_timed(
                    "As senhas não coincidem ou o usuário é vazio, por favor,"
                    " tente novamente",
                    auto_close_duration=2)

# Armazenando o icon base64                      /:11


def icon():
    return b"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kUM6tv9sV3TY6GOtOnco1pTKrIE9O7hwRHLU3MatO/k23pTOtFE7PHrsOm4yM0+nPLum66fQtIFjWLp4tnrgtEHDvZL29ZjS7ypzRk2bN3Lk0OE6Pj/KO3Tqv2mjxhnHuYcde+sRiGCCCi7IYIMOPghhhBJWY6CBE16IYYYabshhhx4WWOGBH45IYokmnogigiFWmGKLLr4IY4wRrhiijDbeiGOON9K4oo4+/ghkkBDy2KOQRh6JZJItEcmikk4+CaWMTNIYZZVWXrnhlDxiyWWXXrqnJZFfjklmmRSGuaWZaq5pJZpasglnnEG6iaacdt4JI5104slnnx3qCaifgg76IKDShgJAaKKKMndoo4guCmmkZzrqqKSWJkpppplcyqmdmn7KSaeieglqqaaeimqqqq7KaquuvgprrLLOSmuttt6Ka6667sprr77+Cmywwg5LbLHGHotsssouy2yzzj4LbbTSTktttdZei2222m7LbbfefgtuuOKOS2655p6Lbrrqrstuu+6+C2+88s5Lb7323otvvvruy2+//v4LcMACD0xwwQYfjHDCCi/McMMOPwxxxBJPTHHFFl+MccYab8xxxx5/DHLIIo9Mcskmn4xyyiqvzG0gADs="

# Função para Animação da barra de progresso     /:6


def init():
    sg.theme("DarkGrey16")

    layout = [
        # Aqui coloco a função da barra de progresso, com o valor maximo de
        # 1000 na horizontal, com o tamanho (400,50)
        [sg.ProgressBar(max_value=1000, orientation="h",
                        size=(400, 50), key="-PROG-")],
    ]

    # Aqui é uma janela normal mas sem os titulos, botao de fechar ou minimizar
    window = sg.Window("", layout, size=(400, 50), no_titlebar=True)

    # Looping para dar update na barra de progresso
    # Para aumentar a velocidade do update é so alterar o passo 2 para um maior
    for i in range(0, 1000, 2):
        # O paramentro (timeout=1) especifica que o programa aguardara 1
        # milissegundo para receber um evento.
        event, values = window.read(timeout=1)

        # Aqui ele pega a key de progresso la de cima e coloca a função update
        # para refletir o progresso atual.
        window["-PROG-"].UpdateBar(i+1)
    window.close()
    registro()

# Inserindo uma função para a janela eventos     /:2


def eventos():
    # =================================================================================================================================================#
    # Temas
    sg.theme("DarkGrey16")
    # Layout Interface
    layout = [

        # Botão de Calendário
        [sg.CalendarButton("Escolher Data", size=(
            10, 1), button_color="#2e689f"), sg.Text("-- -- -- -- -- --",
                                                     key="-DATA-")],
        # Input de nota
        [sg.T("Insira o seu evento:", size=(16, 1)), sg.I(
            key="-EVENTO-", font=("None 15"), size=(40, 1))],

        # Criar a Tabela com index, data, nota
        # Headings são os titulos, col_widths são os tamanhos das colunas
        [sg.Table(values="", headings=["Index", "Data", "Evento"],
                  key="-TABLE-", enable_events=True, size=(500, 10),
                  auto_size_columns=False, col_widths=[5, 9, 30],
                  vertical_scroll_only=False, justification="l",
                  font=("None 15"))],

        # Criar coluna, inserir botões de adicionar e deletar, dar keys a eles.
        [sg.Column([
            [sg.B("Adicionar", size=(20, 2), button_color="#2e689f"),
             sg.B("Deletar", size=(20, 2), button_color="#2e689f",
                  key="-DEL-"), sg.Button("Voltar para página anterior",
                                          size=(20, 2),
                                          button_color="#2e689f"), ]],
            element_justification="center", expand_x=True, pad=(0, (10, 0)))],
    ]
    # =================================================================================================================================================#
    # Info Janela
    window = sg.Window("Eventos", layout, size=(
        600, 400), element_justification=("left"))

    # Contadores
    eventos = []
    c = 1

    # Condições
    while True:
        button, values = window.read()

        # Fechar App
        if button == sg.WINDOW_CLOSED:
            window.close()
            break

        # Botão de Adicionar notas
        elif button == "Adicionar":
            titulo = values["-EVENTO-"]
            if titulo != "":
                tipo = "eventos"
                data = window["-DATA-"].get().split()[0]
                titulo = values["-EVENTO-"]
                nota = [[c, data, values["-EVENTO-"]]]
                eventos += nota
                window["-TABLE-"].update(eventos)
                window["-EVENTO-"].update("")
                c += 1
                bc.criar(tipo, data, titulo, id)
            else:
                sg.popup_timed("É necessário inserir uma tarefa",
                               auto_close_duration=2)

        # Botão de deletar alguma nota
        elif button == "-DEL-":
            if values["-TABLE-"]:
                index = values["-TABLE-"][0]
                del eventos[index]
                window["-TABLE-"].update(eventos)
                bc.deletar(tipo, id)

        # Voltar para pagina anterior
        elif button == "Voltar para página anterior":
            window.close()
            front2()

# Inserindo uma função para a janela alarmes     /:3


def alarmes():
    # =================================================================================================================================================#
    # Tema
    sg.theme("DarkGrey16")

    # Layout Interface
    layout = [
        [sg.Text("Aqui você marcará os seus alarmes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2),
                       button_color="#2e689f"),
             sg.Button("Sair", size=(20, 2), button_color="#2e689f")]
        ], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]
    # =================================================================================================================================================#
    # Info Janela
    window = sg.Window("Alarmes", layout, size=(700, 300),
                       element_justification=("center"))
    button, values = window.read()

    # Fechar App
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    # Voltar para página anterior
    if button == "Voltar para página anterior":
        front2()
    # =================================================================================================================================================#

# Inserindo uma função para a janela tarefas     /:4


def tarefas():
    # =================================================================================================================================================#
    # Temas
    sg.theme("DarkGrey16")
    # Layout Interface
    layout = [

        # Botão de Calendário
        [sg.CalendarButton("Escolher Data", size=(
            10, 1), button_color="#2e689f"), sg.Text("-- -- -- -- -- --",
                                                     key="-DATA-")],
        # Input de nota
        [sg.T("Insira a sua tarefa:", size=(16, 1)), sg.I(
            key="-TAREFA-", font=("None 15"), size=(40, 1))],

        # Criar a Tabela com index, data, nota
        # Headings são os titulos, col_widths são os tamanhos das colunas
        [sg.Table(values="", headings=["Index", "Data", "Tarefas"],
                  key="-TABLE-", enable_events=True, size=(500, 10),
                  auto_size_columns=False, col_widths=[5, 9, 30],
                  vertical_scroll_only=False, justification="l",
                  font=("None 15"))],

        # Criar coluna, inserir botões de adicionar e deletar, dar keys a eles.
        [sg.Column([
            [sg.B("Adicionar", size=(20, 2), button_color="#2e689f"),
             sg.B("Deletar", size=(20, 2), button_color="#2e689f",
                  key="-DEL-"), sg.Button("Voltar para página anterior",
                                          size=(20, 2),
                                          button_color="#2e689f"), ]],
            element_justification="center", expand_x=True, pad=(0, (10, 0)))],
    ]
    # =================================================================================================================================================#
    # Info Janela
    window = sg.Window("Tarefas", layout, size=(
        600, 400), element_justification=("left"))

    # Contadores
    tarefas = []
    c = 1

    # Condições
    while True:
        button, values = window.read()

        # Fechar App
        if button == sg.WINDOW_CLOSED:
            window.close()
            break

        # Botão de Adicionar notas
        elif button == "Adicionar":
            titulo = values["-TAREFA-"]
            if titulo != "":
                data = window["-DATA-"].get().split()[0]
                nota = [[c, data, values["-TAREFA-"]]]
                tarefas += nota
                window["-TABLE-"].update(tarefas)
                window["-TAREFA-"].update("")
                c += 1
            else:
                sg.popup_timed("É necessário inserir uma tarefa",
                               auto_close_duration=2)

        # Botão de deletar alguma nota
        elif button == "-DEL-":
            if values["-TABLE-"]:
                index = values["-TABLE-"][0]
                del tarefas[index]
                window["-TABLE-"].update(tarefas)

        # Voltar para pagina anterior
        elif button == "Voltar para página anterior":
            window.close()
            front2()

# Inserindo uma função para a janela lembretes   /:5


def lembretes():
    # =================================================================================================================================================#
    # Temas
    sg.theme("DarkGrey16")

    # Layout Interface
    layout = [

        # Botão de Calendário
        [sg.CalendarButton("Escolher Data", size=(
            10, 1), button_color="#2e689f"), sg.Text("-- -- -- -- -- --",
                                                     key="-DATA-")],

        # Input de nota
        [sg.T("Escreva seu lembrete:", size=(16, 1)), sg.I(
            key="-LEMBRETE-", font=("None 15"), size=(40, 1))],

        # Criar a Tabela com index, data, nota
        # Headings são os titulos, col_widths são os tamanhos das colunas
        [sg.Table(values="", headings=["Index", "Data", "Lembretes"],
                  key="-TABLE-", enable_events=True, size=(500, 10),
                  auto_size_columns=False, col_widths=[5, 9, 30],
                  vertical_scroll_only=False, justification="l",
                  font=("None 15"))],

        # Criar coluna, inserir botões de adicionar e deletar, dar keys a eles.
        [sg.Column([
            [sg.B("Adicionar", size=(20, 2), button_color="#2e689f"),
             sg.B("Deletar", size=(20, 2), button_color="#2e689f",
                  key="-DEL-"), sg.Button("Voltar para página anterior",
                                          size=(20, 2),
                                          button_color="#2e689f"), ]],
            element_justification="center", expand_x=True, pad=(0, (10, 0)))],
    ]
    # =================================================================================================================================================#
    # Info Janela
    window = sg.Window("Lembretes", layout, size=(
        600, 400), element_justification=("left"))

    # Contadores
    lembretes = []
    c = 1

    # Condições
    while True:
        button, values = window.read()

        # Fechar App
        if button == sg.WINDOW_CLOSED:
            window.close()
            break

        # Botão de Adicionar notas
        elif button == "Adicionar":
            titulo = values["-LEMBRETE-"]
            if titulo != "":
                data = window["-DATA-"].get().split()[0]
                nota = [[c, data, values["-LEMBRETE-"]]]
                lembretes += nota
                window["-TABLE-"].update(lembretes)
                window["-LEMBRETE-"].update("")
                c += 1
            else:
                sg.popup_timed("É necessário inserir uma tarefa",
                               auto_close_duration=2)

        # Botão de deletar alguma nota
        elif button == "-DEL-":
            if values["-TABLE-"]:
                index = values["-TABLE-"][0]
                del lembretes[index]
                window["-TABLE-"].update(lembretes)

        # Voltar para pagina anterior
        elif button == "Voltar para página anterior":
            window.close()
            front2()

# Inserindo janela de perfil                     /:10


def perfil():
    sg.theme("DarkGrey16")

    frame_layout = [
        [sg.Text("Usuário: Ygor")],
        [sg.Text("Nome: Ygor Gabriel")],
        [sg.Text("Email: ygbml@example.com")],
        [sg.Text("Telefone: (82) 1234-5678")],
        [sg.Text("Idade: 18")],
        [sg.Text("Gênero: Masculino")]
    ]

    # Frame que contém as informações do usuário
    frame = sg.Frame("Informações do Usuário", frame_layout, size=(400, 100))

    # Layout principal da janela
    layout = [
        [frame],
    ]
    window = sg.Window("Perfil", layout, size=(400, 300))
    button, values = window.read()
    window.close()

    if button == "Sair da conta":
        window.close()
        registro()
    elif button == sg.WINDOW_CLOSED:
        exit()


# Página de inicialização do App                 /:1
def front2():
    sg.theme("DarkGrey16")

    # Layout dos botões dentro do frame interno
    buttons_layout = [
        [sg.Button("Eventos", size=(10, 2), button_color=("#2e689f"),
                   pad=(1, 1)),
         sg.Button("Alarmes", size=(10, 2),
                   button_color=("#2e689f"), pad=(1, 1)),
         sg.Button("Tarefas", size=(10, 2),
                   button_color=("#2e689f"), pad=(1, 1)),
         sg.Button("Lembretes", size=(10, 2),
                   button_color=("#2e689f"), pad=(1, 1)),
         sg.Button("Perfil", size=(10, 2), button_color=("#2e689f"),
                   pad=(1, 1))],
    ]

    # Frame interno que contém os botões
    frame_interno = sg.Frame(None, buttons_layout)

    # Layout do frame externo que contém o frame interno
    layout_do_frame_externo = [
        [frame_interno]
    ]

    # Frame externo
    frame_externo = sg.Frame(None, layout_do_frame_externo, size=(500, 430))

    # Layout Principal
    layout = [
        [frame_externo]
    ]

    # Janela
    window = sg.Window("Calendário", layout, size=(
        500, 430), element_justification="left")
    button, values = window.read()
    window.close()

    # Condições
    if button == "Eventos":
        eventos()
    elif button == "Alarmes":
        alarmes()
    elif button == "Tarefas":
        tarefas()
    elif button == "Lembretes":
        lembretes()
    elif button == "Perfil":
        perfil()
    elif button == sg.WINDOW_CLOSED:
        exit()


# ICON PARA O APP
icon = icon()
sg.set_global_icon(icon)

id = login()
