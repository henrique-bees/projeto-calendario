import sqlite3 as sq
import uuid


def criar(tipo, data, nota, id):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    query = f"INSERT INTO {tipo} (data, titulo, id_eventos) VALUES (?, ?, ?)"
    cursor.execute(query, (data, nota, id))
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


def criar_sessao(nome, senha):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nome = ? AND senha = ?",
                   (nome, senha))
    usuario = cursor.fetchone()
    if usuario:
        id_usuario = usuario[0]
        token_sessao = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO sessions (user_id, session_token) VALUES (?, ?)",
            (id_usuario, token_sessao))
        conexao.commit()
        conexao.close()
        return token_sessao
    else:
        conexao.close()
        return None


def verificar_sessao(token_sessao):
    conexao = sq.connect("programa/registro.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE session_token = ?",
                   (token_sessao))
    session = cursor.fetchone()
    conexao.close()
    return session is not None
