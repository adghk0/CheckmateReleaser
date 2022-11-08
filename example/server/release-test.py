import os, sys

src_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(src_path)

from checkmate.server import Server

if __name__ == '__main__':
    s = Server('example/server/server.ini')
    s.release(os.path.abspath('C:\\Data\\Develop\\checkmate_test'), '0.0.2', 'client test')