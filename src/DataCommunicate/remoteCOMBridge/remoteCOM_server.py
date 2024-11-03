import serial
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

CLI_COM = "COM16"
DATA_COM = "COM17"

BUF_SIZE = 4096

def handle_client(conn: socket):
    try:
        while True:
            try:
                if cliCom.in_waiting > 0:
                    serial_data = cliCom.read(cliCom.in_waiting)
                    conn.sendall(serial_data)
            except serial.SerialException as e:
                print("Error with reading from cliCom: " + e)
                
            try:
                data = conn.recv(BUF_SIZE)
                if not data:
                    print("No data received from client, closing connection")
                    break
                
                print(f"Recieved: {data}")
            except socket.error as e:
                print("socket error during data reception: " + e)
                break
    finally:
        conn.close()
        server_sock.close()

if __name__ == "__main__":
    try:
        cliCom = serial.Serial(CLI_COM, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.6)
        dataCom = serial.Serial(DATA_COM, baudrate=921600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.6)
        dataCom.reset_output_buffer()
    except serial.SerialException as e:
        print("Error with opening serial ports: " + e)
        exit(1)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_sock.bind((HOST, PORT))
        server_sock.listen()
    except socket.error as e:
        print("Socket error: " + e)
        server_sock.close()
        exit(1)

    conn, addr = None, None
    try:
        conn, addr = server_sock.accept()
        print(f"connected by {addr}")
    except socket.error as e:
        print("Error with accepting connection: " + e)
        server_sock.close()
        exit(1)

    handle_thread = threading.Thread(target=handle_client, args=(conn,))
    handle_thread.start()

    handle_thread.join()

