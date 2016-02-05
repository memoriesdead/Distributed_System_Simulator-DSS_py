from functions import *
import multiprocessing
import time

with open("config.txt") as f:
    lines = f.readlines()
max_instances =  int(lines[0].split(' ')[1])


class machine():
    'Class for the instance of a machine'
    
    q = [multiprocessing.Queue() for i in range(max_instances + 1)]
    # q[0] is unused
    count = multiprocessing.Value('i', 1)

    def __init__(self):
        self.mac_id = machine.count.value
        machine.count.value += 1

    def execute_func(self, func_name, *args):
        comm_str = str(func_name) + ' = multiprocessing.Process(name = "' + str(func_name) + '", target = ' + str(func_name) + ', args = ('
        comm_str += 'self,'
        for arg in args:
            if(type(arg) is str):
                comm_str += '"' + str(arg) + '",'
            else:
                comm_str += str(arg) + ','
        comm_str += '))'

        # create the new process
        exec(comm_str)

        # start the new process
        comm_str = str(func_name) + '.start()'
        exec(comm_str)
        

    def send(self, destination_id, message):
        # send message to the machine with machine_id destination_id

        mac_id = int(destination_id[8:])
        if(mac_id >= machine.count.value or mac_id <= 0):
            return -1

        # message is of the format "hello|2". Meaning message is "hello" from machine with id 2
        # However, the message received is processed and then returned back to the user
        message += '|' + str(self.get_id())

        machine.q[mac_id].put(message)
        return 1

    def recv(self):
        mac_id = self.get_id()
        if(mac_id >= machine.count.value or mac_id <= 0):
            return -1, -1

        message =  machine.q[mac_id].get().split('|')

        # message received is returned with the format "hello" message from "machine_2"
        return message[0], 'machine_' + message[1]

    def get_id(self):
        return self.mac_id

    def get_machine_id(self):
        return "machine_" + str(self.get_id()) 
