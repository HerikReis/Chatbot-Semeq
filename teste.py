import nltk
import spacy

from database import Banco_dados
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tf_idf(user_input,list_text_db):
    list_text_db.append(user_input)
    list_text_db = list(filter(None, list_text_db))
    tfidf = TfidfVectorizer()
    palavras_vetorizadas = tfidf.fit_transform(list_text_db)
    similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)
    vetor_similar = similaridade.flatten()
    vetor_similar.sort()
    vetor_encontrado = vetor_similar[-2]
    indice_sentenca = similaridade.argsort()[0][-2]
    return vetor_encontrado,indice_sentenca

def analisar(input_user,context):
    lista_vetor = []
    for i in context:
        vetor_encontrado,indices_sentenca = tf_idf(input_user,i)
        lista_vetor.append(vetor_encontrado)
    return lista_vetor

def context(input_user):
    introducao = [
        introducao_user := Banco_dados.ler_db("banco_introducao","context_introducao"),
        introducao_problema := Banco_dados.ler_db("banco_problema","context_introducao")
    ]
    lista_vetor1 = analisar(input_user,introducao)

    despedida = [
        despedida_user := Banco_dados.ler_db("banco_despedida","context_despedida")
    ]
    lista_vetor2 = analisar(input_user,despedida)

    return max(lista_vetor1), max(lista_vetor2)

a = input(': ')
print(context(a))