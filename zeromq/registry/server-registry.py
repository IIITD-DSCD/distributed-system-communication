import zmq
import threading
import json
cxt = zmq.Context()
mutex = threading.Lock()

class ServerRegistry:
    def __init__(self):
        self.MAXSERVERS = 10
        self.current_registered=0
        self.server_list={}

    def start(self):
        self.__setup()
        print("STARTING SERVER REGISTRY...")
        while True:
            with mutex:
                try:
                    request = self.__registry_socket.recv()
                    self.__handle_request(request)
                except zmq.Again:
                    print("No Message")
                    continue
            
    def __setup(self):
        self.__registry_socket = cxt.socket(zmq.REP)
        self.__registry_socket.setsockopt(zmq.SNDTIMEO, 1000)
        self.__registry_socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.__registry_socket.bind("tcp://127.0.0.1:5556")
    
    def __handle_request(self, req):
        args = req.decode()

        request = json.loads(args)        
        if (request['request_type']=='register'):
            self.register_server(request['arguments'])
        elif (request['request_type']=='get_server_list'):
          
            self.get_server_list(request['arguments'])
        
    def get_server_list(self, args):
        print("COMING SOON")

    def register_server(self, args):
        
        print(f"JOIN REQUEST FROM {args['address']} [ADDRESS]")
        status='FAIL'
        if(self.current_registered<self.MAXSERVERS):
            status='SUCCESS'
            self.server_list[args['name']]=args['address']
            self.current_registered+=1
        self.__registry_socket.send_string(json.dumps({'request_type':'register', 'response':status}))


registry = ServerRegistry()

registry.start()