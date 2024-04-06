import socket
import threading

def listen_on_port(port=32100):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()
    print(f"Listening on port {port}...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")

listener_thread = threading.Thread(target=listen_on_port)
listener_thread.start()
