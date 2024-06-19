import backend as bc
import login as lg
import PySimpleGUI as sg
import sqlite3 as sq
import time
from datetime import datetime
from random import choice
import threading


# Função para Animação da barra de progresso
def loading():
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

# Inserindo uma função para a janela eventos


def eventos():
    # Temas
    sg.theme("DarkGrey16")
    # Layout Interface
    conteudo = bc.ler_eventos(id)
    layout = [

        # Botão de Calendário
        [sg.CalendarButton("Escolher Data", format='%Y-%m-%d', size=(
            10, 1), button_color="#4169E1", target="-DATA-"), sg.Multiline(
            font=("None 15"), size=(10, 1), disabled=True, no_scrollbar=True,
            key="-DATA-"),
         sg.Text('Hora'), sg.Combo(
             [f'{i:02d}' for i in range(24)], button_arrow_color="#4169E1",
             key='-HORA-', size=(5, 1), readonly=True),
         sg.Text('Minuto'), sg.Combo(
             [f'{i:02d}' for i in range(60)], button_arrow_color="#4169E1",
             key='-MINUTO-', size=(5, 1), readonly=True)],
        # Input de nota
        [sg.T("Insira o seu evento:", size=(16, 1)), sg.I(
            key="-EVENTO-", font=("None 15"), size=(40, 1))],


        # Criar a Tabela com index, data, nota
        # Headings são os titulos, col_widths são os tamanhos das colunas
        [sg.Table(values=conteudo, headings=["Index", "Data / Hora", "Evento"],
                  key="-TABLE-", sbar_arrow_color="#4169E1",
                  enable_events=True, size=(500, 10), auto_size_columns=False,
                  col_widths=[5, 14, 23], vertical_scroll_only=True,
                  justification="l", font=("None 15"))],

        # Criar coluna, inserir botões de adicionar e deletar, dar keys a eles.
        [sg.Column([
            [sg.B("Adicionar", size=(20, 2), button_color="#4169E1",
                  bind_return_key=True),
             sg.B("Deletar", size=(20, 2), button_color="#4169E1",
                  key="-DEL-"),
             sg.Button("Voltar para página anterior", size=(20, 2),
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
            exit()

        # Botão de Adicionar notas
        elif button == "Adicionar":
            titulo = values["-EVENTO-"]
            if titulo != "":
                data_selecionada = window["-DATA-"].get().split()[0]
                hora = values["-HORA-"]
                minuto = values["-MINUTO-"]
                hora_selecionada = f"{hora}:{minuto}"
                if hora != "" and minuto != "":
                    agora = datetime.now()
                    hora_atual = agora.strftime("%H:%M")
                    selected_date = datetime.strptime(
                        data_selecionada, '%Y-%m-%d').date()
                    selected_hour = datetime.strptime(hora_selecionada,
                                                      '%H:%M')
                    current_hour = datetime.strptime(hora_atual, '%H:%M')
                    if selected_date < datetime.now().date() or \
                            (selected_date == datetime.now().date() and
                             selected_hour < current_hour):
                        sg.popup_no_buttons(
                            "Essa data já passou.\n"
                            "Selecione uma data no futuro.",
                            title="ERRO")
                    else:
                        titulo = values["-EVENTO-"]
                        data = data_selecionada + " / " + hora_selecionada
                        c = bc.criar_eventos(data, titulo, id)
                        nota = [(c, data, values["-EVENTO-"])]
                        conteudo += nota
                        window["-TABLE-"].update(conteudo)
                        window["-EVENTO-"].update("")
                else:
                    sg.popup_no_buttons("É necessário inserir um horario",
                                        title="ERRO")
            else:
                sg.popup_no_buttons("É necessário inserir uma tarefa",
                                    title="ERRO")

        # Botão de deletar alguma nota
        elif button == "-DEL-":
            if values["-TABLE-"]:
                index = values["-TABLE-"][0] + 1
                bc.deletar(index, id)
                conteudo = bc.ler_eventos(id)
                window["-TABLE-"].update(conteudo)
                window["-EVENTO-"].update("")

        # Voltar para pagina anterior
        elif button == "Voltar para página anterior":
            window.close()
            front2()

        # Sistema de notificações


# Inserindo uma função para a janela relógio


def relógio():
    sg.theme("DarkGrey16")

    # Frame com os botões
    buttons_layout = [
        [sg.Button("Cronômetro", button_color="#4169E1", size=(11, 2)),
         sg.Button("Temporizador", button_color="#4169E1", size=(11, 2)),
         sg.Button("Alarmes", button_color="#4169E1", size=(11, 2))]
    ]
    buttons_frame = sg.Frame(None, buttons_layout,
                             size=(320, 50), relief='sunken')

    frame_layout_hora = [
        [sg.Column([
            [sg.Frame(None,
                      [[sg.Text("00", font=("Arial", 30),
                                key='-HORAS_DIGITS-')]],
                      size=(64, 60), relief='ridge'),
             sg.Text(":", font=("Arial", 20)),
             sg.Frame(None, [[sg.Text("00", font=("Arial", 30),
                                      key='-MINUTOS_DIGITS-')]],
                      size=(64, 60), relief='ridge'),
             sg.Text(":", font=("Arial", 20)),
             sg.Frame(None, [[sg.Text("00", font=("Arial", 30),
                                      key='-SEGUNDOS_DIGITS-')]],
                      size=(64, 60), relief='ridge')]],
            # Reduziu a distância superior da coluna
            expand_x=True, pad=(15, 15, 15, 0))]
    ]
    frame_hora = sg.Frame(None, frame_layout_hora)

    digits_frame_layout = [
        [sg.Column([
            [sg.Text("HORA ATUAL", font=("Arial", 20))]], expand_x=True,
            pad=(60, 20, 0, 10))],
        [frame_hora],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", button_color="#4169E1",
                   size=(10, 2), pad=(120, 0))]

    ]
    digits_frame = sg.Frame(None, digits_frame_layout,
                            size=(320, 400), relief='sunken')

    frame_layout_externo = [
        [buttons_frame],
        [digits_frame]
    ]
    frame_global_layout = [
        [sg.Frame(None, frame_layout_externo)]
    ]

    layout = [
        [frame_global_layout]
    ]

    window = sg.Window("Relógio", layout, size=(370, 380))

    while True:
        event, values = window.read(timeout=1000)  # Atualizar a cada segundo
        if event == sg.WINDOW_CLOSED:
            exit()
        elif event == "Voltar":
            window.close()
            front2()
        elif event == "Cronômetro":
            window.close()
            cronômetro()
        elif event == "Temporizador":
            window.close()
            temporizador()
        elif event == "Alarmes":
            window.close()
            alarmes()
        # Atualizar a hora
        current_time = time.localtime()
        # Atualizar os dígitos individuais de horas, minutos e segundos
        window['-HORAS_DIGITS-'].update('{:02d}'.format(current_time.tm_hour))
        window['-MINUTOS_DIGITS-'].update('{:02d}'.format(current_time.tm_min))
        window['-SEGUNDOS_DIGITS-'].update(
            '{:02d}'.format(current_time.tm_sec))

#   Inserindo uma função para a janela cronômetro


def cronômetro():
    sg.theme("DarkGrey16")

    # Frame com os botões
    buttons_layout = [
        [sg.Button("INICIAR", key='-START-', button_color="#4169E1",
                   size=(11, 2)),
         sg.Button("PAUSAR", key='-PAUSE-',
                   button_color="#4169E1", size=(11, 2)),
         sg.Button("RESETAR", key='-RESET-', button_color="#4169E1",
                   size=(11, 2))]
    ]
    buttons_frame = sg.Frame(None, buttons_layout,
                             size=(320, 50), relief='sunken')

    frame_layout_hora = [
        [sg.Column([
            [sg.Frame(None,
                      [[sg.Text("00", font=("Arial", 30),
                                key='-HORAS_DIGITS-')]],
                      size=(64, 60), relief='ridge'),
             sg.Text(":", font=("Arial", 20)),
             sg.Frame(None,
                      [[sg.Text("00", font=("Arial", 30),
                                key='-MINUTOS_DIGITS-')]],
                      size=(64, 60), relief='ridge'),
             sg.Text(":", font=("Arial", 20)),
             sg.Frame(None,
                      [[sg.Text("00", font=("Arial", 30),
                                key='-SEGUNDOS_DIGITS-')]],
                      size=(64, 60), relief='ridge')]],
            # Reduziu a distância superior da coluna
            expand_x=True, pad=(15, 15, 15, 0))]
    ]
    frame_hora = sg.Frame(None, frame_layout_hora)

    digits_frame_layout = [
        [sg.Column([
            [sg.Text("CRONÔMETRO", font=("Arial", 20))]], expand_x=True,
            pad=(50, 10, 0, 10))],
        [frame_hora],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", button_color="#4169E1",
                   size=(10, 2), pad=(120, 0))]
    ]
    digits_frame = sg.Frame(None, digits_frame_layout,
                            size=(320, 400), relief='sunken')

    frame_layout_externo = [
        [buttons_frame],
        [digits_frame]
    ]
    frame_global_layout = [
        [sg.Frame(None, frame_layout_externo)]
    ]

    layout = [
        [frame_global_layout]
    ]

    window = sg.Window("Cronômetro", layout, size=(
        370, 310), return_keyboard_events=True)

    # Variáveis de controle do cronômetro
    start_time = 0
    paused_time = 0
    running = False

    while True:
        event, values = window.read(timeout=10)  # Atualizar a cada segundo

        if event == sg.WINDOW_CLOSED:
            exit()
        elif event == "Voltar":
            window.close()
            relógio()
        elif event == '-START-':
            if not running:
                start_time = time.time() - paused_time
                running = True
        elif event == '-PAUSE-':
            if running:
                paused_time = time.time() - start_time
                running = False
        elif event == '-RESET-':
            start_time = 0
            paused_time = 0
            running = False
            window['-HORAS_DIGITS-'].update('00')
            window['-MINUTOS_DIGITS-'].update('00')
            window['-SEGUNDOS_DIGITS-'].update('00')
        elif not running and event == ' ':
            window['-START-'].click()
        elif event == 'Escape':
            window["-RESET-"].click()
        elif running and event == ' ':
            window['-PAUSE-'].click()

        elif running:
            elapsed_time = time.time() - start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            window['-HORAS_DIGITS-'].update('{:02d}'.format(int(hours)))
            window['-MINUTOS_DIGITS-'].update('{:02d}'.format(int(minutes)))
            window['-SEGUNDOS_DIGITS-'].update('{:02d}'.format(int(seconds)))


def format_time(hours, minutes, seconds):
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def temporizador():
    sg.theme("DarkGrey16")

    # Inputs
    layout_frame_horas = [
        [sg.Text("HORAS:", size=(10, 1)), sg.Input(
            size=(10, 1), key='-HORAS-')]
    ]

    layout_frame_minutos = [
        [sg.Text("MINUTOS:", size=(10, 1)), sg.Input(
            size=(10, 1), key='-MINUTOS-')]
    ]

    layout_frame_segundos = [
        [sg.Text("SEGUNDOS:", size=(10, 1)), sg.Input(
            size=(10, 1), key='-SEGUNDOS-')]
    ]

    # Frames
    frame_segundos = sg.Frame(None, layout_frame_segundos)
    frame_horas = sg.Frame(None, layout_frame_horas)
    frame_minutos = sg.Frame(None, layout_frame_minutos)

    layout_frame_dh = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_HOURS-')],
    ]
    layout_frame_dm = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_MINUTES-')]
    ]
    layout_frame_ds = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_SECONDS-')]
    ]

    layout_frame_temporizador = [
        [sg.Column([
            [sg.Frame(None, layout_frame_dh, size=(50, 50)),
             sg.Text(":"),
             sg.Frame(None, layout_frame_dm, size=(50, 50)),
             sg.Text(":"),
             sg.Frame(None, layout_frame_ds, size=(50, 50))]], expand_x=True,
            element_justification="center", pad=(0, 20, 0, 0))]
    ]

    layout_temporizador = sg.Frame(
        None, layout_frame_temporizador, size=(350, 100))

    # Frame Global
    layout_frame_global = [
        [sg.Column([
            [frame_segundos],
            [frame_minutos],
            [frame_horas],],
            justification='l'), sg.VerticalSeparator(),

         sg.Column([
             [sg.Button("INICIAR", size=(8, 1), button_color="#4169E1")],
             [sg.Button("RESETAR", size=(8, 1), button_color="#4169E1")],
             [sg.Button("Voltar", size=(8, 1), button_color="#4169E1")],])],
        [sg.HorizontalSeparator()],
        [layout_temporizador]
    ]

    frame_global = sg.Frame(None, layout_frame_global, size=(400, 250))

    layout = [
        [frame_global]
    ]

    start_time = None
    paused_time = 0
    target_time = None

    window = sg.Window("Temporizador", layout, size=(340, 250))

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            exit()
        elif event == "INICIAR":
            if start_time is None:
                try:
                    hours = int(values['-HORAS-']) if values['-HORAS-'] else 0
                    minutes = int(values['-MINUTOS-']
                                  ) if values['-MINUTOS-'] else 0
                    seconds = int(values['-SEGUNDOS-']
                                  ) if values['-SEGUNDOS-'] else 0
                    if hours < 0 or minutes < 0 or seconds < 0:
                        raise ValueError
                    target_time = hours * 3600 + minutes * 60 + seconds
                    start_time = time.time()
                except ValueError:
                    sg.popup(
                        'Por favor, insira números válidos e maiores ou iguais a zero para as horas, minutos e segundos.', button_color="#4169E1")
        elif event == "RESETAR":
            start_time = None
            paused_time = 0
            target_time = None
            window['-DISPLAY_HOURS-'].update('00')
            window['-DISPLAY_MINUTES-'].update('00')
            window['-DISPLAY_SECONDS-'].update('00')
            window['-HORAS-'].update('')
            window['-MINUTOS-'].update('')
            window['-SEGUNDOS-'].update('')
        elif start_time is not None:
            elapsed_time = time.time() - start_time - paused_time
            remaining_time = max(target_time - elapsed_time, 0)
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            window['-DISPLAY_HOURS-'].update(f'{int(hours):02}')
            window['-DISPLAY_MINUTES-'].update(f'{int(minutes):02}')
            window['-DISPLAY_SECONDS-'].update(f'{int(seconds):02}')
            if remaining_time == 0:
                sg.popup('Tempo Esgotado!', button_color=("#4169E1"))
                window['-DISPLAY_HOURS-'].update('00')
                window['-DISPLAY_MINUTES-'].update('00')
                window['-DISPLAY_SECONDS-'].update('00')
                window['-HORAS-'].update('')
                window['-MINUTOS-'].update('')
                window['-SEGUNDOS-'].update('')
                start_time = None
        elif event == "Voltar":
            window.close()
            relógio()


