import socket

def start_server():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Allow connections from any IP
    port = 12345       # Port number

    # Bind the socket to the address and port
    server_socket.bind((host, port))
    server_socket.listen(1)  # Allow one connection for simplicity
    print(f"Server running on {host}:{port}")

    # Wait for a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Client connected from: {client_address}")

    while True:
        try:
            # Get command input from the user
            command = input("Enter command for the client (type 'exit' to quit): ")
            if command.lower() == 'exit':
                break

            # Send the command to the client
            client_socket.send(command.encode('utf-8'))

            # Receive response from the client
            response = client_socket.recv(4096).decode('utf-8')  # Increased buffer size
            print(f"Client response: {response}")

        except Exception as e:
            print(f"Error: {e}")
            break

    # Close the connection
    client_socket.close()
    server_socket.close()
    print("Connection closed.")

if __name__ == "__main__":
    start_server()
