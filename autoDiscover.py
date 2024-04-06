import socket
import threading
import time

def listen_for_connections(port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind(('', port))
        listener.listen(5)
        print(f"Listening on port {port}...")
        while True:
            client, address = listener.accept()
            print(f"Received connection from {address[0]}:{address[1]}")
            client.sendall(f"Hello from {socket.gethostname()}!".encode())
            client.close()
    except Exception as e:
        print(f"Error in listener: {e}")
    finally:
        listener.close()

def scan_network_continuously(port, own_ip):
    while True:
        print("Starting network scan...")
        for ip in range(1, 255):
            ip_address = f"192.168.1.{ip}"
            if ip_address == own_ip:
                continue
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    if s.connect_ex((ip_address, port)) == 0:
                        print(f"Device found at {ip_address}:{port}")
                        s.sendall(f"Hello from {own_ip}:{port}".encode())
                        response = s.recv(1024).decode()
                        print(f"Received response: {response}")
            except Exception as e:
                print(f"Error scanning {ip_address}: {e}")
        print("Network scan complete. Restarting in 10 seconds...")
        time.sleep(10)  # Wait for 10 seconds before starting the next scan

if __name__ == "__main__":
    port = 32100

    # Start listening thread
    listener_thread = threading.Thread(target=listen_for_connections, args=(port,))
    listener_thread.start()
    time.sleep(1)  # Give the listener thread time to start

    # Get own IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        own_ip = s.getsockname()[0]
    except Exception:
        own_ip = '127.0.0.1'
    finally:
        s.close()

    print(f"My IP address is {own_ip}")

    # Continuously scan the network
    scan_network_continuously(port, own_ip)
