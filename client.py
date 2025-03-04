import socket   # Python's built-in networking module
from gachamon import Gachamon
import threading
import time
import os

# Flag to control the flow between receive_messages and choices
continue_choices = True
gacha_Battle = False
P1 = "x" #defult player 1 variable
P2 = "y" #defult player 2 variable
turn = False

def receive_messages(client):
    global continue_choices
    global gacha_Battle
    global P1
    global P2
    global turn

    while True:
        try:
            message = client.recv(1024).decode()
            request = message.split()[0]
            match request:
                case "CHALLENGE":
                    challenger_id = message.split(" ", 1)[1]
                    print(f"Client {challenger_id} has challenged you to a battle!")
                    response = input("Do you accept the challenge? (yes/no): ")
                    if response.lower() == "yes":
                        client.send(f"ACCEPT {challenger_id}".encode())
                    else:
                        print("Challenge declined.")
                        client.send(f"DECLINE {challenger_id}".encode())
                        continue_choices = True  # Allow choices to be shown again
                case "DECLINE":
                    print("Challenge declined.")
                    continue_choices = True  # Allow choices to be shown again
                case "LIST":
                    client_list = message.split(" ", 1)[1]
                    clear_terminal()
                    print(client_list + "\n \n" + "enter to continue:")
                    input()  # Wait for user to press Enter
                    continue_choices = True  # Allow choices to be shown again
                case "Battle":
                    challenger_id = message.split(" ", 1)[1]
                    TurnS = message.split(" ", 2)[2]
                    if TurnS == "1":
                        turn = True
                    else:
                        turn = False
                    P1 = "you"
                    P2 = challenger_id
                    print(f"Battle with {challenger_id} has started!")
                    time.sleep(1)
                    clear_terminal()
                    gacha_Battle = True # Start the battle
                case "MOVE":
                    move = message.split(" ", 1)[1]
                    print(f"Opponent's move: {move}")
                case _:
                    print("sent nothing")
                    print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    global continue_choices
    global gacha_Battle
    global P1
    global P2
    global turn

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
        time.sleep(1)
        # Start a thread to receive messages from the server
        threading.Thread(target=receive_messages, args=(client,)).start()
        clear_terminal()

        while True:
            if continue_choices:
                print("1. View connected clients")
                print("2. Challenge a client to a battle")
                choice = input("Enter your choice: ") 
  
                try:
                    match choice:
                        case "1":
                            client.send("LIST".encode())
                            continue_choices = False  # Wait for LIST response
                        case "2":
                            target_username = input("Enter the username to challenge: ")
                            client.send(f"CHALLENGE {target_username}".encode())
                            continue_choices = False  # Wait for CHALLENGE response
                        case _:
                            print("Invalid choice")
                            time.sleep(1)
                            clear_terminal()
                except Exception as e:
                    print(f"Error sending message: {e}")

            if gacha_Battle:
                print(f"{P1} vs {P2}")
                time.sleep(1)   
                clear_terminal()
                while True:
                    try: 
                        if turn == True:
                            print("It's your turn!")
                            move = input("Enter your move: ")
                            client.send(f"MOVE {move}".encode())
                            turn = False
                        else:
                            # OPPONENT'S TURN
                            print("\nWaiting for opponent's move...")
                            message = client.recv(1024).decode()
                            if message.startswith("MOVE"):
                                turn = True

                        if game == "over":
                            print("Game Over")
                            gacha_Battle = False
                            continue_choices = True
                            break
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