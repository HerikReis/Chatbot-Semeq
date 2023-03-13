import nltk
import spacy
import re
import numpy as np
import os
import json
import random
from database import Banco_dados
from nltk.tokenize import word_tokenize
from nltk import download
from sklearn.feature_extraction.text import TfidfVectorizer # pip install scikit-learn
from sklearn.metrics.pairwise import cosine_similarity

download('punkt')
nlp = spacy.load("pt_core_news_sm") # python -m spacy download pt_core_news_sm => erro de linguagem
os.system('cls')

#############################################################################################
class Tratamento:
    # Função para pré-processar os textos para calculo de correlação
    def preprocess(text,lematizar=True):
        text = text.lower()
        if lematizar:
            # encontrar radical das palavras (lematização)
            documento = nlp(text)
            text = []
            for token in documento:
                text.append(token.lemma_)
            text = ' '.join([str(elemento) for elemento in text if not elemento.isdigit()])
        # tirar pontuações, acentos e espaços extras
        text = re.sub(r"[!#$%&'()*+,-./:;<=>?@[^_`{|}~]+", ' ', re.sub('[áàãâä]', 'a', re.sub('[éèêë]', 'e', re.sub('[íìîï]', 'i', re.sub('[óòõôö]', 'o', re.sub('[úùûü]', 'u', text))))))
        # tirar espaços em branco
        text = re.sub(r'\s+', ' ',text)
        return text.strip()
    
    def get_values_vetor(lista):
        # Filtra a lista para manter apenas os valores acima de zero
        lista_filtrada = [x for x in lista if x > 0]
        # Classifica a lista filtrada em ordem decrescente
        sorted_lista = sorted(lista_filtrada, reverse=True)
        # Seleciona no máximo três valores acima de zero
        lista = sorted_lista[:3]
        value_counts = {}
        for value in lista:
            if value not in value_counts:
                value_counts[value] = 1
            else:
                value_counts[value] += 1
        unique_values = sorted(set(lista), reverse=True)
        values_vetor = []
        for value in unique_values:
            count = value_counts[value]
            if len(values_vetor) < 3:
                values_vetor.extend([value] * min(count, 3 - len(values_vetor)))
            elif count > 1:
                indices = [i for i, x in enumerate(lista) if x == value]
                chosen_index = random.choice(indices)
                values_vetor[chosen_index % 3] = value
        return values_vetor

    # Função para calcular correlação
    def tf_idf(user_input,list_text_db):
        list_text_db.append(user_input)
        tfidf = TfidfVectorizer()
        list_text_db = list(filter(None, list_text_db))
        palavras_vetorizadas = tfidf.fit_transform(list_text_db)
        similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)
        vetor_similar = similaridade.flatten()
        vetor_similar.sort()
        vetor_similar = np.delete(vetor_similar, -1)
        vetor_encontrado = Tratamento.get_values_vetor(vetor_similar)
        count = -2
        indices_sentenca = []
        for i in vetor_encontrado:
            indices_sentenca.append(similaridade.argsort()[0][count])
            count -= 1
        return vetor_encontrado,indices_sentenca

#############################################################################################
def feedback(user_input):
    user_input = user_input.lower().split()
    feedback_negativo = ['não','nao','n','nn','nops','no']
    feedback_positivo = ['sim','ss','s','yes','si','foi']
    for i in user_input:
        if i in feedback_negativo:
            return -1, False
        elif i in feedback_positivo:
            return True, False
        else:
            return False, True
#############################################################################################
class Contexto:
    # analisa o contexto
    def context_parser(input_user,context):
        lista_vetor = []
        for i in context:
            vetor_encontrado,indices_sentenca = Tratamento.tf_idf(input_user,i)
            if len(vetor_encontrado) > 0:
                lista_vetor.append(max(vetor_encontrado))
            else:
                lista_vetor.append(0)
        return lista_vetor

    def context(input_user):
        introducao = [
            introducao_user := Banco_dados.ler_db("banco_introducao","context_introducao"),
            introducao_problema := Banco_dados.ler_db("banco_problema","context_introducao")
        ]
        vetor_contexto1 = Contexto.context_parser(input_user,introducao)

        despedida = [
            despedida_user := Banco_dados.ler_db("banco_despedida","context_despedida")
        ]
        vetor_contexto2 = Contexto.context_parser(input_user,despedida)

        feedback = [
            feedback_positivo := Banco_dados.ler_db("banco_feedback_positivo","context_feedback"),
            feedback_negativo := Banco_dados.ler_db("banco_feedback_negativo","context_feedback")
        ]
        vetor_contexto3 = Contexto.context_parser(input_user,feedback)
    
        problema = [
            assunto := Banco_dados.ler_db("assunto","context_problema"),
            interface := Banco_dados.ler_db("interface","context_problema"),
            problema := Banco_dados.ler_db("problema","context_problema")
        ]
        vetor_contexto4 = Contexto.context_parser(input_user,problema)
        # verifica qual vetor é maior. Ou seja, qual contexto tem mais relação
        list_vetor = [vetor_contexto1,vetor_contexto2,vetor_contexto3,vetor_contexto4]
        max_vetor = max(list_vetor)
        if list_vetor.index(max_vetor) == 0:
            return 'context_introducao'
        elif list_vetor.index(max_vetor) == 1:
            return 'context_despedida'
        elif list_vetor.index(max_vetor) == 2:
            return 'context_feedback'
        elif list_vetor.index(max_vetor) == 3:
            return 'context_problema'
        else:
            return 'erro'

