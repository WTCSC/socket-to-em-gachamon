import socket   # Python's built-in networking module
from gachamon import Gachamon
import time

def main():
    # Create a TCP socket for client-server communication
    # TCP (Transmission Control Protocol) ensures reliable data transfer
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get connection details from the user
    # The IP address identifies the server computer on the network
    server_ip = input("Enter server IP address: ")

    # The port number must match the server's port for successful connection
    port = int(input("Enter server port: "))
    
    try:
        # Attempt to establish a connection to the server
        # If the server isn't running, this will raise an exception
        client.connect((server_ip, port))
        print("Connected to server!")
        
        # Wait for the server's ready signal before starting
        # This ensures both players are ready to begin
        client.recv(1024).decode()
        
        # Initialize the game board and randomly place ships
        game = Gachamon()
        print("you have joined the game")

        try: # keeps the game running
            while True:
                print("game online")

                turn = "heads"

                client.send(turn.encode())
                response = client.recv(1024).decode()

                if response == True:
                    print("response resived")
















        except ConnectionRefusedError:
        # This exception occurs when we can't connect to the server
            print("Could not connect to server. Make sure server is running and address is correct.")
        except Exception as e:
        # Handle any other unexpected errors
            print(f"Error: {e}")
        finally:
        # Always close the network connection when we're done
            client.close()
    
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