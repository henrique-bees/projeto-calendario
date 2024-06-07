import backend as bc
import PySimpleGUI as sg
import sqlite3 as sq
import time
import threading
from random import choice

# Inserindo função de login                     
def login():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário: "), sg.I(key="-NAME-")],
        [sg.T("Senha:   "), sg.I(key="-SENHA-", password_char="*", size=(36,2)),sg.Button("∞", key="-SHOW_PASSWORD-", 
                                                                                          border_width=0, button_color=("#343434"))],
        [sg.HorizontalSeparator()],
        [sg.Button("Esqueci minha senha", button_color="#4169E1")],
    ]

    layout = [
        [sg.Frame("Login", frame)],
        [sg.Ok(button_color="#4169E1"), sg.B(
            "Voltar", button_color="#4169E1")],

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
        elif event == "-SHOW_PASSWORD-":
                password_input = window['-SENHA-']
                if password_input.Widget.cget("show") == "*":  
                    password_input.Widget.config(show="")
                else:
                    password_input.Widget.config(show="*")
        elif event == sg.WINDOW_CLOSED:
            exit()
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
                               auto_close_duration=5, button_color="#4169E1")
                (usuario, senha)
                window.close()
                global id
                id = busca[2]
                front2()
            else:
                sg.popup("Usuário ou senha incorretos",
                         button_color="#4169E1")

# Inserindo função de registro
def registro():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "), sg.I(key="-NAME-")],
        [sg.T("Senha:               "), sg.I(key="-SENHA-",
                                             password_char="*", size=(30,2)),sg.Button("∞", key="-SHOW_PASSWORD-", border_width=0, button_color="#343434")],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-",
                                        password_char="*", size=(30,2)),sg.Button("∞", key="-SHOW_CONFIRM_PASSWORD-", border_width=0, button_color="#343434")],
        [sg.HorizontalSeparator()],
        [sg.Button("Já possuo um login", button_color="#4169E1"),
         sg.VerticalSeparator(),
         sg.Text("""Uma letra maíuscula | Uma letra minúscula\nUm caractere especial | Um número\nMínimo 8 caracteres | Máximo 16 caracteres""", font=("Arial", 7)),
         sg.VerticalSeparator()]
    ]

    layout = [
        [sg.Frame("Registro", frame)],
        [sg.Ok(button_color="#4169E1"), sg.B(
            "Cancel", button_color="#4169E1")],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0))
        )]
    ]
    window = sg.Window("Registro", layout, size=(400, 210))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
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
        elif event == "Já possuo um login":
            window.close()
            login()
            break
        if event == "Ok":
            usuario = values["-NAME-"].strip()
            senha = values["-SENHA-"]
            senha2 = values["-SENHA2-"]
            massa = bc.verificar_registro(usuario)
            if massa == "vazio":
                sg.popup_timed(
                    "O usuário precisa estar preenchido", auto_close_duration=5, button_color="#4169E1"
                )
            elif massa == "invalido":
                sg.popup_timed(
                    "Usuário já foi cadastrado", auto_close_duration=5, button_color="#4169E1"
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
                                       auto_close=5, button_color="#4169E1")
                        login()
                    else:
                        sg.popup_timed(
                            "Senha invalida, as senhas devem possuir "
                            "pelo menos uma letra maiuscula, uma "
                            "minuscula, um numero, um caractere "
                            "especial, e ter entre 8 e 16 caracteres",
                            auto_close_duration=5, button_color="#4169E1")
                else:
                    sg.popup_timed(
                        "As senhas não coincidem ou o usuário é vazio,"
                        " por favor, tente novamente",
                        auto_close_duration=5, button_color="#4169E1")

