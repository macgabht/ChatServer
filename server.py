#Tiarnan Mac Gabhann
#Server
#
import struct
import binascii
from socket import *


def crc16_ccitt(crc, data):
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print 'Server is ready to receive'
connectionSocket, addr = serverSocket.accept()
seqNum = 0
payloadL = 0
letters = None
checkSum = 0
 
while 1:

    recieved = connectionSocket.recv(1024)
    if recieved.strip() == "disconnect":
        connectionSocket.close()
        sys.exit("Received disconnect message.  Shutting down.")
        connectionSocket.send("nak")
    elif recieved:
        packed_data = str(recieved)
        s = struct.Struct('I I 8s f')
        unpacked_data = s.unpack(packed_data)
        letters = unpacked_data[2]
        checkSum1 = unpacked_data[3]
        seqNum = unpacked_data[0]
        checkSum2 = crc16_ccitt(0x1021, letters)
        if checkSum1 != checkSum2:
            print 'Error'
        print 'Unpacked Values:', unpacked_data
        connectionSocket.send("ack")

        file = open('outputFile.txt','w')
        file.write(letters)
        file.close()