def alarm_function(alarm_time, alarm_name, alarm_message, days_of_week=None):
    while True:
        current_time = datetime.now()
        if days_of_week:
            # Verifica se o dia da semana atual está nos dias selecionados
            if current_time.weekday() in days_of_week:
                if current_time.time() >= alarm_time.time():
                    sg.popup(f'Alarme: {alarm_name}',
                             alarm_message, button_color="#4169E1")
                    break
        else:
            if current_time >= alarm_time:
                sg.popup(f'Alarme: {alarm_name}',
                         alarm_message, button_color="#4169E1")
                break
        time.sleep(1)

# Função para calcular o tempo restante


def calculate_time_left(alarm_time):
    current_time = datetime.now()
    time_left = alarm_time - current_time
    if time_left.total_seconds() < 0:
        return (0, 0, 0)
    hours, remainder = divmod(time_left.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)

# Função principal


def alarmes():
    sg.theme("DarkGrey16")

    layout_frame_button = [
        [sg.Button("Adicionar", size=(7, 2), button_color="#4169E1"),
         sg.Button("Deletar", size=(7, 2), button_color="#4169E1"),
         sg.Button("Voltar", size=(7, 2), button_color="#4169E1")]
    ]

    frame_button = sg.Frame(None, layout_frame_button, size=(230, 50))
    layout_frame_dh = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_HOURS-')],
    ]
    layout_frame_dm = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_MINUTES-')]
    ]
    layout_frame_ds = [
        [sg.Text("00", font=("Arial", 20), key='-DISPLAY_SECONDS-')]
    ]

    layout_frame_temporizador = [
        [sg.Column([
            [sg.Frame(None, layout_frame_dh, size=(50, 50)),
             sg.Text(":"),
             sg.Frame(None, layout_frame_dm, size=(50, 50)),
             sg.Text(":"),
             sg.Frame(None, layout_frame_ds, size=(50, 50))]], expand_x=True, element_justification="center", pad=(0, 20, 0, 0))]
    ]

    frame_digito = sg.Frame(None, layout_frame_temporizador)

    layout_frame_hora = [
        [frame_digito]
    ]

    frame_hora = sg.Frame(None, layout_frame_hora, size=(230, 110))

    layout_esquerda = [
        [frame_button],
        [sg.HorizontalSeparator()],
        [sg.Text("Nome:", size=(10, 1), font=("Arial", 10)),
         sg.Input(key="-NOME-", size=(19, 1))],
        [sg.Checkbox("D", pad=(0, 0), font=("Arial", 8), key="-MON-"),
         sg.Checkbox("S", pad=(0, 0), font=("Arial", 8), key="-TUE-"),
         sg.Checkbox("T", pad=(0, 0), font=("Arial", 8), key="-WED-"),
         sg.Checkbox("Q", pad=(0, 0), font=("Arial", 8), key="-THU-"),
         sg.Checkbox("Q", pad=(0, 0), font=("Arial", 8), key="-FRI-"),
         sg.Checkbox("S", pad=(0, 0), font=("Arial", 8), key="-SAT-"),
         sg.Checkbox("S", pad=(0, 0), font=("Arial", 8), key="-SUN-")],
        [sg.Text("Data:", size=(10, 1), font=("Arial", 10)), sg.Multiline(key="-DATA-", size=(12, 1), disabled=True, no_scrollbar=True),
         sg.CalendarButton('Data', button_color="#4169E1", key='-BOTAODATA-', target='-DATA-', format='%Y-%m-%d')],
        [sg.Text('Horas:', size=(10, 1), font=("Arial", 10)), sg.Combo(
            [f'{i:02d}' for i in range(24)], readonly=True, key='-HOUR-', size=(17, 1))],
        [sg.Text('Minutos:', size=(10, 1), font=("Arial", 10)), sg.Combo(
            [f'{i:02d}' for i in range(60)], readonly=True, key='-MINUTE-', size=(17, 1))],
        [sg.Text('Segundos:', size=(10, 1), font=("Arial", 10)), sg.Combo(
            [f'{i:02d}' for i in range(60)], readonly=True, key='-SECOND-', size=(17, 1))],
        [sg.Text("Nota:", size=(10, 1), font=("Arial", 10)),
         sg.Input(key="-NOTA-", size=(19, 1))],
        [sg.HorizontalSeparator()],
        [frame_hora]
    ]

    layout_frame_alarmes = [
        [sg.Text('Alarmes:', font=("Arial", 10), text_color="#4169E1")],
        [sg.Listbox(values=[], sbar_arrow_color="#4169E1", key='-ALARMS-', size=(30, 400),
                    enable_events=True, horizontal_scroll=True)]
    ]

    frame_alarmes = sg.Frame(None, layout_frame_alarmes)

    layout_direita = [
        [frame_alarmes]
    ]

    layout_global = [
        [sg.Frame(None, [[sg.Column(layout_esquerda), sg.VerticalSeparator(
        ), sg.Column(layout_direita)]], size=(510, 380))]
    ]

    window = sg.Window("Alarmes", layout_global, size=(510, 400))

    alarm_set = False
    alarm_time = None

    while True:
        event, values = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED:
            exit()

        if event == "Adicionar":
            date_str = values['-DATA-']
            hour = values['-HOUR-']
            minute = values['-MINUTE-']
            second = values['-SECOND-']
            name = values['-NOME-']
            message = values['-NOTA-']
            days_of_week = [i for i, key in enumerate(
                ["-MON-", "-TUE-", "-WED-", "-THU-", "-FRI-", "-SAT-", "-SUN-"]) if values[key]]

            if not hour or not minute or not second or not name or not message:
                sg.popup('Por favor, preencha todos os campos!',
                         button_color="#4169E1")
                continue

            elif not days_of_week and not date_str:
                sg.popup(
                    'Por favor, selecione uma data ou dias da semana!', button_color="#4169E1")
                continue

            elif not days_of_week:
                alarm_time_str = f"{date_str} {hour}:{minute}:{second}"
                alarm_time = datetime.strptime(
                    alarm_time_str, '%Y-%m-%d %H:%M:%S')
                if alarm_time <= datetime.now():
                    sg.popup('O horário do alarme deve estar no futuro!',
                             button_color="#4169E1")
                    continue
            else:
                alarm_time = datetime.now().replace(hour=int(hour), minute=int(minute),
                                                    second=int(second), microsecond=0)
                if alarm_time <= datetime.now():
                    alarm_time += datetime.timedelta(days=1)

            threading.Thread(target=alarm_function, args=(
                alarm_time, name, message, days_of_week), daemon=True).start()
            alarm_set = True
            sg.popup('Alarme configurado com sucesso!', button_color="#4169E1")
            window["-DATA-"].update('')
            window['-DATA-'].update('')
            window['-HOUR-'].update('')
            window['-MINUTE-'].update('')
            window['-SECOND-'].update('')
            window['-NOME-'].update('')
            window['-NOTA-'].update('')
            # Atualiza a lista de alarmes no frame direito
            alarm_str = f"{name} - {alarm_time.strftime('%Y-%m-%d %H:%M:%S')}"
            window['-ALARMS-'].update(
                values=window['-ALARMS-'].GetListValues() + [alarm_str])

        elif event == "Deletar":
            selected_alarm_indices = values['-ALARMS-']
            if selected_alarm_indices:
                # Assume apenas um alarme selecionado por vez
                selected_alarm_index = selected_alarm_indices[0]
                alarms_list = window['-ALARMS-'].get_list_values()
                # Obter o nome do alarme da string selecionada
                alarm_str = selected_alarm_index.split(" - ")[0]
                # Obter o índice do alarme na lista
                alarm_index = alarms_list.index(selected_alarm_index)
                del alarms_list[alarm_index]  # Remover o alarme da lista
                window['-ALARMS-'].update(values=alarms_list)
                sg.popup('Alarme removido com sucesso!',
                         button_color="#4169E1")
            else:
                sg.popup('Selecione um alarme para deletar.',
                         button_color="#4169E1")

        elif event == "Voltar":
            window.close()
            relógio()

        # Atualizar o display do tempo restante
        if alarm_set and alarm_time:
            hours, minutes, seconds = calculate_time_left(alarm_time)
            window['-DISPLAY_HOURS-'].update(f'{hours:02d}')
            window['-DISPLAY_MINUTES-'].update(f'{minutes:02d}')
            window['-DISPLAY_SECONDS-'].update(f'{seconds:02d}')

        # Desabilitar/habilitar campo de data baseado nas checkboxes
        if any(values[key] for key in ["-MON-", "-TUE-", "-WED-", "-THU-", "-FRI-", "-SAT-", "-SUN-"]):
            window['-BOTAODATA-'].update(disabled=True)
            window['-DATA-'].update("")
        else:
            window['-BOTAODATA-'].update(disabled=False)
