import sqlite3 as sq


def criar(tipo, data, titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    try:
        query = f"SELECT MAX(posição) FROM {tipo} WHERE id_pins = ?"
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()[0]
        if resultado is not None:
            index = resultado + 1
        else:
            index = 1
    finally:
        query = f"INSERT INTO {tipo} (posição, data, titulo, id_pins) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (index, data, titulo, id))
        conexao.commit()
        conexao.close()
        return index


def deletar(tipo, index, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"DELETE FROM {tipo} WHERE posição = ? and id_pins = ?"
    cursor.execute(query, (index, id,))
    query = f"UPDATE {tipo} SET posição = posição - 1 WHERE id_pins = ? AND posição > ?"
    cursor.execute(query, (id, index))
    conexao.commit()
    conexao.close()
    print("a")


def ler_salvos(tipo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"SELECT posição, data, titulo FROM {tipo} WHERE id_pins = ?"
    cursor.execute(query, (id,))
    conteudo = cursor.fetchall()
    conexao.close()
    return conteudo


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
