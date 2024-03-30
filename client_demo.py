import socket 
import json
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

def print_menu():
    print()
    print("add: Add a student's name and score")
    print("show: Print all")
    print("exit: Exit")
    selection = input("Please select: ")

    return selection



action_list = {
    "add": AddStu,   
    "show": PrintAll
}

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))       

    def send_command(self, command, parameters=None):
        if parameters is None:
            parameters = {}
        send_data = {'command': command, 'parameters': parameters}
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print("Received data:", raw_data)
        if raw_data == "closing":
            return False        
        try:
            response = json.loads(raw_data)
            return response
        except json.JSONDecodeError:
            print("Error decoding JSON:", raw_data)
            return False

if __name__ == '__main__':
    client = SocketClient(host, port)

    keep_going = True
    while keep_going:
        command = print_menu()
        try:
            if command == 'exit':
                break
            if command in action_list: 
                response = action_list[command](client).execute()              
            else:
                print("Invalid command.")
        except Exception as e:
            print(e) 
