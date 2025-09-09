from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import csv
import os

from database import create_table, insert_or_update_player, get_ranking, DATABASE_NAME

app = Flask(__name__)
CORS(app)  

CSV_FILE = 'jogadores.csv'
LOG_FILE = 'erros.log'

def process_csv_file_if_needed():
    """Processa o CSV e popula o banco de dados se a tabela estiver vazia."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jogadores")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        print("Banco de dados vazio. Processando o arquivo CSV...")
        with open(LOG_FILE, 'w') as log_file:
            if not os.path.exists(CSV_FILE):
                print(f"Erro: O arquivo '{CSV_FILE}' não foi encontrado.")
                return

            with open(CSV_FILE, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                try:
                    next(reader)  
                except StopIteration:
                    print("O arquivo CSV está vazio.")
                    return
                
                for i, row in enumerate(reader, 1):
                    if len(row) != 3:
                        log_file.write(f"Linha {i}: Linha inválida, número de colunas incorreto -> {row}\n")
                        continue
                    try:
                        nome, nivel, pontuacao = row
                        nivel = int(nivel)
                        pontuacao = float(pontuacao)
                        insert_or_update_player(nome, nivel, pontuacao)
                    except ValueError:
                        log_file.write(f"Linha {i}: Dados de nível ou pontuação inválidos -> {row}\n")
        print("Dados importados com sucesso.")
    else:
        print("Banco de dados já populado. Pulando a importação do CSV.")

@app.route('/api/ranking', methods=['GET'])
def get_ranking_api():
    ranking = get_ranking()
    ranking_list = []
    for pos, (nome, nivel, pontuacao) in enumerate(ranking, 1):
        ranking_list.append({
            'posicao': pos,
            'nome': nome,
            'nivel': nivel,
            'pontuacao': pontuacao
        })
    return jsonify(ranking_list)

if __name__ == '__main__':
    create_table()
    process_csv_file_if_needed()
    app.run(debug=True)