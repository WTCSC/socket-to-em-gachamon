import socket   # Python's built-in networking module
from gachamon import Gachamon
import threading
import time
import os

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            e = message.split()
            e = e[0]
            match e:
                case ["CHALLENGE", challenger_id]:
                    print(f"Client {challenger_id} has challenged you to a battle!")
                    response = input("Do you accept the challenge? (yes/no): ")
                    if response.lower() == "yes":
                        client.send(f"ACCEPT {challenger_id}".encode())
                    else:
                        print("Challenge declined.")
                case ["MOVE", opponent_id, move]:
                    print(f"Opponent {opponent_id} made a move: {move}")
                case ["LIST"]:
                    client_list = message.split(" ", 1)[1]
                    clear_terminal()
                    print(client_list + "\n \n")
                case _:
                    print("sent nothing")
                    print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Create a TCP socket for client-server communication
    # TCP (Transmission Control Protocol) ensures reliable data transfer
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get connection details from the user
    # The IP address identifies the server computer on the network
    server_ip = input("Enter server IP address: ")

    # The port number must match the server's port for successful connection
    port = int(input("Enter server port: "))
    
    username = input("Enter your username: ")

    try:
        # Attempt to establish a connection to the server
        # If the server isn't running, this will raise an exception
        print("Waiting for server's ready signal...")
        client.connect((server_ip, port))
        print("Connected to server!")

        time.sleep(2)
        clear_terminal()
        # Send the client's username to the server
        client.send(username.encode())

        # Initialize the game board and randomly place ships
        game = Gachamon()
        print("you have joined the game")

        # Start a thread to receive messages from the server
        threading.Thread(target=receive_messages, args=(client,)).start()

        while True:
            print("1. View connected clients")
            print("2. Challenge a client to a battle")
            choice = input("Enter your choice: ")

            try:
                match choice:
                    case "1":
                        client.send("LIST".encode())
                    case "2":
                        target_username = input("Enter the username to challenge: ")
                        client.send(f"CHALLENGE {target_username}".encode())
                    case _:
                        print("Invalid choice")
                        time.sleep(1)
                        clear_terminal()
            except Exception as e:
                print(f"Error sending message: {e}")
    #connection status              
    except ConnectionRefusedError:
        # This exception occurs when we can't connect to the server
        print("Could not connect to server. Make sure server is running and address is correct.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Error: {e}")
    finally:
        # Always close the network connection when we're done
        client.close()

# Only run the client if this file is run directly
if __name__ == "__main__":
    main()