import sqlite3

DATABASE_NAME = 'ranking.db'

def connect_db():
    """Conecta-se ao banco de dados e retorna o objeto de conexão."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    """Cria a tabela 'jogadores' se ela não existir, com uma restrição de unicidade no nome."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            nivel INTEGER,
            pontuacao REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_or_update_player(nome, nivel, pontuacao):
    """Insere um novo jogador ou atualiza um jogador existente com o mesmo nome."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO jogadores (id, nome, nivel, pontuacao)
        VALUES (
            (SELECT id FROM jogadores WHERE nome = ?),
            ?, ?, ?
        )
    ''', (nome, nome, nivel, pontuacao))
    conn.commit()
    conn.close()

def get_ranking():
    """Retorna a lista de jogadores ordenada por pontuação, de forma decrescente."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nivel, pontuacao FROM jogadores ORDER BY pontuacao DESC")
    ranking = cursor.fetchall()
    conn.close()
    return ranking