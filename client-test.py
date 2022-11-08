import os, sys

program_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(program_path)

from checkmate.client import Client
from checkmate.common import Work
import time

class TestWork(Work):
    def __init__(self):
        self.i = 0
    
    def execute(self):
        print(self.i)
        self.i = self.i + 1
        time.sleep(0.5)

if __name__ == '__main__':
    client = Client('client.ini', program_path, __file__)
    client.append_work(TestWork())
    client.start()
    time.sleep(15)
    client.stop()
    