from model.log import Log
from model.extract import class_prediction, get_response
from keras.models import load_model

def chatbot_run(input_user):
    id_response = 0
    # extrai o modelo usando o keras
    model = load_model('model.h5')
    # abre o banco de dados para carregar as intenções
    ...
    intents_db = ...
    # chama função de correlção para filtrar palavras inpróprias
    vetor = ...
    # verifica se houve correlação com o intent de palavras/frases inpróprias e define a intenção
    if vetor > 0.3:
        intent_user = "censored"
        list_response = get_response(intent_user, intents_db)
        response = [id_response]
    else:
        # carrega a intenção do log da última conversa
        intent_log = ...
        # verifica se a intenção era um feedback
        if ...:
            ...
        # verifica se a intenção era uma pergunta filtro para o usuário responder 
        elif ...:
            ...
        # se não for nenhuma das intenções de resposta acima, chama o modelo para interagir
        else:
            intent_user = class_prediction(input_user, model)
            list_response = get_response(intent_user, intents_db)
            response = [id_response]
    # cria um log da conversa
    Log(intent_user,input_user,list_response,response,id_response)
    return response