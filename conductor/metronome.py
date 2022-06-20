import socket
from time import sleep

UDP_IP = "192.168.48.255"
UDP_PORT = 1860

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
if hasattr(socket,'SO_BROADCAST'):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
for h in range(0, 255):
	for l in range(0, 255):
		message = bytearray([l, h])
		# message = "%d/%d\n" % (l,h)
		sock.sendto(message, (UDP_IP, UDP_PORT))
		sleep(0.02)