#############################################################################################
# Função para obter uma resposta do chatbot
def get_response(input_user, indice=0):
    user_input = input_user
    # Pré-processar o input do usuário
    user_input = Tratamento.preprocess(user_input)
    count,passar = feedback(input_user)
    resposta_chatbot = []
    if passar:
        lista_db = []
        db = Banco_dados.ler_db('problema','problemas')
        for i in db:
            lista_db.append(Tratamento.preprocess(i))
        vetor_encontrado,indice_sentenca = Tratamento.tf_idf(user_input,lista_db)
        if (len(vetor_encontrado) == 0):
            vetor_encontrado,indice_sentenca = Tratamento.tf_idf(user_input,db)
            if (len(vetor_encontrado) == 0):
                resposta_chatbot.append('Desculpe, mas não entendi!')
                entendeu = False
            else:
                resposta_chatbot.append(db[indice_sentenca[indice]])
                entendeu = True
        else:
            resposta_chatbot.append(db[indice_sentenca[indice]])
            entendeu = True
    elif not passar and count == True:
        resposta_chatbot.append('Ótimo, se precisar de mais alguma coisa estarei aqui!')
        entendeu = False
    else:
        with open(os.path.join("\\Users\\herik\\OneDrive\\Área de Trabalho\\chatbot\\logs", 'log_chat.json'), 'r+') as f:
            log = json.load(f)
        if log[-1]['indice'] == indice:
            resposta_chatbot.append("Desculpe, não tenho mais soluções para isso!")
            entendeu = False
        else:
            indice = log[-1]['indice'] + count
            resposta_chatbot.append(db[indice_sentenca[indice]])
            entendeu = True
    log_chat(input_user,resposta_chatbot,indice)
    return resposta_chatbot,entendeu

def log_chat(pergunta,resposta,indice,diretorio="\\Users\\Semeq\\Desktop\\Chatbot-Semeq\\logs"):
    if os.path.exists(diretorio):
        if os.path.isfile(os.path.join(diretorio, 'log_chat.json')):
            with open(os.path.join(diretorio, 'log_chat.json'), 'r+') as f:
                log = json.load(f)
                num = len(log) + 1
                log.append({"pergunta": pergunta, "resposta": resposta, "indice": indice})
                f.seek(0)
                json.dump(log, f, indent=4)
        else:
            with open(os.path.join(diretorio, 'log_chat.json'), 'w') as f:
                log = [{"pergunta": pergunta, "resposta": resposta, "indice": indice}]
                json.dump(log, f, indent=4)
    else:
        print("O diretório especificado não existe.")

#############################################################################################
def chatbot_cmd():
    textos_saida = ('sair','tchau','exit','esc')
    while True:
        user_input = input('Usuário: ')
        if user_input not in textos_saida:
            resposta_chatbot,entendeu = get_response(user_input)
            for i in resposta_chatbot:
                print('Chatbot:',i)
            if entendeu:
                print('Chatbot: Esta resposta foi útil?')
        else:
            print('Chatbot: Até breve!')
            with open("\\Users\\Semeq\\Desktop\\Chatbot-Semeq\\logs\\log_chat.json", 'w') as f:
                json.dump([], f)
            break 

def chatbot_GUI(user_input):
    textos_saida = ('sair','tchau','exit','esc')
    if user_input not in textos_saida:
        resposta_chatbot,entendeu = get_response(user_input)
        for i in resposta_chatbot:
            return i
        if entendeu:
            return 'Esta resposta foi útil?'
    else:
        with open(os.path.join("\\Chatbot-Semeq\\logs\\log_chat.json"), 'w') as f:
            json.dump([], f)
        return 'Chatbot: Até breve!'

if __name__ == "__main__":
    chatbot_cmd()
    # a = input(': ')
    # print(Contexto.context(a))