# Inserindo função de criar uma nova senha
def nova_senha():
    sg.theme("DarkGrey16")
    frame = [
        [sg.T("Usuário:             "),
         sg.I(key="-USUARIO-")],
        [sg.HorizontalSeparator()],
        [sg.T("Senha:               "),
         sg.I(key="-SENHA-", password_char="*", size=(29,2)),sg.Button("∞", key="-SHOW_PASSWORD-", 
                                                                                          border_width=0, button_color=("#343434"))],
        [sg.T("Confirmar Senha:"), sg.I(key="-SENHA2-", password_char="*", size=(29,2)),sg.Button("∞", key="-SHOW_CONFIRM_PASSWORD-", 
                                                                                          border_width=0, button_color=("#343434"))],
    ]

    layout = [
        [sg.Frame("Nova Senha", frame)],
        [sg.Ok(button_color="#4169E1"), sg.B(
            "Voltar", button_color="#4169E1")],

        [sg.Column([
            [sg.T("Retirando Marca d'água")]],
            expand_x=True, pad=(0, (50, 0)
                                ))]
    ]
    window = sg.Window("Recuperação de senha", layout, size=(400, 163))
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
                                   auto_close_duration=5, button_color="#4169E1")
                    login()
            else:
                sg.popup_timed(
                    "As senhas não coincidem ou o usuário é vazio, por favor,"
                    " tente novamente",
                    auto_close_duration=5, button_color="#4169E1")

# Armazenando o icon base64
def icon():
    return b"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kUM6tv9sV3TY6GOtOnco1pTKrIE9O7hwRHLU3MatO/k23pTOtFE7PHrsOm4yM0+nPLum66fQtIFjWLp4tnrgtEHDvZL29ZjS7ypzRk2bN3Lk0OE6Pj/KO3Tqv2mjxhnHuYcde+sRiGCCCi7IYIMOPghhhBJWY6CBE16IYYYabshhhx4WWOGBH45IYokmnogigiFWmGKLLr4IY4wRrhiijDbeiGOON9K4oo4+/ghkkBDy2KOQRh6JZJItEcmikk4+CaWMTNIYZZVWXrnhlDxiyWWXXrqnJZFfjklmmRSGuaWZaq5pJZpasglnnEG6iaacdt4JI5104slnnx3qCaifgg76IKDShgJAaKKKMndoo4guCmmkZzrqqKSWJkpppplcyqmdmn7KSaeieglqqaaeimqqqq7KaquuvgprrLLOSmuttt6Ka6667sprr77+Cmywwg5LbLHGHotsssouy2yzzj4LbbTSTktttdZei2222m7LbbfefgtuuOKOS2655p6Lbrrqrstuu+6+C2+88s5Lb7323otvvvruy2+//v4LcMACD0xwwQYfjHDCCi/McMMOPwxxxBJPTHHFFl+MccYab8xxxx5/DHLIIo9Mcskmn4xyyiqvzG0gADs="

# Função para Animação da barra de progresso
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

# Inserindo uma função para a janela eventos
def eventos():
    # Temas
    sg.theme("DarkGrey16")
    # Layout Interface
    tipo = "eventos"
    conteudo = bc.ler_salvos(tipo, id)
    layout = [

        # Botão de Calendário
        [sg.CalendarButton("Escolher Data", size=(
            10, 1), button_color="#4169E1"), sg.Text("-- -- -- -- -- --",
                                                     key="-DATA-")],
        # Input de nota
        [sg.T("Insira o seu evento:", size=(16, 1)), sg.I(
            key="-EVENTO-", font=("None 15"), size=(40, 1))],

        # Criar a Tabela com index, data, nota
        # Headings são os titulos, col_widths são os tamanhos das colunas
        [sg.Table(values=conteudo, headings=["Index", "Data", "Evento"],
                  key="-TABLE-", enable_events=True, size=(500, 10),
                  auto_size_columns=False, col_widths=[5, 9, 30],
                  vertical_scroll_only=False, justification="l",
                  font=("None 15"))],

        # Criar coluna, inserir botões de adicionar e deletar, dar keys a eles.
        [sg.Column([
            [sg.B("Adicionar", size=(20, 2), button_color="#4169E1"),
             sg.B("Deletar", size=(20, 2), button_color="#4169E1",
                  key="-DEL-"), sg.Button("Voltar para página anterior",
                                          size=(20, 2),
                                          button_color="#4169E1"), ]],
            element_justification="center", expand_x=True, pad=(0, (10, 0)))],
    ]

    # Info Janela
    window = sg.Window("Eventos", layout, size=(
        600, 400), element_justification=("left"))

    # Condições
    while True:
        button, values = window.read()

        # Fechar App
        if button == sg.WINDOW_CLOSED:
            window.close()
            quit()

        # Botão de Adicionar notas
        elif button == "Adicionar":
            titulo = values["-EVENTO-"]
            if titulo != "":
                data = window["-DATA-"].get().split()[0]
                titulo = values["-EVENTO-"]
                c = bc.criar(tipo, data, titulo, id)
                nota = [[c, data, values["-EVENTO-"]]]
                conteudo += nota
                window["-TABLE-"].update(conteudo)
                window["-EVENTO-"].update("")
            else:
                sg.popup_timed("É necessário inserir uma tarefa",
                               auto_close_duration=2)

        # Botão de deletar alguma nota
        elif button == "-DEL-":
            if values["-TABLE-"]:
                index = values["-TABLE-"][0] + 1
                bc.deletar(tipo, index, id)
                del conteudo[index]
                window["-TABLE-"].update(conteudo)
                window["-TABLE-"].update(index)
                window["-EVENTO-"].update("")

        # Voltar para pagina anterior
        elif button == "Voltar para página anterior":
            window.close()
            front2()

