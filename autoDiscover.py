import socket
import threading
import ipaddress

discovered_devices = []

def handle_client(client_socket):
    with client_socket as sock:
        try:
            while True:
                message = sock.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n\n\nNEW MESSAGE:\n----------------\nMessage from {sock.getpeername()}: {message}\n----------------\n")
        except ConnectionResetError:
            print(f"Connection with {sock.getpeername()} was lost.")

def listen_on_port(port=32100):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen()
    print(f"Listening on port {port} for incoming messages...")
    while True:
        client_socket, address = server_socket.accept()
        # print(f"Connection from {address} has been established.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def send_message(target_ip, message, port=32100):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((target_ip, port))
            sock.sendall(message.encode('utf-8'))
            print("Message sent successfully.")
        except Exception as e:
            print(f"Could not send message to {target_ip}: {e}")

def scan_port(ip, port=32100):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            discovered_devices.append(ip)
            # print(f"Device found at {ip}")
        sock.close()
    except Exception as e:
        print(f"Error scanning {ip}: {e}")

def scan_network(network, port=32100):
    for ip in ipaddress.IPv4Network(network):
        threading.Thread(target=scan_port, args=(str(ip), port)).start()

def user_interface():
    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            if not discovered_devices:
                print("No devices discovered on the network. Please ensure the network scan has completed.")
            else:
                print("Discovered Devices:")
                for idx, ip in enumerate(discovered_devices, start=1):
                    print(f"{idx}. {ip}")
                try:
                    selection = int(input("Select a device to message by number: ")) - 1
                    target_ip = discovered_devices[selection]
                    message = input("Enter your message: ")
                    send_message(target_ip, message)
                except (ValueError, IndexError):
                    print("Invalid selection. Please enter a valid number.")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    # Replace '192.168.0.0/24' with your actual LAN subnet to scan
    scan_network('192.168.0.0/24')

    # Start the listening server in a separate thread
    threading.Thread(target=listen_on_port, daemon=True).start()

    # Start the user interface in the main thread
    user_interface()
