import socket   # Python's built-in networking module
import threading
import random
from gachamon import Gachamon
import time

# List to keep track of connected clients
clients = []

def handle_client(conn, addr, client_id):
    print(f"New connection from {addr}")
    conn.send("ready".encode())
    
    try:
        while True:
            # Receive data from client
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received from {addr}: {data}")

            if data == "LIST":
                # Send the list of connected clients to the requesting client
                client_list = "Connected clients:\n" + "\n".join([f"Client {i}" for i in range(len(clients))])
                conn.send(client_list.encode())
            elif data.startswith("CHALLENGE"):
                target_id = int(data.split()[1])
                if target_id < len(clients):
                    clients[target_id].send(f"CHALLENGE {client_id}".encode())
                else:
                    conn.send("Invalid client ID".encode())
            elif data.startswith("ACCEPT"):
                opponent_id = int(data.split()[1])
                if opponent_id < len(clients):
                    start_battle(client_id, opponent_id)
                else:
                    conn.send("Invalid client ID".encode())
            elif data.startswith("MOVE"):
                opponent_id = int(data.split()[1])
                move = data.split()[2]
                if opponent_id < len(clients):
                    clients[opponent_id].send(f"MOVE {client_id} {move}".encode())
                else:
                    conn.send("Invalid client ID".encode())



    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Connection with {addr} closed")

def start_battle(client1_id, client2_id):
    first_turn = random.choice([client1_id, client2_id])
    clients[first_turn].send("Your turn".encode())
    clients[1 - first_turn].send("Opponent's turn".encode())

def main():
    # Create a new TCP socket for network communication
    # TCP ensures reliable, ordered data delivery between the client and server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the port number from user input
    # Ports are like specific channels that network traffic can flow through
    port = int(input("Enter port number: "))

    # Bind the server to listen on all available network interfaces ('')
    # This allows connections from any IP address that can reach this computer
    server.bind(('', port))
    
    # Start listening for incoming connections
    # The parameter 1 means we only allow one connection in the waiting queue
    server.listen(6)
    print(f"Server started on port {port}")

    while True:
    # accept() blocks (waits) until a client connects
    # It returns a new socket specifically for this connection and the client's address
        conn, addr = server.accept()
        clients.append(conn)

        # Assign client ID based on the order of connection
        client_id = len(clients) - 1

        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")  

# Only run the server if this file is run directly (not imported)
if __name__ == "__main__":
    main()