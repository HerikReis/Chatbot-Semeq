import sqlite3
import random

conn = sqlite3.connect('database.db')
c = conn.cursor()

def get_solution(problem_description):
    # Seleciona todas as linhas da tabela 'problems' que contenham a descrição do problema
    c.execute("SELECT * FROM problemas WHERE problema LIKE ?", ('%' + problem_description + '%',))
    rows = c.fetchall()
    print(len(rows))
    print()
    # Retorna a solução correspondente ao problema
    return rows[-1]



def ask_question(question, possible_answers):
    # Pergunta a questão e espera uma resposta
    answer = input(question + ' ')

    # Se a resposta não estiver na lista de possíveis respostas, pede ao usuário que tente novamente
    while answer not in possible_answers:
        answer = input('Desculpe, resposta inválida. ' + question + ' ')

    # Retorna a resposta do usuário
    return answer



def chatbot():
    print('Olá! Eu sou um chatbot de suporte e estou aqui para ajudar com seus problemas.')
    print('Por favor, descreva o seu problema abaixo.\n')

    # Faz a primeira pergunta ao usuário
    problem_description = ask_question('Qual é o problema que você está enfrentando?', ['Internet lenta', 'Sem conexão com a internet', 'Problemas com o email','COLETOR NÃO LIGA'])

    # Continua fazendo perguntas até encontrar uma solução
    while True:
        solution = get_solution(problem_description)

        # Se a solução for encontrada, mostra-a ao usuário e encerra a conversa
        if solution:
            print('Solução:', solution)
            break

        # Se não houver uma solução, pede ao usuário que forneça mais detalhes
        else:
            problem_description = ask_question('Por favor, forneça mais detalhes sobre o problema.', ['Internet lenta', 'Sem conexão com a internet', 'Problemas com o email'])

    print('Obrigado por usar o chatbot de suporte. Até a próxima!')

chatbot()