import nltk
import spacy
import re
import numpy as np
import os
import json
from database import Banco_dados
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer # pip install scikit-learn
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nlp = spacy.load("pt_core_news_sm")
os.system('cls')

# Função para pré-processar o input do usuário
def preprocess_input(text,lematizar=True):
    if lematizar:
        # tirar radical (lematização)
        documento = nlp(text)
        text = []
        for token in documento:
            text.append(token.lemma_)
        text = ' '.join([str(elemento) for elemento in text if not elemento.isdigit()])
    # tirar pontuações 
    text = re.sub(r"[!#$%&'()*+,-./:;<=>?@[^_`{|}~]+", ' ', re.sub('[áàãâä]', 'a', re.sub('[éèêë]', 'e', re.sub('[íìîï]', 'i', re.sub('[óòõôö]', 'o', re.sub('[úùûü]', 'u', re.sub(r" +", ' ', text)))))))
    # tirar espaços em branco
    text = re.sub(r'\s+', ' ',text)
    # Tokenize o texto em palavras
    text = word_tokenize(text)
    # Converter todas as palavras para minúsculas
    text = [word.lower() for word in text]
    # Retornar as palavras como uma string única
    text = " ".join(text)
    return text

# Função para calcular correlação
def tf_idf(user_input,lista_db):
    lista_db.append(user_input)
    tfidf = TfidfVectorizer()
    palavras_vetorizadas = tfidf.fit_transform(lista_db)
    similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)
    vetor_similar = similaridade.flatten()
    vetor_similar.sort()
    vetor_encontrado = []
    for i in vetor_similar:
        if i > 0 and np.where(vetor_similar==i)[0][0] != (len(vetor_similar) - 1):
            vetor_encontrado.append(i)
    count = -2
    indices_sentenca = []
    for i in vetor_encontrado:
        indices_sentenca.append(similaridade.argsort()[0][count])
        count -= 1
    return vetor_encontrado,indices_sentenca

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

# Função para obter uma resposta do chatbot
def get_response(input_user, indice=0):
    user_input = input_user
    # Pré-processar o input do usuário
    user_input = preprocess_input(user_input)
    count,passar = feedback(input_user)
    resposta_chatbot = []
    if passar:
        lista_db = []
        db = Banco_dados.ler_db()
        for i in db:
            lista_db.append(preprocess_input(i))
        vetor_encontrado,indice_sentenca = tf_idf(user_input,lista_db)
        if (len(vetor_encontrado) == 0):
            vetor_encontrado,indice_sentenca = tf_idf(user_input,db)
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

def log_chat(pergunta,resposta,indice,diretorio="\\Users\\herik\\OneDrive\\Área de Trabalho\\chatbot\\logs"):
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


def chatbot():
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
            with open("\\Users\\herik\\OneDrive\\Área de Trabalho\\chatbot\\logs\\log_chat.json", 'w') as f:
                json.dump([], f)
            break 

if __name__ == "__main__":
    chatbot()