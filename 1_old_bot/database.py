import sqlite3
import json

class Banco_dados:
    def criar_db():
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # cria uma tabela chamada 'mensagens' com duas colunas: 'mensagem' e 'resposta'
        cursor = conexao.cursor()
        #cursor.execute('CREATE TABLE problemas (assunto, app_device, interface, modelo, problema, solucao)')
        cursor.execute('CREATE TABLE context_introducao (msg_introducao,banco_introducao,msg_problema,banco_problema)')
        cursor.execute('CREATE TABLE context_despedida (msg_despedida,banco_despedida)')
        cursor.execute('CREATE TABLE erro (msg_entendeu,msg_encaminhamento)')
        cursor.execute('CREATE TABLE context_problema (assunto,pergunta_assunto,interface,pergunta_interface,problema,pergunta_problema)')
        cursor.execute('CREATE TABLE context_feedback (pergunta_feedback,banco_feedback_positivo,banco_feedback_negativo)')
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def inserir_db():
        novos_valores = [
            "sim",
            "s",
            "ss",
            "yes",
            "si",
            "sí",
            "isso",
            "foi",
            "bom"
        ]
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # insere algumas mensagens e respostas na tabela
        cursor = conexao.cursor()
        for valor in novos_valores:
            cursor.execute("INSERT INTO context_feedback (banco_feedback_positivo) VALUES (?)", (valor,))
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def ler_db(column,table):
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # Executa a instrução SQL SELECT para obter os dados da coluna desejada
        cursor = conexao.cursor()
        cursor.execute(f"SELECT {column} FROM {table}")
        # Iterar sobre os resultados e imprimir na tela
        dados =[]
        for resultado in cursor.fetchall():
            dados.append(resultado[0])
        # fecha a conexão com o banco de dados
        conexao.close()
        return dados

    def percorrer_dicionarios(dicionario, caminho, cursor):
        for chave, valor in dicionario.items():
            novo_caminho = caminho + [chave]
            if isinstance(valor, dict):
                Banco_dados.percorrer_dicionarios(valor, novo_caminho, cursor)
            else:
                solucao = valor
                assunto = novo_caminho[0] if novo_caminho else ""
                app_device = novo_caminho[1] if len(novo_caminho) > 1 else ""
                interface = novo_caminho[2] if len(novo_caminho) > 2 else ""
                modelo = novo_caminho[3] if len(novo_caminho) > 3 else ""
                problema = novo_caminho[4] if len(novo_caminho) > 4 else ""
                cursor.execute("INSERT INTO problemas (assunto, app_device, interface, modelo, problema, solucao) VALUES (?, ?, ?, ?, ?, ?)",(assunto, app_device, interface, modelo, problema, solucao))

    def inserir_json():
        # Carrega o arquivo JSON
        with open('bd_suporte.json', 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
        # Conecta ao banco de dados SQLite
        conexao = sqlite3.connect('database.db')
        # Cria uma tabela no banco de dados
        cursor = conexao.cursor()
        # Insere os dados do JSON na tabela
        Banco_dados.percorrer_dicionarios(dados_json, [], cursor)
        # Salva as mudanças e fecha a conexão com o banco de dados
        conexao.commit()
        conexao.close()

# Banco_dados.criar_db()
# Banco_dados.inserir_json()
# Banco_dados.inserir_db()

# conexao = sqlite3.connect('database.db')
# cursor = conexao.cursor()
# cursor.execute("DELETE FROM context_feedback")
# conexao.commit()
# conexao.close()