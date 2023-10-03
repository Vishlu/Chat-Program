import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, END

# Function to send messages
def send_message():
    message = entry.get()
    if message:
        client_socket.send(message.encode())
        entry.delete(0, END)

# Function to receive messages
def receive_messages():
    try:
        while True:
            message = client_socket.recv(1024).decode()
            chat_text.config(state="normal")
            chat_text.insert(tk.END, message + "\n")
            chat_text.config(state="disabled")
    except Exception as e:
        print(f"Error receiving message: {str(e)}")

# Main client function
def main():
    global client_socket, entry, chat_text

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Enter server address: ")
    port = 1234

    try:
        client_socket.connect((host, port))
        name = input("Enter your name: ")
        client_socket.send(name.encode())
        print("Connected to server. Start typing your messages (enter 'e' to exit).")

        # Create a GUI window
        root = tk.Tk()
        root.title("Vishal Chat Room")

        # Create a chat text area
        chat_text = scrolledtext.ScrolledText(root, state="disabled", wrap=tk.WORD)
        chat_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        chat_text.config(state="disabled")

        # Create an entry field for typing messages
        entry = tk.Entry(root, width=50)
        entry.grid(row=1, column=0, padx=10, pady=10)

        # Create a send button
        send_button = tk.Button(root, text="Send", command=send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        root.mainloop()
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")

if __name__ == "__main__":
    main()
