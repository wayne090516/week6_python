import socket 
import json
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

action_list = {
    "add": AddStu,  
    "show": PrintAll
}

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))
 
    def send_command(self, command, parameters):
        send_data = {'command': command, 'parameters': parameters}
        print(f"    The client sent data => {send_data}")
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(f"    The client received data => {raw_data}")

        if raw_data == "closing":
            return False
        
        return True, json.loads(raw_data)

class HandleCommand:
    def __init__(self, client, action_list):
        self.client = client
        self.action_list = action_list
        self.student_dict = dict()
        self.keep_going = True

    def execute(self, command):
        command_mapping = {
            'add': self.handle_add,
            'show': self.handle_show,
            'exit': self.handle_exit
        }

        if command in command_mapping:
            return command_mapping[command]()
        else:
            print("### Hold up, unknown command ###")
            return True

    def handle_add(self):
        try:
            self.student_dict = self.action_list['add'](self.student_dict).execute()
            self.client.send_command('add', self.student_dict)
            self.keep_going, raw_data = self.client.wait_response()
            if raw_data['status'] == 'OK':
                print(f"    Add {self.student_dict} success")
            elif raw_data['status'] == 'Fail':
                print(f"    Add {self.student_dict} fail")

        except Exception as e:
            print(e)

        return self.keep_going

    def handle_show(self):
        try:
            self.client.send_command('show', {})
            self.keep_going, raw_data = self.client.wait_response()
            self.student_dict = self.action_list['show'](raw_data).execute()

        except Exception as e:
            print(e)

        return self.keep_going

    def handle_exit(self):
        self.keep_going = False

        return self.keep_going

def print_menu():
    print()
    print("add: Add a student's name and score")
    print("show: Print all")
    print("exit: Exit")
    selection = input("Please select: ")
    return selection

if __name__ == '__main__':
    client = SocketClient(host, port)

    handler = HandleCommand(client, action_list)

    while handler.keep_going:
        command = print_menu()
        handler.keep_going = handler.execute(command)