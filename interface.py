import tkinter as tk
from tkinter import scrolledtext
import json
from chatbot import get_response

class ChatBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")

        self.chat_history = []
        self.json_data = {}

        self.label = tk.Label(master, text="Converse com o ChatBot!")
        self.label.pack(pady=10)

        self.chat_log = scrolledtext.ScrolledText(master, height=15, width=50)
        self.chat_log.pack(padx=10, pady=10)

        self.input_box = tk.Entry(master, width=50)
        self.input_box.pack(padx=10, pady=10)
        self.input_box.bind('<Return>', self.send_message)

        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.pack(pady=10)

    def send_message(self, event=None):
        user_input = self.input_box.get()
        # Adicionar entrada do usuário ao histórico de bate-papo
        self.chat_history.append(('usuário', user_input))
        self.json_data["input_user"] = user_input
        # Obter resposta do chatbot
        bot_response = get_response(user_input)
        # Adicionar resposta do chatbot ao histórico de bate-papo
        self.chat_history.append(('chatbot', bot_response))
        self.json_data["resposta"] = bot_response
        # Exibir histórico de bate-papo na caixa de chat
        self.chat_log.insert(tk.END, 'Você: ' + user_input + '\n')
        self.chat_log.insert(tk.END, 'ChatBot: ' + bot_response + '\n')
        # Limpar caixa de entrada de texto
        self.input_box.delete(0, tk.END)
        # Salvar histórico em um arquivo JSON
        with open('chat_history.json', 'w') as f:
            json.dump(self.json_data, f)

root = tk.Tk()
my_gui = ChatBotGUI(root)
root.mainloop()