# Inserindo uma função para a janela alarmes
def alarmes():
    # Tema
    sg.theme("DarkGrey16")

    # Layout Interface
    layout = [
        [sg.Text("Aqui você marcará os seus alarmes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2),
                       button_color="#4169E1"),
             sg.Button("Sair", size=(20, 2), button_color="#4169E1")]
        ], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]

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

# Inserindo uma função para a janela anotações
def anotações():
    # Temas
    sg.theme("DarkGrey16")
    # Layout Interface

    frame_layout = [
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.Button("Adicionar", button_color="#4169E1", size=(12, 2), pad=(9, 1)),
         sg.Button("Deletar", button_color="#4169E1",
                   size=(12, 2), pad=(9, 2)),
         sg.Button("Voltar", button_color="#4169E1", size=(12, 2), pad=(9, 2))]
    ]

    layout = [
        [sg.Frame(None, frame_layout, size=(400, 400))]

    ]

    # Info Janela
    window = sg.Window("Anotações", layout, size=(
        400, 400), element_justification=("left"))

    button, values = window.read()

    if button == sg.WINDOW_CLOSED:
        window.close()
        exit()
    elif button == "Adicionar":
        window.close()

        def novo_texto():
            frame_layout = [
                
                [sg.Text("Nome do texto: ", font=("Arial", 10)),
                 sg.Input(key="-TAG-")],
                [sg.HorizontalSeparator()],
                [sg.Button("Salvar", button_color="#4169E1", size=(10,1), pad=(23,2)),
                 sg.Button("Cancelar", button_color="#4169E1", size=(10,1), pad=(20,2))]
            ]

            layout = [
                [sg.Frame("Criar novo texto", frame_layout, size=(300, 200))]
            ]

            window = sg.Window("Novo Texto", layout, size=(300, 100))
            button, values = window.read()

            # """elif button == "Deletar":"""
            if button == sg.WINDOW_CLOSED:
                window.close()
                exit()
            elif button == "Voltar":
                window.close()
                front2()
        novo_texto()

# Inserindo janela de edição de perfil
def editar_perfil():
    sg.theme("DarkGrey16")

    frame_layout = [
        [sg.Text("Usuário: ", size=(10, 1)), sg.Input(
            key="-USUARIO-", font=("None 15"), size=(30, 1))],
        [sg.Text("Nome: ", size=(10, 1)), sg.Input(
            key="-NOME-", font=("None 15"), size=(30, 1))],
        [sg.Text("Email: ", size=(10, 1)), sg.Input(
            key="-EMAIL-", font=("None 15"), size=(30, 1))],
        [sg.Text("Telefone: ", size=(10, 1)), sg.Input(
            key="-TELEFONE-", font=("None 15"), size=(30, 1))],
        [sg.Text("Idade: ", size=(10, 1)), sg.Input(
            key="-IDADE-", font=("None 15"), size=(30, 1))],
        [sg.Text("Gênero: ", size=(10, 1)), sg.Input(
            key="-GENERO-", font=("None 15"), size=(30, 1))],
        [sg.HorizontalSeparator()],
        [sg.Button("Salvar alterações", size=(15, 2), button_color="#4169E1",
                   pad=(30, 1)),
         sg.Button("Visualizar Perfil", size=(15, 2), button_color="#4169E1",
                   pad=(15, 1))]
    ]

    # Frame que contém as informações do usuário
    frame = sg.Frame("Informações do Usuário", frame_layout, size=(400, 300))

    # Layout principal da janela
    layout = [
        [frame],
    ]
    window = sg.Window("Editar Perfil", layout, size=(400, 276))
    button, values = window.read()
    window.close()

    if button == sg.WINDOW_CLOSED:
        exit()
    elif button == "Visualizar Perfil":
        window.close()
        perfil()
    elif button == "Salvar alterações":
        ""

