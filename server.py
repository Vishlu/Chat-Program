import socket
import threading
import tkinter as tk
#192.168.0.105
# Function to start the server
def start_server():
    global server_thread
    if not server_thread or not server_thread.is_alive():
        server_thread = threading.Thread(target=main_server)
        server_thread.start()
        status_label.config(text="Server is running", fg="green")
    else:
        status_label.config(text="Server is already running", fg="red")

# Function to stop the server
def stop_server():
    global server_socket
    try:
        server_socket.close()
        status_label.config(text="Server is stopped", fg="red")
    except Exception as e:
        print(f"Error stopping server: {str(e)}")

# Main server function
def main_server():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 1234

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        status_label.config(text=f"Server is listening on {host}:{port}", fg="green")

        while True:
            client_socket, client_address = server_socket.accept()
            client_name = client_socket.recv(1024).decode()
            print(f"{client_name} has connected from {client_address}")
            clients.append((client_socket, client_name))
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
            client_handler.start()
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

# Function to handle each client connection
def handle_client(client_socket, client_name):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"{client_name} has disconnected.")
                break
            print(f"{client_name}: {message}")
            # Broadcast the message to all connected clients
            broadcast(message, client_name)
    except Exception as e:
        print(f"Error handling {client_name}: {str(e)}")
    finally:
        client_socket.close()

# Function to broadcast a message to all clients
def broadcast(message, sender_name):
    for client, name in clients:
        if client != sender_name:
            try:
                client.send(f"{sender_name}: {message}".encode())
            except Exception as e:
                print(f"Error broadcasting to {name}: {str(e)}")

# Initialize the GUI
root = tk.Tk()
root.title("Server Control Panel")

start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Server", command=stop_server)
stop_button.pack(pady=10)

status_label = tk.Label(root, text="Server is not running", fg="red")
status_label.pack()

clients = []  # List to store client sockets and names
server_socket = None
server_thread = None

root.mainloop()
