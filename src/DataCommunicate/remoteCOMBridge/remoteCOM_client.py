import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

BUF_SIZE = 4096

def receive_data(sock: socket):
    while True:
        data = sock.recv(BUF_SIZE)
        if not data:
            break
        print(f"Received from server: {data}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receiver_thread = threading.Thread(target=receive_data, args=(client_socket,))
receiver_thread.start()

try:
    while True:
        message = input("Enter message to send: ")
        client_socket.sendall(message.encode())  # Send data to the server
finally:
    client_socket.close()  # Close the client socket
    receiver_thread.join()  # Wait for the receiver thread to finish