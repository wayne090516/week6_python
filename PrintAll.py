class PrintAll:

    def __init__(self, raw_data):
        self.dict = raw_data

    def execute(self):
        print("\n==== student list ====\n")
        for key, value in self.dict['parameters'].items():
            print(f"Name: {key}")
            for subject, score in value['scores'].items():
                print(f"  subject: {subject}, score: {score}")
            print()
        print("\n======================")