# Inserindo janela de perfil
def perfil():
    sg.theme("DarkGrey16")

    frame_layout = [
        [sg.Text("Usuário: ", size=(10, 1)), sg.Input(
            key="-USUARIO-", font=("None 15"), size=(30, 1))],
        [sg.Text("Nome: ", size=(10, 1)), sg.Input(
            key="-NOME-", font=("None 15"), size=(30, 1))],
        [sg.Text("Email: ", size=(10, 1)), sg.Input(
            key="-EMAIL-", font=("None 15"), size=(30, 1))],
        [sg.Text("Telefone: ", size=(10, 1)), sg.Input(
            key="-TELEFONE-", font=("None 15"), size=(30, 1))],
        [sg.Text("Idade: ", size=(10, 1)), sg.Input(
            key="-IDADE-", font=("None 15"), size=(30, 1))],
        [sg.Text("Gênero: ", size=(10, 1)), sg.Input(
            key="-GENERO-", font=("None 15"), size=(30, 1))],
        [sg.HorizontalSeparator()],
        [sg.Button("Sair da conta", size=(10, 2), button_color="#4169E1",
                   pad=(16, 1)),
         sg.Button("Editar Perfil", size=(10, 2),
                   button_color="#4169E1", pad=(16, 1)),
         sg.Button("Voltar", size=(10, 2), button_color="#4169E1",
                   pad=(16, 1))]

    ]
    frame = sg.Frame("Informações do Usuário", frame_layout, size=(400, 300))

    layout = [
        [frame]
    ]
    window = sg.Window("Perfil", layout, size=(400, 276))
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        exit()
    elif event == "Sair da conta":
        window.close()
        login()
    elif event == "Editar Perfil":
        window.close()
        editar_perfil()
    elif event == "Voltar":
        window.close()
        front2()

# Inserindo função de verificação de autenticidade
def verificação():
    sg.theme("Darkgrey16")
    frame_layout = [
        [sg.Text("Usuário:", size=(7, 1)), sg.Input(key="-USUARIO-")],
        [sg.HorizontalSeparator()],
        [sg.Text("Senha:", size=(7, 1)), sg.Input(key="-SENHA-")],

        [sg.Button("Ok"), sg.Button("Cancel")],

    ]

    layout = [
        [sg.Frame(None, frame_layout)],
    ]
    window = sg.Window("Verificação", layout, size=(300, 115))
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        exit()
    elif event == "Ok":
        window.close()
        sg.popup("Informações modificadas com sucesso")
        perfil()
    elif event == "Cancel":
        sg.popup("Tentativa de edição mal sucedida")
        window.close()
        front2()

