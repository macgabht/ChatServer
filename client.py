#tiarnan mac gabhann 
#13325213
#Client
#
import struct
import binascii
from socket import *


def gremlin(myList = [], *args):
    for x in myList:
        l[0] = 'x'
        return

def crc16_ccitt(crc, data):
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
seqNum = 1
payloadL = 8

filename = 'alphabet.txt'
with open(filename, 'r') as f:
    while True:
        c = f.read(8)
        if not c:
            break
        l = list(c)
        checkSum = crc16_ccitt(0x1021, c)
        if seqNum < 3:
           gremlin(l)

        values = (seqNum, payloadL, l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7], checkSum)
        s = struct.Struct('I I 8c f')
        packed_data = s.pack(*values)
        print 'Original values:', values
        print 'Format string  :', s.format
        print 'Uses           :', s.size, 'bytes'
        print 'Packed Value   :', binascii.hexlify(packed_data)
        clientSocket.send(packed_data)
        if clientSocket.recv(2048) == "ack":
            print "acknowledgment received!"

        elif clientSocket.recv(2048) == "nak":
            print "acknowledgment not received!"

        seqNum = seqNum+1


clientSocket.close()
