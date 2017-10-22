import socket, pdb

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'
KILL_STRING = 'KILL_SERVICE\n'

SERVER_IP = ''
ROOM_REF
JOIN ID


def create_socket(address): #called from the server, takes host, PORT as arguments in the form of one parameter address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address) #connects to the same host/address with .connect on client side
    s.listen(MAX_CLIENTS)
    print ("Server now listening at ", address)
    return s #returned to server

class Hall:
	def __init__(self):
		self.rooms = {} #dictionary {room_name: Room}
		self.room_player_map = {} #{playerName: roomName}

	def welcome_new(self, new_player): #called from server
		new_player.socket.sendall(b'Welcome\n' + instructions)
		

	def list_rooms(self, player):
        
       	     if len(self.rooms) == 0:
            	 msg = 'Oops, no active rooms currently. Create your own!\n' \
                     + 'Use [<join> room_name] to create a room.\n'
                 player.socket.sendall(msg)
       	     else:
            	 msg = 'Listing current rooms...\n'
                 for room in self.rooms:
                     msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
                 player.socket.sendall(msg)

	def handle_msg(self, player, msg): #RECEIVED THE REQUEST MESSAGE HERE
				
            request_response = b'JOINED_CHATROOM' + room_name + '\n' \
	    + b'SERVER_IP: [] \n' \
	    + b'PORT : [] \n'
            + b'ROOM_REF:' + room_ref + '\n'
	    + b'JOIN_ID': + join_id + '\n'
	    
		
            instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'["JOIN_CHATROOM" room_name] to join/create/switch to a room\n' \
            + b'[<guide>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'
	
		
		print(player.name + " says: " + msg)
		if "JOIN_CHATROOM" in msg:
                   same_room = False
                   if len(msg.split()) >= 2: # error check
                        room_name = msg.split()[1]
			player.name = msg.split()[7] #string will be provided by user client
			print "New Connection from:" player.name
			player.socket.sendall(request_response)	
			
			 if player.name in self.room_player_map: # switching?
                    	     if self.room_player_map[player.name] == room_name:
                                 player.socket.sendall(b'You are already in room: ' + room_name)
                                 same_room = True
                             else: # switch
                                 old_room = self.room_player_map[player.name]
                                 self.rooms[old_room].remove_player(player)
                         if not same_room:
                             if not room_name in self.rooms: # new room:
                                 new_room = Room(room_name) #similar to the function to create a new socket
                                 self.rooms[room_name] = new_room
                             self.rooms[room_name].players.append(player)
                             self.rooms[room_name].welcome_new(player) #call
                             self.room_player_map[player.name] = room_name
                    
		  else:
                       player.socket.sendall(instructions)

		
        `	elif "<list>" in msg:
           		self.list_rooms(player) 

        	elif "<manual>" in msg:
           	  player.socket.sendall(instructions)
        
       		elif "<quit>" in msg:
            		player.socket.sendall(QUIT_STRING)
            		self.remove_player(player)
		elif "KILL_SERVICE\n" in msg:
	   		player.socket.sendall(KILL_STRING)
	   		self.remove_player(player)  
	    
        	else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg)
            	  else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                player.socket.sendall(msg)
	
	def remove_player(self, player):
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].remove_player(player)
                del self.room_player_map[player.name]
            print "Player: " + player.name + " has left\n"
	

class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_player):
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(msg)
    
    def broadcast(self, from_player, msg):
        msg = from_player.name + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name + b"has left the room\n"
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
	return self.socket.fileno()




		 

`	




               
	

		