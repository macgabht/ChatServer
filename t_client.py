import sys, socket, select, pdb
from t_util import Hall, Room, Player
import t_util
import time, random

CLIENT_NAME = random.randint(1,50001)
CLIENT_IP = 0
PORT = 22222
RECV_BUFFER = 4096 #make preferably factor of 2

if len(sys.argv) < 2: #i.e [1] = localhost [2] = 5000
     print "Usage: Python3 client.py [hostname]" 
     sys.exit(1) #system error exit

else:
     server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     server_connection.connect((sys.argv[1], t_util.PORT))  #sys.argv[1] = host,

def prompt(): #called before each message is written by client
     print '>'

print "You are now to connected to the server\n"
msg_pref = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: # incoming message 
            msg = s.recv(RECV_BUFFER)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if  msg == t_util.QUIT_STRING:
                    sys.stdout.write(QUIT_STRING)
                    sys.exit(2)
                elif "LEFT_CHATROOM" in msg:
                    sys.stdout.write(msg)
                    
                elif "JOINED_CHATROOM" in msg:
                    ROOM_REF = msg.split()[7]
                    JOIN_ID = msg.split()[9]
                    sys.stdout.write(msg)
                    msg_prefix = ''
               
                else:
                    sys.stdout.write(msg)
                    msg_prefix = ''
                prompt()

        else:
            msg = msg_prefix + sys.stdin.readline()
            if "<join>" in msg:
                room_name = msg.split()[1]
                msg = ('JOIN_CHATROOM: '+ str(room_name) +'\n'+ 'CLIENT_IP: ' + str(CLIENT_IP)  + '\n'
                + 'PORT: ' + str(PORT) + '\n' +'CLIENT_NAME: ' + str(CLIENT_NAME)  + '\n')	
                server_connection.sendall(msg)
			
            elif '<leave>' in msg:
                msg = ('LEAVE_CHATROOM: ' + str(ROOM_REF) + '\n' + 'JOIN_ID: ' + str(JOIN_ID)
                + '\n' + 'CLIENT_NAME: ' + str(CLIENT_NAME) + '\n')
                server_connection.sendall(msg)
			
            elif '<disconnect>' in msg:
                msg = ('DISCONNECT: ' + str(CLIENT_IP) + '\n' + 'PORT: ' 
                + str(PORT) + '\n' + 'CLIENT_NAME: ' + str(CLIENT_NAME) + '\n')
                server_connection.sendall(msg)
            
            elif '<kill>'in msg:
                msg = 'KILL_SERVICE\n'
                server_connection.sendall(msg)

	    elif '<HELO>'in msg:
                msg = 'HELO text\n'
                server_connection.sendall(msg)

			
            else:
                data = 'CHAT: ' + str(ROOM_REF) + '\n' + 'CLIENT_NAME: ' + str(CLIENT_NAME) + '\n' + 'MESSAGE: ' + str(msg) + '\n' 
                server_connection.sendall(data)

		    
                
            

            
            


		
		
