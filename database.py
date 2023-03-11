import sqlite3

class Banco_dados:
    def criar_db():
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('suporteBD.db')
        # cria uma tabela chamada 'mensagens' com duas colunas: 'mensagem' e 'resposta'
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE mensagens (mensagem TEXT, resposta TEXT)')
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def inserir_db():
        novos_valores = ['oi','ola','eai','salve']
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('suporteBD.db')
        # insere algumas mensagens e respostas na tabela
        cursor = conexao.cursor()
        for valor in novos_valores:
            cursor.execute("INSERT INTO mensagens (resposta) VALUES (?)", (valor,))
        conexao.commit()
        # fecha a conexão com o banco de dados
        conexao.close()

    def ler_db():
        # estabelece uma conexão com o banco de dados
        conexao = sqlite3.connect('suporteBD.db')
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