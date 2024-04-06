import socket
import threading
import ipaddress

def listen_on_port(port=32100):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()
    print(f"Listening on port {port}...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")

def scan_port(ip, port=32100):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Device found at {ip}")
        sock.close()
    except Exception as e:
        print(f"Error scanning {ip}: {e}")

def scan_network(network, port=32100):
    for ip in ipaddress.IPv4Network(network):
        threading.Thread(target=scan_port, args=(str(ip), port)).start()

if __name__ == "__main__":
    # Start the listening server in a separate thread
    listener_thread = threading.Thread(target=listen_on_port)
    listener_thread.start()

    # Start the network scan in the main thread
    # Replace '192.168.0.0/24' with your actual LAN subnet
    scan_network('192.168.0.0/24')
