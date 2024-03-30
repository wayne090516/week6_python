import socket 
import json
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))

    def send_command(self, command, parameters):
        send_data = {'command': command, 'parameters': parameters}
        print(f"The client sent data => {send_data}")
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
            data = self.client_socket.recv(BUFFER_SIZE)
            raw_data = data.decode()
            keep_going = True

            if raw_data == "closing":
                keep_going = False
            else:
                raw_data = json.loads(raw_data)
            print(f"The client received data => {raw_data}")
            return keep_going, raw_data

if __name__ == '__main__':
    client = SocketClient(host, port)
    keep_going = True

    while keep_going:
        try:
            command_type = input("\nadd: Add a student's name and score\nmodify: Modify a student's score\nexit: Exit\nPlease select: ")

            if command_type == 'add':
                parameters = AddStu().execute()  
                client.send_command('add', parameters)
                keep_going = client.wait_response()

            elif command_type == 'show':
                client.send_command('show', {})
                keep_going, response = client.wait_response()
                PrintAll(response).execute()  

            elif command_type == 'exit':
                break

            else:
                print("The selection isn't exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            continue