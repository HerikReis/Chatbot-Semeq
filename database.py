import sqlite3
import json

class Banco_dados:
    def criar_db():
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # cria uma tabela chamada 'mensagens' com duas colunas: 'mensagem' e 'resposta'
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE problemas (assunto, app_device, interface, modelo, problema, solucao)')
        cursor.execute('CREATE TABLE menssagens ()')
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def inserir_db():
        novos_valores = ['oi','ola','eai','salve']
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # insere algumas mensagens e respostas na tabela
        cursor = conexao.cursor()
        for valor in novos_valores:
            cursor.execute("INSERT INTO mensagens (resposta) VALUES (?)", (valor,))
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def ler_db():
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('database.db')
        # Executa a instrução SQL SELECT para obter os dados da coluna desejada
        cursor = conexao.cursor()
        cursor.execute("SELECT problema FROM problemas")
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