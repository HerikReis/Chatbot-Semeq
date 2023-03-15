import json
import os

class Log:

    def __init__(self,intent,input_user,response,list_responses,id_response):
        self.intent = intent
        self.input_user = input_user
        self.response = response
        self.list_responses = list_responses
        self.id_response = id_response
        logs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        self.log_path = os.path.join(logs_path, "log_chat.json")
        self.log_chat()


    def log_chat(self):
        if self.intent == "bye":
            # apaga o log
            if os.path.exists(self.log_path):
                with open(os.path.join(self.log_path),'w',encoding="UTF-8") as chat_log:
                    log = json.dump([],chat_log)
            else:
                pass
        else:
            # verifica se o log existe
            if os.path.exists(self.log_path):
                # verifica se o arquivo está vazio
                if os.path.isfile(self.log_path):
                    with open(os.path.join(self.log_path),'r+',encoding="UTF-8") as chat_log:
                        log = json.load(chat_log)
                        log.append({"pattern": self.input_user, "response": self.response, "id": self.id_response, "list_response":self.list_responses})
                        log.seek(0)
                        json.dump(log, chat_log)
                else:
                    # cria o log
                    with open(os.path.join(self.log_path),'w',encoding="UTF-8") as chat_log:
                        log = ({"pattern": self.input_user, "response": self.response, "id": self.id_response, "list_response":self.list_responses})
                        json.dump(log, chat_log)
            else:
                with open(os.path.join(self.log_path), "w", encoding="UTF-8") as chat_log:
                    log = {
                        "pattern": self.input_user,
                        "response": self.response,
                        "id": self.id_response,
                        "list_response": self.list_responses
                    }
                    json.dump(log, chat_log)