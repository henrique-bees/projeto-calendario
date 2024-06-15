from frontend import *
from backend import *
from login import registro, login, nova_senha_deslogado
from icone import icon
from PySimpleGUI import set_global_icon


def main():
    loading()
    while True:
        reg = registro()
        if reg == "login":
            global log
            log = login()
            while True:
                if log == "Voltar":
                    pass
                elif log == "nova senha":
                    nova_senha_deslogado()


# ICON PARA O APP
icon = icon()
set_global_icon(icon)
main()
