import PySimpleGUI as sg                #Importando biblioteca PySimpleGUI para o front-end
import calendar as cal                  #Importando biblioteca calendario para um possível acréscimo no futuro

#As partes "MAINs" do código ficam no final para todo o conteudo externo, (funções) poder ser lido perfeitamente.

sg.theme("DarkGrey16")                   #Definindo o thema da janela inicial

#Função para Animação da barra de progresso     /:8
def init():
    layout = [
	#Aqui coloco a função da barra de progresso, com o valor maximo de 1000, #Na horizontal, com o tamanho (400,50)
    [sg.ProgressBar(max_value=1000, orientation="h", size=(400,50), key="-PROG-")],
    ]

    #Aqui é uma janela normal mas sem os titulos, botao de fechar ou minimizar
    window = sg.Window("", layout, size=(400,50), no_titlebar=True)

    #Looping para dar update na barra de progresso
    #Para aumentar a velocidade do update é so alterar o passo 2 para um maior
    for i in range(0,1000,2):
        #O paramentro (timeout=1) especifica que o programa aguardara 1 
        #milissegundo para receber um evento.
        event, values = window.read(timeout=1)
        
        #Aqui ele pega a key de progresso la de cima e coloca a função update
        #para refletir o progresso atual.
        window["-PROG-"].UpdateBar(i+1)
    window.close()
    front()

