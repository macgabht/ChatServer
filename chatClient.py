from t_util import Hall, Room, Player
import t_util

CLIENT_IP = ''
PORT = ''
RECV_BUFFER = 4096 #make preferably factor of 2

if len(sys.argv) < 2: #i.e [1] = localhost [2] = 5000
     print "Usage: Python3 client.py [hostname]" 
     sys.exit(1) #system error exit

else:
     server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     server_connection.connect((sys.argv[1], pychat_util.PORT))  #sys.argv[1] = host,

def prompt(): #called before each message is written by client
     print '>'

print "You are now to connected to the server\n"
msg_pref = ''

socket_list = [sys.stdin, server_connection]

while True:
	read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
	for s in read_sockets: 
		if s is server_connection: #message is being received
			msg = s.recv(RECV_BUFFER) #assign datat received by buffer to msg	
			if not msg: #nothing received?
				print "Something went wrong, server is down!"
				sys.exit(2)
			else:
			    sys.stdout.write(msg) #receives message from server and prints it  to the screen, "Welcome""
			    if 'Welcome" in msg:
			    	msg_pref = ''
			    else:
				msg_pref = '' #ordinary messages
			    prompt()
		else:
		msg = msg_pref + sys.stdin.readline() #JOIN_CHATROOM .....
		server_connection.sendall(msg)
		
