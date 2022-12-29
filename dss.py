import zmq
import multiprocessing
import sys

# for compatibility with Python 2.7 and 3
try:
    from Queue import Empty, Full
except ImportError:
    from queue import Empty, Full
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# This is the file which contains your user-defined functions (to be given to
# the machines for execution)
from functions import *

# Added import for zmq Context and REQ socket type
# Added import for CurveZMQ security options

class machine():
    'Class for the instance of a machine'

    def __init__(self):
        # Added security measures to the socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.CURVE_SECRETKEY, b'secret')

    def execute_func(self, func_name, *user_args):
        list_of_args = [self]
        for arg in user_args:
            list_of_args.append(arg)
        arguments = tuple(list_of_args)

        # Added try-except block to catch any exceptions that may occur during execution
        try:
            if(func_name in globals()):
                iprocessing.Process(target=globals().get(func_name), args=arguments).start()
            else:
                raise NameError("name '" + func_name + "'is not defined")
        except Exception as e:
            print("Exception in execute_func():", e)

    def send(self, destination_id, message, is_blocking):
        # send message to the machine with machine_id destination_id

        try:
            # Connect to the destination machine using its address
            self.socket.connect(destination_id)
            # Send the message using the REQ socket
            self.socket.send_string(message)
            # Receive the response from the destination machine
            response = self.socket.recv_string()
            # Disconnect from the destination machine
            self.socket.disconnect(destination_id)
        except Exception as e:
            print("Exception in send():", e)
            return -1

        return 1

    def recv(self, is_blocking):
        # Added try-except block to catch any exceptions that may occur during execution
        try:
            # Receive the message from the REQ socket
            message = self.socket.recv_string()
            # Send the response to the sender
            self.socket.send_string('Received')
        except Exception as e:
            print("Exception in recv():", e)
            return -1, -1

        return message, 1

    def get_id(self):
        return self.socket.getsockopt(zmq.CURVE_PUBLICKEY)

    def get_machine_id(self):
        return 'machine_' + str(self.get_id())

    def get_machine_ip(self):
        return self.socket.getsockopt(zmq.LAST_ENDPOINT)
        

        