#   Inserindo uma função para a janela anotações


def anotações():
    # Temas
    sg.theme("DarkGrey16")

    def editar_nota(note_name, nota=""):
        layout = [
            [sg.Text(f"Anotações para {note_name}")],
            [sg.Multiline(default_text=nota, sbar_arrow_color="#4169E1", size=(
                40, 10), key='-ANOTAÇÃO-')],
            [sg.Button('Salvar', button_color="#4169E1"), sg.Button(
                'Deletar', button_color="#4169E1"), sg.Button('Voltar', button_color="#4169E1")]
        ]
        return sg.Window(note_name, layout, modal=True)

    # Layout Interface

    layout_frame_buttons = [
        [sg.Button("Adicionar", button_color="#4169E1",
                   size=(10, 2), pad=(30, 2), bind_return_key=True),
         sg.Button("Voltar", button_color="#4169E1",
                   size=(10, 2), pad=(30, 2))]
    ]
    frame_buttons = sg.Frame(None, layout_frame_buttons, size=(400, 150))

    layout_frame_info = [
        [sg.Text("Nome do Arquivo: ", font=("Arial", 10)),
         sg.Input(key='-NOMENOTA-')]
    ]
    frame_info = sg.Frame("Nova Nota", layout_frame_info, size=(400, 50))

    notas_salvas = bc.mostrar_notas(id)

    layout_frame_salvos = [
        [sg.Column([], key='-BUTTON_LIST-'),
         sg.Listbox(values=notas_salvas, size=(400, 190), sbar_arrow_color="#4169E1",
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key="-LISTA-")],
    ]
    frame_salvos = sg.Frame(
        "Notas Salvas", layout_frame_salvos, size=(400, 190))

    layout_frame = [
        [frame_info],
        [frame_salvos],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [frame_buttons],
    ]
    layout = [
        [sg.Frame(None, layout_frame, size=(400, 450))]

    ]

    # Info Janela
    window = sg.Window("Anotações", layout, size=(
        350, 340), element_justification=("left"), )

    window.finalize()

    window['-LISTA-'].Widget.bind('<Double-1>',
                                  lambda event: window.write_event_value('-LISTBOX-DOUBLE_CLICK', ''))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            exit()
        elif event == "Adicionar":
            nome_nota = values['-NOMENOTA-']
            if nome_nota not in notas_salvas:
                if nome_nota != '':
                    note_window = editar_nota(nome_nota)
                    while True:
                        note_event, note_values = note_window.read()
                        nota = note_values["-ANOTAÇÃO-"]
                        if note_event in (sg.WINDOW_CLOSED, 'Voltar'):
                            note_window.close()
                            break
                        elif note_event == 'Salvar':
                            sg.popup_timed("Nota criada com sucesso!")
                            bc.criar_notas(nome_nota, nota, id)
                            note_window.close()
                            window["-NOMENOTA-"].update("")
                            window["-LISTA-"].update(bc.mostrar_notas(id))
                            break
                        elif note_event == "Voltar":
                            note_window.close()
                            break
                        elif note_event == sg.WINDOW_CLOSED:
                            quit()
                else:
                    sg.popup_timed(
                        "você deve colocar um título para a nota", auto_close=5)
            else:
                sg.popup_timed(
                    "você não pode criar uma nota com um título já utilizado", auto_close=5)
        elif event == '-LISTBOX-DOUBLE_CLICK':
            titulo = values['-LISTA-']
            nota = bc.ler_nota(titulo[0][0], id)
            note_window = editar_nota(titulo[0][0], nota)
            note_event, note_values = note_window.read()
            while True:
                nota = note_values["-ANOTAÇÃO-"]
                if note_event in (sg.WINDOW_CLOSED, 'Voltar'):
                    note_window.close()
                    window["-NOMENOTA-"].update("")
                    break
                elif note_event == 'Salvar':
                    sg.popup_timed(
                        "Nota atualizada com sucesso!", auto_close=5)
                    bc.modificar_nota(nota, titulo[0][0], id)
                    note_window.close()
                    break
                elif note_event == 'Deletar':
                    sg.popup_timed("Nota deletada.", auto_close_duration=5)
                    bc.deletar_nota(titulo[0][0], id)
                    note_window.close()
                    window["-NOMENOTA-"].update("")
                    window["-LISTA-"].update(bc.mostrar_notas(id))
                    break
                elif note_event == 'Voltar':
                    note_window.close()
                    break
        elif event == "Voltar":
            window.close()
            front2()


