import socket   # Python's built-in networking module
from gachamon import Gachamon
import time

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
    server.listen(1)
    print(f"Server started on port {port}")

    # Initialize the game board and ships
    game = Gachamon()
    print("\nWaiting for opponent...")

    # accept() blocks (waits) until a client connects
    # It returns a new socket specifically for this connection and the client's address
    conn, addr = server.accept()
    print(f"Opponent has connected from {addr}!")
    
    # Send a ready signal to the client to synchronize game start
    conn.send("ready".encode())
    
    print("game starting")
    # game.gacha()

    try: # keeps the game running
        while True:
            print("game online")

            turn = True

            #send back the result
            conn.send(turn.encode())











    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up network resources when the game ends
        conn.close()
        server.close()   


# Only run the server if this file is run directly (not imported)
if __name__ == "__main__":
    main()