class AddStu:
    def __init__(self,client):
        self.client = client

    def execute(self):
        name=input("  Please input a student's name or exit:")
        if name=="exit":
            return 0
        else:
            add_dict=dict()
            subject=input("  Please input a subject name or exit for ending:")  
            while subject!="exit":
                score=""
                while score=="":   
                    score=input(f"  Please input {name}'s {subject} score or < 0 for discarding the subject: ")
                    try:
                        score=int(score)
                        if score>0:
                            add_dict[subject]=score
                    except :  
                        print(f"    Wrong format with reason could not convert string to float: {score}, try again")
                        score=""
                subject=input("  Please input a subject name or exit for ending:")
        self.client.send_command("add", {'name': name, 'scores': add_dict})
        if eval(self.client.wait_response())["status"] == "OK":
            print(f"Add {add_dict} success")
        else:
            print(f"Add {add_dict} failed")
        return 0