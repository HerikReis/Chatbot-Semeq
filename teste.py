import sqlite3
import json

def percorrer_dicionarios(dicionario, caminho, cursor):
    for chave, valor in dicionario.items():
        novo_caminho = caminho + [chave]
        if isinstance(valor, dict):
            percorrer_dicionarios(valor, novo_caminho, cursor)
        else:
            solucao = valor
            assunto = novo_caminho[0] if novo_caminho else ""
            app_device = novo_caminho[1] if len(novo_caminho) > 1 else ""
            interface = novo_caminho[2] if len(novo_caminho) > 2 else ""
            modelo = novo_caminho[3] if len(novo_caminho) > 3 else ""
            problema = novo_caminho[4] if len(novo_caminho) > 4 else ""
            cursor.execute("INSERT INTO problemas (assunto, app_device, interface, modelo, problema, solucao) VALUES (?, ?, ?, ?, ?, ?)",(assunto, app_device, interface, modelo, problema, solucao))

# Carrega o arquivo JSON
with open('bd_suporte.json', 'r', encoding='utf-8') as f:
    dados_json = json.load(f)

# Conecta ao banco de dados SQLite
conexao = sqlite3.connect('suporteBD.db')

# Cria uma tabela no banco de dados
cursor = conexao.cursor()

# Insere os dados do JSON na tabela
percorrer_dicionarios(dados_json, [], cursor)

# Salva as mudanças e fecha a conexão com o banco de dados
conexao.commit()
conexao.close()