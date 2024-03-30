import socket 
import json
import sys
host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))
        self.student_dict = {'name':None,'scores':{}}
        self.parameters ={'name':None,'scores':{}}

    def add(self):
        while True:
            name = input("Please input a student's name or type 'exit' to end: ")
            if name == 'exit':
                client.send_command(command,self.student_dict)
                client.wait_response()
                break
            else:
                self.student_dict = {'name':None,'scores':{}}
                while True:
                    subject = input("Please input a subject name or type 'exit' to end: ")
                    if subject == 'exit':
                        break
                    while True:
                        score = input(f"Please input {name}'s {subject} score or < 0 to discard the subject: ")
                        try:
                            score = float(score)
                            if score >= 0:
                                self.student_dict['name'] = name
                                self.student_dict['scores'][subject] = score
                                break
                            else:
                                print("Score discarded.")
                                break
                        except ValueError:
                            print("Wrong format: could not convert string to float:", score, "try again.")
    def show(self):
        print ("\n==== student list ====\n")
        for person, info in self.parameters.items():
            print("Name:", person)
            for subject, score in info['scores'].items():
                print(f"  subject: {subject}, score: {score}")
            print()
        print ("======================")

    def send_command(self, command,parameters = None):
        if parameters is None:
            parameters = {}
        send_data = {'command': command, 'parameters': parameters}
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(raw_data)
        
        if raw_data == "closing":
            self.client_socket.close()
            return False
        try:
            response_json = json.loads(raw_data)
            parameters = response_json.get('parameters')
            if parameters is not None:
                self.parameters = dict(parameters)
        except json.JSONDecodeError:
            print("Invalid JSON data received.")
        return True

if __name__ == '__main__':
    client = SocketClient(host, port)

    keep_going = True
    while keep_going:
        print("Commands:")
        print("add: Add a student's name and score")
        print("show: Show all students and their scores")
        print("exit: Exit the program")
        command = input(">>> ")
        if command == 'add':
            client.add()
            continue
        elif command == 'show':
            client.send_command(command)
            client.wait_response()
            client.show()
            continue
        elif command == 'exit':
            client.client_socket.close()
            sys.exit()
        else:
            keep_going = client.wait_response()