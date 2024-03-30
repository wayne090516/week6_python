class AddStu:
    def __init__(self, socket_client):
        self.socket_client = socket_client

    def execute(self):
        student_data = {'name': None, 'scores': {}}
        student_data['name'] = input("Please input a student's name: ")
        while True:
            subject = input("Please input a subject name or exit for ending: ")
            if subject == 'exit':
                break
            try:
                score = float(input(f"Please input {student_data['name']}'s {subject} score or < 0 for discarding the subject: "))
                if score >= 0:
                    student_data['scores'][subject] = score
            except ValueError:
                print("Invalid score input. Please try again.")

        self.socket_client.send_command('add', student_data)
        response = self.socket_client.wait_response()

        if response and response['status'] == 'OK':
            print(f"Add name {student_data['name']}, scores {student_data['scores']} success.")
        else:
            print(f"name {student_data['name']} , scores {student_data['scores']} fail.")

        return response
