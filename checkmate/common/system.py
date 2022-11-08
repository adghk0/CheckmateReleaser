import socket
import platform
import sys

def host_name():
    return socket.gethostname()

def inner_ip():
    return socket.gethostbyname(socket.gethostname())

def outer_ip():
    return socket.gethostbyname(socket.getfqdn())

def os():
    return platform.uname().system + ' ' + platform.uname().release

def python_version():
    return sys.version.split(' ', 2)[0]
