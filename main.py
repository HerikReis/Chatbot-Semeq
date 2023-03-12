import random
import sqlite3
import nltk
import spacy
import re
import string
from os import system
from database import Banco_dados
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer # pip install scikit-learn
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nlp = spacy.load("pt_core_news_sm")
system('cls')

# Função para pré-processar o input do usuário
def preprocess_input(text):
    # palavras que o modelo irá ignorar
    stop_words = spacy.lang.pt.stop_words.STOP_WORDS
    # pontuações que o modelo irá ignorar
    stop_punct = string.punctuation
    # tirar radical (lematização)
    documento = nlp(text)
    text = []
    for token in documento:
        text.append(token.lemma_)
    text = [palavra for palavra in text if palavra not in stop_words and palavra not in stop_punct]
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
    indice_sentenca = similaridade.argsort()[0][-2]
    vetor_similar = similaridade.flatten()
    vetor_similar.sort()
    vetor_encontrado = vetor_similar[-2]
    return vetor_encontrado,indice_sentenca

# Função para obter uma resposta do chatbot
def get_response(user_input):
    # Pré-processar o input do usuário
    user_input = preprocess_input(user_input)
    resposta_chatbot = ''
    lista_db = []
    db = Banco_dados.ler_db()
    for i in db:
        lista_db.append(preprocess_input(i))
    vetor_encontrado,indice_sentenca = tf_idf(user_input,lista_db)
    if (vetor_encontrado == 0):
        vetor_encontrado,indice_sentenca = tf_idf(user_input,db)
        if (vetor_encontrado == 0):
            resposta_chatbot = 'Desculpe, mas não entendi!'
        else:
            resposta_chatbot = db[indice_sentenca]
        return resposta_chatbot
    else:
        resposta_chatbot = db[indice_sentenca]
        return resposta_chatbot


def chatbot():
    textos_saida = ('sair','tchau','exit','esc')
    while True:
        user_input = input('Usuário: ')
        if user_input not in textos_saida:
            print('Chatbot:',get_response(user_input))
        else:
            print('Chatbot: Até breve!')
            break 

if __name__ == "__main__":
    chatbot()