#   Inserindo janela de edição de perfil
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
        [sg.Button("Alterar senha", size=(10, 1), button_color="#4169E1",
                   pad=(10, 1))],
        [sg.HorizontalSeparator()],
        [sg.Button("Salvar alterações", size=(15, 2), button_color="#4169E1",
                   pad=(30, 1)),
         sg.Button("Visualizar Perfil", size=(15, 2), button_color="#4169E1",
                   pad=(30, 1))]
    ]

    # Frame que contém as informações do usuário
    frame = sg.Frame("Informações do Usuário", frame_layout, size=(400, 320))

    # Layout principal da janela
    layout = [
        [frame],
    ]
    window = sg.Window("Editar Perfil", layout, size=(400, 236))
    button, values = window.read()
    window.close()

    if button == sg.WINDOW_CLOSED:
        exit()
    elif button == "Visualizar Perfil":
        window.close()
        perfil()
    elif button == "Alterar senha":
        lg.senha_nova_logado(id)
    elif button == "Salvar alterações":
        usuario = values["-USUARIO-"]
        validez = bc.verificar_registro(usuario)
        nome = values["-NOME-"]
        email = values["-EMAIL-"]
        telefone = values["-TELEFONE-"]
        try:
            conexao = sq.connect("programa/registro.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM infoad WHERE id_perfil = ?", (id,))
            resultado = cursor.fetchone()
            if resultado is None:
                cursor.execute("INSERT INTO infoad (nome, email, telefone, id_perfil) VALUES (?, ?, ?, ?)",
                               (nome, email, telefone, id))
            if usuario != "" and validez == "valido":
                cursor.execute(
                    "UPDATE usuarios SET nome = ? WHERE id = ?", (usuario, id))
            elif validez == "invalido":
                sg.popup_timed("Usuário ja está sendo usado, tente outro",
                               auto_close=5, button_color="#4169E1")
            if nome != "":
                cursor.execute(
                    "UPDATE infoad SET nome = ? WHERE id_perfil = ?", (nome, id))
            if email != "":
                cursor.execute(
                    "UPDATE infoad SET email = ? WHERE id_perfil = ?", (email, id))
            if telefone != "":
                cursor.execute(
                    "UPDATE infoad SET telefone = ? WHERE id_perfil = ?", (telefone, id))
            conexao.commit()
        finally:
            conexao.close()

        window.close()
        perfil()


