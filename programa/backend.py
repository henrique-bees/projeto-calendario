import sqlite3 as sq


def criar(tipo, data, titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"INSERT INTO {tipo} (data, titulo, id_pins) VALUES (?, ?, ?)"
    cursor.execute(query, (data, titulo, id))
    conexao.commit()
    conexao.close()


def deletar(tipo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"DELETE FROM {tipo} WHERE id = ?"
    cursor.execute(query, (id,))
    conexao.commit()
    conexao.close()


def ler_salvos(tipo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"SELECT * FROM {tipo} WHERE id_pins = ?"
    cursor.execute(query, (id,))
    conteudo = cursor.fetchall()
    conexao.close()
    return conteudo


def atualizar_index(tipo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    try:
        query = f"SELECT id FROM {tipo} WHERE id_pins = ?"
        cursor.execute(query, (id,))
        id_atualizado = cursor.fetchall()
        conexao.close()
        return id_atualizado[-1][0]
    finally:
        return 0


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
