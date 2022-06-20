import socket
from time import sleep

UDP_IP = "192.168.48.255"
UDP_PORT = 1860

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
if hasattr(socket,'SO_BROADCAST'):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = bytearray([255, 255])
sock.sendto(message, (UDP_IP, UDP_PORT))