#   Inserindo janela de perfil
def perfil():
    sg.theme("DarkGrey16")
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome, email, telefone FROM infoad WHERE id_perfil = ?", (id,))
    resultado = cursor.fetchone()
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (id,))
    resultado1 = cursor.fetchone()
    if resultado is None:
        resultado = ("", "", "")
    conexao.close()

    frame_layout = [
        [sg.Text("Usuário: ", size=(10, 1)), sg.Multiline(
            font=("None 15"), size=(30, 1), disabled=True, no_scrollbar=True, default_text=resultado1[0])],
        [sg.Text("Nome: ", size=(10, 1)), sg.Multiline(
            font=("None 15"), size=(30, 1), disabled=True, no_scrollbar=True, default_text=resultado[0])],
        [sg.Text("Email: ", size=(10, 1)), sg.Multiline(
            font=("None 15"), size=(30, 1), disabled=True, no_scrollbar=True, default_text=resultado[1])],
        [sg.Text("Telefone: ", size=(10, 1)), sg.Multiline(
            font=("None 15"), size=(30, 1), disabled=True, no_scrollbar=True, default_text=resultado[2])],
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
    window = sg.Window("Perfil", layout, size=(400, 216))
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

#   Inserindo função de verificação de autenticidade


def verificação():
    sg.theme("Darkgrey16")
    frame_layout = [
        [sg.Text("Usuário:", size=(7, 1)), sg.Input(key="-USUARIO-")],
        [sg.HorizontalSeparator()],
        [sg.Text("Senha:", size=(7, 1)), sg.Input(key="-SENHA-", password_char="*", size=(22, 2)), sg.Button("👁", key="-SHOW_PASSWORD-",
                                                                                                             border_width=0, button_color=("#343434"))],
    ]

    layout = [
        [sg.Frame(None, frame_layout)],
        [sg.Button("Ok", button_color="#4169E1"), sg.Button(
            "Cancel", button_color="#4169E1")],
    ]

    window = sg.Window("Verificação", layout, size=(300, 115))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            exit()
        elif event == "-SHOW_PASSWORD-":
            password_input = window['-SENHA-']
            if password_input.Widget.cget("show") == "*":
                password_input.Widget.config(show="")
            else:
                password_input.Widget.config(show="*")
        elif event == "Ok":
            window.close()
            sg.popup("Informações modificadas com sucesso")
            perfil()
        elif event == "Cancel":
            sg.popup("Tentativa de edição mal sucedida")
            window.close()
            front2()

#   Página de inicialização do App


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
                   pad=(13, 1)),
         sg.Button("Relógio", size=(10, 2),
                   button_color=("#4169E1"), pad=(13, 1)),
         sg.Button("Anotações", size=(10, 2),
                   button_color=("#4169E1"), pad=(13, 1)),
         sg.Button("Perfil", size=(10, 2), button_color=("#4169E1"),
                   pad=(13, 1))],
    ]

    layout_frame_proximos_eventos = [
        [sg.Table(
            values=bc.eventos_recentes(id),
            headings=("DATA / HORA", "PROXIMOS EVENTOS"),
            key="-TABLE-", sbar_arrow_color="#4169E1", enable_events=True, size=(500, 10),
            auto_size_columns=False, col_widths=[14, 39],
            vertical_scroll_only=False, justification="l",
            font=("Arial", 15))]
    ]
    ultima_nota = bc.ultima_nota(id)
    layout_frame_anotações = [
        [sg.Multiline(default_text=ultima_nota[1],
                      sbar_arrow_color="#4169E1", size=(500, 210), disabled=True)]
    ]

    frame_anotações = sg.Frame(
        f"Última Anotação - {ultima_nota[0]}", layout_frame_anotações, size=(500, 210))

    # Frame interno que contém os botões
    frame_interno = sg.Frame(None, buttons_layout, size=(500, 45))

    frame_proximos_eventos = sg.Frame(
        "Próximos Eventos", layout_frame_proximos_eventos, size=(500, 150))
    # Layout do frame externo que contém o frame interno
    layout_do_frame_externo = [
        [frame_interno],
        [sg.HorizontalSeparator()],
        [frame_proximos_eventos],
        [frame_anotações],
        [sg.VPush()],
        [sg.Column([
            [sg.HorizontalSeparator()],
            [sg.Button("Frase do dia", size=(10, 2), button_color="#006400", pad=(8, 5)),
             sg.Multiline("", size=(50, 2), disabled=True, no_scrollbar=True, auto_size_text=True, key='-FRASE-')]
        ], expand_x=True, pad=(0, 0, 0, 0))]]
    # Frame externo
    frame_externo = sg.Frame(None, layout_do_frame_externo, size=(500, 600))

    # Layout Principal
    layout = [
        [frame_externo],
    ]

    # Janela
    window = sg.Window("Agenda", layout, size=(
        500, 520), element_justification="left", finalize=True)

    update(window)

    while True:
        button, values = window.read()
        # Condições
        if button == "Eventos":
            window.close()
            return "Eventos"
        elif button == "Relógio":
            window.close()
            return "Relógio"
        elif button == "Anotações":
            window.close()
            return "Anotações"
        elif button == "Perfil":
            window.close()
            return "Perfil"
        elif button == "Frase do dia":
            return "Frase do dia"
        elif button == sg.WINDOW_CLOSED:
            exit()
