import os, sys

src_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
program_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(src_path)

from checkmate.client import Client

if __name__ == '__main__':
    client = Client('example/client/client.ini', program_path)
    client.run()
    