#Inserindo uma função para a janela eventos     /:3
def eventos():
    #=================================================================================================================================================#
    #Tema
    sg.theme("DarkGrey16")

    #Layout Interface
    layout = [
        [sg.Text("Aqui você marcará os seus eventos", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Marcar novo evento", size=(20, 2), button_color="#2e689f"), sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
           
    ]
    #=================================================================================================================================================#
    #Info Janela
    window = sg.Window("Eventos", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    
    #Fechar App
    if button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    
    #Voltar para página anterior
    if button == "Voltar para página anterior":
        front2()
    elif button == "Marcar novo evento":
        window.close()

    
    
    #=================================================================================================================================================#

#Inserindo uma função para a janela alarmes     /:4
def alarmes():
    #=================================================================================================================================================#
    #Tema
    sg.theme("DarkGrey16")

    #Layout Interface
    layout = [
        [sg.Text("Aqui você marcará os seus alarmes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]
    #=================================================================================================================================================#
    #Info Janela
    window = sg.Window("Alarmes", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    
    #Fechar App
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    #Voltar para página anterior
    if button == "Voltar para página anterior":
        front2()
    #=================================================================================================================================================#

#Inserindo uma função para a janela tarefas     /:5
def tarefas():
    #=================================================================================================================================================#
    #Tema
    sg.theme("DarkGrey16")
    
    #Layout Interface
    layout = [
        [sg.Text("Aqui você marcará as suas tarefas", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]
    #=================================================================================================================================================#
    #Info Janela
    window = sg.Window("Tarefas", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    
    #Fechar App
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    
    #Voltar para página anterior
    if button == "Voltar para página anterior":
        front2()
    #=================================================================================================================================================#

#Inserindo uma função para a janela anotações   /:6
def anotações():
    #=================================================================================================================================================#
    #Temas
    sg.theme("DarkGrey16")

    #Layout Interface
    layout = [
        [sg.Text("Aqui você marcará as suas anotações", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]
    #=================================================================================================================================================#
    #Info Janela
    window = sg.Window("Anotações", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    
    #Fechar App
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    
    #Voltar para pagina anterior
    if button == "Voltar para página anterior":
        front2()
    #=================================================================================================================================================#

#Inserindo uma função para a janela lembretes   /:7
def lembretes():
    #=================================================================================================================================================#
    #Temas
    sg.theme("DarkGrey16")

    #Layout da Interface
    layout = [
        [sg.Text("Aqui você marcará os seus lembretes", font=("Arial", 20))],
        [sg.Column([
            [sg.Button("Voltar para página anterior", size=(20, 2), button_color="#2e689f"), sg.Button("Sair", size=(20, 2), button_color="#2e689f")]], element_justification="center", expand_x=True, pad=(0, (220, 0)))],
    ]
    #=================================================================================================================================================#
    #Info Janelas
    window = sg.Window("Lembretes", layout, size=(700, 300), element_justification=("center"))
    button, values = window.read()
    
    #Fechar App
    if button == "Sair" or button == sg.WINDOW_CLOSED:
        exit()
    window.close()
    
    #Voltar para página anterior
    if button == "Voltar para página anterior":
        front2()
    #=================================================================================================================================================#

#Página de inicialização do App                 /:1
def front():
    #=================================================================================================================================================#
    #Inserindo uma lista para definir as características da minha janela inicial
    flayout = [                                                                                     
    
        #Utilizando a função sg.Text para colocar texto na paginal inicial, aqui eu consigo manipular o texto, tamanho, fonte.
        [sg.Text("Seja Bem-vindo!", font=("Arial", 13))],
        [sg.Text("Insira o seu nome", font=("Arial", 13))],            
        [sg.Input(key="-NAME-", size=(20,2))],
        #Utilizando a função Column para criar uma coluna na interface gráfica, ela serve para organizar elementos GUI, como textos, botões, entradas, etc
        #Aqui nesse caso, eu queria fazer com que os botões ficassem isolados na parte inferior da janela por isso usei ela.
        [sg.Column([                                            
            #Defini a cor dos botões, o seu nome, e sua cordenada na interface
            
            [sg.Button("Ver Calendário", button_color="#2e689f"), sg.Button("Sair do aplicativo", button_color=("#2e689f"))],
        ], element_justification="center", expand_x=True, pad=(0, (80, 0)))],
    
    ]
    #=================================================================================================================================================#
    #Aqui coloco a variavel window para armazendar a função window que basicamente é onde eu irei colocar todo o layout de cima dentro de uma janela.
    #O layout era basicamente as características de interação com o usuário, aqui são as características próprias da janela
    #Defino o nome, insiro o layout feito mais acima, defino o tamanho da janela, e centralizo o texto no meio.
    window = sg.Window("Calendary Project App", flayout, size=(500, 200), element_justification="center")
    
    #Aqui eu defino 2 variáveis, e elas servem basicamente para quantificar esses botões, ao clica-los por exemplo. A função "window.read()" é para ler essas variáveis
    button, values = window.read() 
    
    #Aqui é um bloco de condição onde eu redireciono os meus botões inseridos anteriormente
    #E basicamente ele funciona da seguinte forma, se a função acima ler que eu cliquei em "Visualizar Calendário", serei redirecionado para a página main do app
    #Entretanto, caso eu clicar no "Sair do Aplicativo", ele fechará o app.
    #Podem se perguntar pra que esse tal de "sg.WINDOW_CLOSER", ele serve para fazer com que o X de fechar janelas, que a gnt usa pra fechar tudo, funcione corretamente.
    
    if button == "Ver Calendário":
        window.close()
        front2()
    elif button == "Sair do aplicativo" or button == sg.WINDOW_CLOSED:
        exit()
    #=================================================================================================================================================#

#Pagina Inicial /  "Página Main                 /:2
def front2():
    #=================================================================================================================================================#
    #Setando o tema
    sg.theme("DarkGrey16")
    
    #Definindo uma coluna para separar a tela
    Coluna1 = [
        
        #Definindo botões, seus respecitivos tamanhos e cores, aqui podemos colocar qualquer cor hexadecimal possível.
        [sg.Button("Eventos", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Alarmes", size=(20, 2), button_color=("#2e689f") )],
        [sg.Button("Tarefas", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Anotações", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Lembretes", size=(20, 2), button_color=("#2e689f"))],
        [sg.Button("Sair", size=(20, 2), button_color=("#2e689f"))]
    ]
    #Definindo o layout para chamar a coluna , sg.VerticalSeparator() é para tração uma linha na tela
    layout = [
        [sg.Col(Coluna1), sg.VerticalSeparator()]
    ]
    #=================================================================================================================================================#
    #Definindo as características próprias da janela main, titulo, tamanho, e cordenada na interface
    window = sg.Window("Calendário", layout, size=(700, 300), element_justification="left")
    
    #Lendo as variáveis
    button, values = window.read()
    
    #Essa função "window.close()" basicamente fecha a janela atual quando for para uma outra janela, para n ficar com 2 janelas abertas
    window.close()
    
    #Inserindo condicionais de botões, basicamente é para redirecionar paginas ao clicar nos seus respectivos botão, ALARMES - ALARMES, SAIR - FECHAR APP
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
    #=================================================================================================================================================#


init()


