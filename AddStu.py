class AddStu():
    def __init__(self):
        self.student_dict = {}

    def execute(self):
        student_name = input("Please input a student's name or exit: ")

        if student_name.lower() == 'exit':
            return {}

        if student_name not in self.student_dict:
            self.student_dict[student_name] = {}

        while True:
            subject_name = input("  Please input a subject name or exit for ending: ")
            if subject_name.lower() == "exit":
                print(f"    Add {student_name}'s scores successfully.")
                break

            if subject_name in self.student_dict[student_name]:            
                print(f"  {student_name} already has a score for {subject_name}.")
            else:
                score_input = input(f"  Please input {student_name}'s {subject_name} score or < 0 for discarding the subject: ")
                try:
                    score = float(score_input)
                    if score < 0:
                        continue
                    else:
                        self.student_dict[student_name][subject_name] = score
                        print(f"    Add {student_name}'s {subject_name} score: {score}")
                except ValueError as e:
                    print(f"    Wrong format with reason: {e}, please try again.")

        return {'name': student_name, 'scores': self.student_dict[student_name]}