# Página de inicialização do App
def front2():
    sg.theme("DarkGrey16")

    frases = ["Acredite em si mesmo e tudo será possível.", "O sucesso é a soma de pequenos esforços repetidos dia após dia.", "Você é mais forte do que imagina e pode fazer mais do que pensa.", "Cada dia é uma nova oportunidade para ser melhor.", "Desafios são o que fazem a vida interessante e superá-los é o que faz a vida significativa.", "A persistência é o caminho do êxito.", "Sonhe grande, comece pequeno, mas comece.", "A vida começa no final da sua zona de conforto.", "O segredo do sucesso é começar antes de estar pronto.", "A melhor maneira de prever o futuro é criá-lo.", "Acredite que você pode e você já está no meio do caminho.", "O único lugar onde o sucesso vem antes do trabalho é no dicionário.", "Não espere por oportunidades, crie-as.", "Tudo o que você sempre quis está do outro lado do medo.", "A jornada de mil milhas começa com um único passo.", "Você é capaz de coisas incríveis.", "Acredite que vale a pena viver e a sua crença ajudará a criar o fato.", "Seja a mudança que você quer ver no mundo.", "O fracasso é apenas a oportunidade de começar de novo com mais inteligência.", "Nunca é tarde demais para ser o que você poderia ter sido.", "O único limite para a nossa realização de amanhã são as nossas dúvidas de hoje.", "Coragem não é a ausência do medo, mas a conquista dele.", "Você nunca saberá do que é capaz até tentar.", "Transforme seus sonhos em metas e suas metas em realidade.", "A maior glória em viver não está em nunca cair, mas em levantar cada vez que caímos.",
              "Faça hoje o que outros não querem, para ter amanhã o que outros não terão.", "O sucesso é ir de fracasso em fracasso sem perder o entusiasmo.", "A maior aventura que você pode ter é viver a vida dos seus sonhos.", "Acredite nos seus sonhos e eles podem se tornar realidade.", "Você não precisa ser perfeito para começar, mas precisa começar para ser perfeito.", "Você é o autor da sua própria história.", "Acredite no seu potencial ilimitado.", "Não importa o quão devagar você vá, desde que você não pare.", "Seu único limite é você mesmo.", "O futuro pertence àqueles que acreditam na beleza dos seus sonhos.", "Não deixe que os erros de ontem ocupem muito do seu hoje.", "Você é a média das cinco pessoas com quem passa mais tempo.", "Tenha fé em si mesmo e nos seus sonhos.", "Cada sonho que você deixa para trás é um pedaço do seu futuro que deixa de existir.", "Se você pode sonhar, você pode realizar.", "A diferença entre quem você é e quem você quer ser é o que você faz.", "Não espere por circunstâncias perfeitas, crie-as.", "Você não pode mudar seu passado, mas pode mudar seu futuro.", "A melhor maneira de começar é parar de falar e começar a fazer.", "Acredite que você pode, e você já está no meio do caminho.", "O sucesso não é final, o fracasso não é fatal: é a coragem de continuar que conta.", "Se você quer algo que nunca teve, você precisa fazer algo que nunca fez.", "A vida é 10% o que acontece com você e 90% como você reage a isso.", "Você é mais forte do que pensa e mais capaz do que imagina.", "Nunca subestime o poder dos seus sonhos."]

    def update(window):
        frase_aleatoria = choice(frases)
        window['-FRASE-'].update(frase_aleatoria)

    # Layout dos botões dentro do frame interno
    buttons_layout = [
        [sg.Button("Eventos", size=(10, 2), button_color=("#4169E1"),
                   pad=(1, 1)),
         sg.Button("Alarmes", size=(10, 2),
                   button_color=("#4169E1"), pad=(1, 1)),
         sg.Button("Anotações", size=(10, 2),
                   button_color=("#4169E1"), pad=(1, 1)),
         sg.Button("Perfil", size=(10, 2), button_color=("#4169E1"),
                   pad=(1, 1))],
    ]

    # Frame interno que contém os botões
    frame_interno = sg.Frame(None, buttons_layout)

    # Layout do frame externo que contém o frame interno
    layout_do_frame_externo = [
        [frame_interno],
        [sg.HorizontalSeparator()],
        [sg.VPush()],
        [sg.Column([
            [sg.HorizontalSeparator()],
            [sg.Button("Frase do dia", size=(10, 2), button_color="#006400", pad=(8, 5)),
             sg.Multiline("", size=(50, 2), disabled=True, no_scrollbar=True, auto_size_text=True, key='-FRASE-')]
        ], expand_x=True, pad=(0, 0, 0, 0))]]
    # Frame externo
    frame_externo = sg.Frame(None, layout_do_frame_externo, size=(500, 430))

    # Layout Principal
    layout = [
        [frame_externo],
    ]

    # Janela
    window = sg.Window("Agenda", layout, size=(
        400, 430), element_justification="left", finalize=True)

    update(window)

    while True:
        button, values = window.read()
        # Condições
        if button == "Eventos":
            window.close()
            eventos()
        elif button == "Alarmes":
            window.close()
            alarmes()
        elif button == "Anotações":
            window.close()
            anotações()
        elif button == "Perfil":
            window.close()
            perfil()
        elif button == "Frase do dia":
            update(window)
        elif button == sg.WINDOW_CLOSED:
            exit()


# ICON PARA O APP
icon = icon()
sg.set_global_icon(icon)

nova_senha()
