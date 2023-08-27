import socket
import struct
UDP_IP = "192.168.1.202"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)

    unpacked = struct.unpack("!f", data)
    
    print("decoded message: %s" % unpacked)
    
    farenheit = unpacked[0] * (9/5) + 32
    
    print("converted  message: %s" % farenheit)
