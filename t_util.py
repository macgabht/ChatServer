import socket, pdb, re, random, sys

ROOM_REF = random.randint(1,50001)
JOIN_ID = random.randint(1, 50001)
SERVER_IP = '134.226.44.169'
MAX_CLIENTS = 30
PORT = 22222
STUDENT_ID = 13325213
QUIT_STRING = '<$leave$>'


instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join>] to join/create/switch to a room\n' \
            + b'[<guide>] to show instructions\n' \
            + b'[<leave>] to leave your chatroom\n' \
			+ b'[<disconnect>] to disconnect from the service\n' \
            + b'[<kill>] to terminate the service\n' \
            + b'[<HELO>] to send a test hello string\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print('Chat server started on port :', str(PORT))
    return s

class Hall:
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}

    def welcome_new(self, new_player):
        new_player.socket.sendall(b'Welcome to T-Chat, here are your instructions' +'\n' + instructions)

    def list_rooms(self, player):
        
        if len(self.rooms) == 0:
            msg = 'Theyre are no rooms active at the moment. Create your own.\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.socket.sendall(msg)
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(msg)
    
    def process_msg(self, player, msg):
	

        print(player.name + " says: " + msg)
	
        if "JOIN_CHATROOM" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                name = msg.split()[7]
                player.name = name #updates in the player class
		
                print "New connection from:" + str(player.name) + '\n'
		
                msg = ('JOINED_CHATROOM: '+ str(room_name) +'\n'+ 'SERVER_IP: ' + str(SERVER_IP) + '\n'
                   + 'PORT: ' + str(PORT) + '\n' + 'ROOM_REF: ' + str(ROOM_REF) +'\n' +'JOIN_ID: ' + str(JOIN_ID) + '\n')
                player.socket.sendall(msg)
		
		
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are already in room: ' + room_name)
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(instructions)

        elif "<list>" in msg:
            self.list_rooms(player) 

        elif "<guide>" in msg:
            player.socket.sendall(instructions)
		
        elif "DISCONNECT" in msg:            
            player.socket.shutdown(1)
            self.remove_player(player)
            
        elif "LEAVE_CHATROOM" in msg: #receives from server sends to remove function
            data = "LEFT_CHATROOM: " +str(ROOM_REF) + '\n' + "JOIN_ID: " + str(ROOM_REF) + '\n'
            player.socket.sendall(data)
            self.remove_player(player) 
        
        elif "KILL_SERVICE" in msg:
            sys.exit(2)

        elif 'HELO text\n' in msg:
            data = 'HELO text\nIP:'+str(SERVER_IP)+'\n'+'Port:'+str(PORT)+'\n'+'StudentID: '+str(STUDENT_ID)+'\n'
            player.socket.sendall(data)

            
            
        else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg)
            else:
                msg = 'You are currently not in any room. \n' \
                    + 'Use [<list>] to see available rooms. \n' \
                    + 'Use [<join> room_name] to join a room. \n'
                player.socket.sendall(msg)
    
    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print "User: " + player.name + " has left\n"

    
class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_player):
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(msg)
    
    def broadcast(self, from_player, msg): #BROADCASTS MESSSAGES 
        #msg = from_player.name + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = ('LEFT_CHATROOM: ' + str(ROOM_REF) + '\n' + 'JOIN_ID: ' + str(JOIN_ID) + '\n')
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
		

    def fileno(self):
		return self.socket.fileno()
