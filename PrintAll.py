class PrintAll:
    def __init__(self,client):
        self.client = client

    def execute(self):
        self.client.send_command("show",{})
        received_data = eval(self.client.wait_response()) 
        student_dict= (received_data)["parameters"]
        print ("\n==== student list ====\n")
        for key in student_dict:
            print(f"Name: {key}")
            score=student_dict[key]
            for subject in score:
                print("  subject: {}, score: {}".format(subject,score[subject]))
            print("")
        print ("======================")
        return 0