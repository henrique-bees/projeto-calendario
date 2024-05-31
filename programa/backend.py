import sqlite3 as sq


def criar(tipo, data, nota, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"INSERT INTO {tipo} (data, titulo, id_eventos) VALUES (?, ?, ?)"
    cursor.execute(query, (data, nota, id))
    conexao.commit()
    conexao.close()


def deletar(tipo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"DELETE FROM {tipo} WHERE id = ?"
    cursor.execute(query, (id))
    conexao.commit()
    conexao.close()


def verificar_senha(senha):
    from string import punctuation
    if 8 <= len(senha) <= 16:
        if any(s.isnumeric() for s in senha) and \
                any(s.isalpha() for s in senha) and \
                any(s.isupper() for s in senha) and \
                any(s.islower() for s in senha) and \
                any(s in punctuation for s in senha):
            return True
    else:
        return False


def verificar_registro(usuario):
    if usuario == "":
        return "vazio"
    else:
        conexao = sq.connect("programa/registro.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM usuarios WHERE nome = ?", (usuario,))
        busca = cursor.fetchone()
        conexao.close()
        if busca is not None:
            return "invalido"
        else:
            return "valido"
