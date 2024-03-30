class PrintAll:
    def __init__(self, socket_client):
        self.socket_client = socket_client

    def execute(self):
        self.socket_client.send_command("show", {})
        response = self.socket_client.wait_response()

        if response is False:
            print("Server closed the connection unexpectedly.")
            return

        if response['status'] != 'OK':
            print("Error: {}".format(response['message']))
            return

        parameters = response.get('parameters', {})
        
        print("\n==== student list ====\n")
        for name, details in parameters.items():
            print(f"Name: {name}")
            for  subject, score in details['scores'].items():
                print(f" Subject: {subject}, Score: {score}")
        print("\n======================")
        