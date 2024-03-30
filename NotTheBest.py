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

def print_menu():
    print()
    print("add: Add a student's name and score")
    print("show: Print all")
    print("exit: Exit")
    selection = input("Please select: ")
    return selection

if __name__ == '__main__':
    client = SocketClient(host, port)

    keep_going = True
    while keep_going:
        command = print_menu()
        student_dict = dict()

        if command == 'add':
            try:
                student_dict = action_list[command](student_dict).execute()
                client.send_command(command, student_dict)
                keep_going, raw_data = client.wait_response() 
                if raw_data['status'] == 'OK':
                    print(f"    Add {student_dict} success")
                elif raw_data['status'] == 'Fail':
                    print(f"    Add {student_dict} fail")

            except Exception as e:
                print(e)

        if command == 'show':
            try:
                client.send_command(command, student_dict)
                keep_going, raw_data = client.wait_response() 
                student_dict = action_list[command](raw_data).execute()
                
            except Exception as e:
                print(e)   

        if command == 'exit':
            keep_going = False