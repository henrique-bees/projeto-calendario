import sqlite3 as sq


def criar_eventos(data, titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT MAX(posição) FROM eventos WHERE id_pins = ?", (id,))
        resultado = cursor.fetchone()[0]
        if resultado is not None:
            index = resultado + 1
        else:
            index = 1
    finally:
        cursor.execute(
            "INSERT INTO eventos (posição, data, titulo, id_pins)"
            " VALUES (?, ?, ?, ?)", (index, data, titulo, id))
        conexao.commit()
        conexao.close()
        return index


def deletar_eventos(index, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "DELETE FROM eventos WHERE posição = ? and id_pins = ?", (index, id,))
    cursor.execute(
        "UPDATE eventos SET posição = posição - 1 WHERE id_pins = ? AND"
        " posição > ?", (id, index))
    conexao.commit()
    conexao.close()


def ler_eventos(id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT posição, data, titulo FROM eventos WHERE id_pins = ?", (id,))
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
            return "existe"
        else:
            return "não existe"


def eventos_recentes(id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT data, titulo FROM eventos WHERE id_pins = ? ORDER BY data",
        (id,))
    conteudo = cursor.fetchmany(3)
    conexao.close()
    return conteudo


def criar_notas(titulo, nota, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO notas (titulo, nota, id_notas) VALUES (?, ?, ?)",
        (titulo, nota, id))
    conexao.commit()
    conexao.close()


def mostrar_notas(id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT titulo FROM notas WHERE id_notas = ?", (id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def ler_nota(titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nota FROM notas WHERE titulo = ? and id_notas = ?",
        (titulo, id))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado[0]


def modificar_nota(nota, titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE notas SET nota = ? WHERE titulo = ? and id_notas = ?",
        (nota, titulo, id))
    conexao.commit()
    conexao.close()


def deletar_nota(titulo, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "DELETE FROM notas WHERE titulo = ? and id_notas = ?", (titulo, id))
    conexao.commit()
    conexao.close()


def ultima_nota(id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT titulo, nota FROM notas WHERE id_notas = ? ORDER BY id DESC",
        (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado
