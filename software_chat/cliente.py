import socket
import threading
import tkinter as tk

# Dados do servidor
HOST = '172.16.31.43'  # IP do servidor
PORT = 5001  # Porta para conexão

# Variável global para armazenar o nome do cliente
client_name = ""

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            # Receber mensagem do servidor
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_box.insert(tk.END, message + '\n', 'message')  # Define a tag 'message' para a mensagem
        except:
            # Erro na conexão com o servidor
            print('Erro na conexão com o servidor')
            client_socket.close()
            break

# Função para enviar mensagens para o servidor
def send_message(event=None):
    message = input_box.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        chat_box.insert(tk.END, f'{client_name}: {message}\n', 'message')  # Define a tag 'message' para a mensagem
        input_box.delete(0, tk.END)
    else:
        input_box.insert(tk.END, 'Digite aqui')  # Adiciona o texto "Digite aqui"

# Função para conectar ao servidor
def connect():
    global client_socket
    global client_name

    # Criar socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Obter o nome do cliente
    client_name = input_name.get()

    # Enviar o nome do cliente para o servidor
    client_socket.send(client_name.encode('utf-8'))

    # Exibir mensagem de conexão
    chat_box.insert(tk.END, f'{client_name} conectou\n', 'system')  # Define a tag 'system' para a mensagem

    # Alterar a interface para a janela de conversa
    name_frame.destroy()
    chat_frame.pack()

    # Criar thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

# Função para desconectar do servidor
def disconnect():
    global client_socket
    global client_name

    # Enviar mensagem de desconexão para o servidor
    client_socket.send('DESCONECTAR'.encode('utf-8'))

    # Exibir mensagem de desconexão
    chat_box.insert(tk.END, f'{client_name} desconectou\n', 'system')  # Define a tag 'system' para a mensagem

    # Fechar o socket do cliente
    client_socket.close()

    # Encerrar a execução do programa
    window.quit()

# Criar janela principal
window = tk.Tk()
window.title('Chat Cliente')

# Definir background como azul claro
window.configure(bg='purple')

# Frame para inserir o nome
name_frame = tk.Frame(window, bg='light blue')
name_frame.pack()

# Entrada para o nome do cliente
name_label = tk.Label(name_frame, text='Nome:', bg='light blue')
name_label.pack(side=tk.LEFT)

input_name = tk.Entry(name_frame)
input_name.pack(side=tk.LEFT)

connect_button = tk.Button(name_frame, text='Conectar', command=connect)
connect_button.pack(side=tk.LEFT)

# Frame para a janela de conversa
chat_frame = tk.Frame(window, bg='light green')

# Área de exibição das mensagens
chat_box = tk.Text(chat_frame, width=50, height=20)
chat_box.pack(side=tk.TOP)
chat_box.tag_configure('message', font=('FixedSys', 12))  # Define a fonte para a tag 'message'

# Scrollbar para a área de exibição das mensagens
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Vincular a scrollbar à área de exibição das mensagens
chat_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_box.yview)

# Entrada para enviar mensagens
input_box = tk.Entry(chat_frame, width=50)
input_box.pack(side=tk.LEFT)
input_box.insert(tk.END, 'Digite aqui')  # Adiciona o texto "Digite aqui"

send_button = tk.Button(chat_frame, text='Enviar', command=send_message, bg='green', fg='white')
send_button.pack(side=tk.LEFT)

# Adiciona um espaço em branco entre os botões
space_label = tk.Label(chat_frame, text=" ", bg='light green')
space_label.pack(side=tk.LEFT)

disconnect_button = tk.Button(chat_frame, text='Desconectar', command=disconnect, bg='red', fg='white')
disconnect_button.pack(side=tk.RIGHT)

# Ocultar a janela de conversa inicialmente
chat_frame.pack_forget()

# Associa a tecla Enter ao envio da mensagem
input_box.bind('<Return>', send_message)

# Iniciar a interface gráfica
window.mainloop()
