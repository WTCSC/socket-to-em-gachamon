import socket   # Python's built-in networking module
import threading
import random
from gachamon import Gachamon
import time

# List to keep track of connected clients
clients = {}
usernames = {}

def handle_client(conn, addr):
    # Receive and store the username
    username = conn.recv(1024).decode()
    clients[username] = conn
    usernames[conn] = username
    print(f"New connection from {addr} with username {username}")
    conn.send("ready".encode())

    try:    
        while True:
            # Receive data from client
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received from {addr}: {data}")

            match data.split():
                case ["LIST"]:
                    # Send the list of connected clients to the requesting client
                    client_list = "Connected clients:\n" + "\n".join(usernames.values())
                    conn.send(f"LIST {client_list}".encode())
                case ["CHALLENGE", target_username]:
                    if target_username in clients:
                        clients[target_username].send(f"CHALLENGE {usernames[conn]}".encode())
                    else:
                        conn.send("ERROR User not found".encode())
                case ["ACCEPT", opponent_username]:
                    if opponent_username in clients:
                        first_player = random.choice([username, opponent_username])
                        Turn1 = "1" if first_player == username else "2"
                        Turn2 = "1" if first_player == opponent_username else "2"
                        opponent_username.send(f"Battle {username} {Turn1}".encode())
                        username.send(f"Battle {opponent_username} {Turn2}".encode())
                    else:
                        conn.send("ERROR Challenger not found".encode())    
                case ["DECLINE", opponent_username]:
                    if opponent_username in clients:
                        clients[opponent_username].send("DECLINE".encode())
                case _:
                    print(f"Unknown command: {data}")

    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        del clients[usernames[conn]]
        del usernames[conn]
        print(f"Connection with {addr} closed")

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
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")  

# Only run the server if this file is run directly (not imported)
if __name__ == "__main__":
    main()