import socket
import threading

# Dados do servidor
HOST = '172.16.31.43'  # IP do servidor
PORT = 5001  # Porta para conexão

# Lista de clientes conectados
clients = []

# Função para receber mensagens de um cliente específico
def receive_messages(client_socket):
    while True:
        try:
            # Receber mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f'Mensagem recebida: {message}')

                # Transmitir mensagem para os outros clientes
                transmit_message(message, client_socket)
        except:
            # Erro na conexão com o cliente
            print('Erro na conexão com o cliente')
            clients.remove(client_socket)
            client_socket.close()
            break

# Função para transmitir mensagem para todos os clientes, exceto o remetente original
def transmit_message(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                # Enviar mensagem para o cliente
                client_socket.send(message.encode('utf-8'))
            except:
                # Erro na conexão com o cliente
                clients.remove(client_socket)

# Função para lidar com a conexão de um novo cliente
def handle_client_connection(client_socket):
    clients.append(client_socket)
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

# Função para iniciar o servidor
def start_server():
    # Criar socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # Aguardar conexões de clientes
    server_socket.listen(10)  # Aumentar o backlog para 10 (pode ajustar conforme necessário)
    print('Aguardando conexões de clientes...')

    while True:
        # Aceitar conexões de clientes
        client_socket, client_address = server_socket.accept()
        print('Conexão estabelecida com', client_address)

        # Lidar com a conexão do novo cliente em uma nova thread
        handle_client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        handle_client_thread.start()

# Iniciar o servidor
start_server()
