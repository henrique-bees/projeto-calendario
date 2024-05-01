from time import sleep
while True:
    print("----------Projeto Calendário!!----------")
    sleep(1)
    print("""
    |   [d][s][t][q][qu][s][sa]         |
    |   [31][1][2][3][4][5][6]          |
    |   [7][8][9][10][11[12][13]        |
    |   [14][15][16][7][18][19][20]     |
    |   [21][22][23][24][25][26][27]    |
    |   [28][29][30]                    |
        """)
    sleep(1)
    opções = input("""

    [VERDE] = Alarme
    [AZUL] = Agendamentos
    [ROXO] = Lembretes
    [VERMELHO] = Notas
    [AMARELO] = Tarefas
    [ROSA] = Outros

    Qual a sua opção de marcação:         
    """).strip().upper()

    if opções == "VERDE":
        print("Você escolheu a opção de alarme.")
        dia = input("Insira o dia desejado: ")
        mes = input("Insira o mês desejado: ")
        ano = input("Insira o ano desejado: ")
        verificação = input(f"A data é {dia}/{mes}/{ano}, correto? [S/N]").strip().upper()
        if verificação == ["S", "SIM"]:
            print("Pronto podemos seguir!")
        else:
            ("Aqui precisa coloca para retornar uma função do dia, mes e ano")
    elif opções	== "AZUL":
        print("ok2")
    elif opções	== "ROXO":
        print("ok3")
    elif opções	== "VERMELHO":
        print("ok4")
    elif opções	== "AMARELO":
        print("ok5")
    elif opções	== "ROSA":
        print("ok6")
    else:
        print("Opção Inválida!")
        break