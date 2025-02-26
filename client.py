import socket   # Python's built-in networking module
from gachamon import Gachamon
import threading
import time

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith("CHALLENGE"):
                challenger_id = int(message.split()[1])
                print(f"Client {challenger_id} has challenged you to a battle!")
                response = input("Do you accept the challenge? (yes/no): ")
                if response.lower() == "yes":
                    client.send(f"ACCEPT {challenger_id}".encode())
                else:
                    print("Challenge declined.")
            elif message.startswith("MOVE"):
                opponent_id = int(message.split()[1])
                move = message.split()[2]
                print(f"Opponent {opponent_id} made a move: {move}")
            else:
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

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
        client.connect((server_ip, port))
        print("Connected to server!")


        client.send(username.encode())

        # Wait for the server's ready signal before starting
        # This ensures both players are ready to begin
        client.recv(1024).decode()
        
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
                if choice == "1":
                    client.send("LIST".encode())
                elif choice == "2":
                    target_username = input("Enter the username to challenge: ")
                    client.send(f"CHALLENGE {target_username}".encode())
                else:
                    print("Invalid choice")
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