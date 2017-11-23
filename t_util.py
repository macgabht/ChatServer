import socket, pdb, re, random, sys

JOIN_ID = 0
MAX_CLIENTS = 30
PORT = 22222
STUDENT_ID = 13325213
QUIT_STRING = '<$leave$>'
SERVER_IP = '134.226.44.143'


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
        self.room_refs = [] #{ROOM_REF: room_name}
        self.join_ids = {} #{JOIN_ID: player.name}
     

    def process_msg(self, player, msg):
	

        print(player.name + " says: " + msg)
	
        if "JOIN_CHATROOM" in msg:
            same_room = False
            
            if len(msg.split()) >= 2: # error check
                
                room_name = msg.split()[1]
                SERVER_IP = msg.split()[3]
                PORT = msg.split()[5]
                name = msg.split()[7]                
                player.name = name 
                	 
               
                if player.name in self.room_player_map: # Case for player already in one room joining another
                            if self.room_player_map[player.name] == room_name:
                                player.socket.sendall(b'you are already in room: ' + str(room_name))
                                same_room = True
                        
                if not same_room:
                    if not room_name in self.rooms: # not in rooms dictionary
                        new_room = Room(room_name) #object new room
                        self.rooms[room_name] = new_room #update in rooms {ROOM_1:room_name}
                        self.room_refs.append(room_name) #add room_name to room_refs list 
                        ROOM_REF = self.room_refs.index(room_name)
                          
                    #otherwise room_name in dict self.rooms, new person                          
                    self.rooms[room_name].players.append(player) #add player to list of sockets in Room
                    self.room_player_map[player.name] = room_name #assigns player.name to room_name,

                    JOIN_ID = random.randint(1, 50001)
                    player.ID = JOIN_ID 
                    self.join_ids[JOIN_ID] = player.name #updates dict {JOIN_ID: player.name}    
		            
                    msg = ('JOINED_CHATROOM: '+ str(room_name) +'\n'+ 'SERVER_IP: ' + '134.226.44.143' + '\n'
                    + 'PORT: ' + str(PORT) + '\n' + 'ROOM_REF: ' + str(ROOM_REF) +'\n' +'JOIN_ID: ' + str(player.ID) + '\n')
                    player.socket.sendall(msg)
                    
                    #self.rooms[room_name].welcome_new(player) #send welcome message

            #else:
             #   player.socket.sendall(instructions)
                
        elif "CHAT" in msg:
            ROOM_REF = msg.split()[1]
            JOIN_ID = msg.split()[3]
            name = msg.split()[5]
            data = msg.split(':')
            chat = data[4]
            #chat = msg.split()[7] 
            player.name = name           
            if JOIN_ID in self.join_ids:
                player.ID = JOIN_ID
                
                msg = "CHAT: " + str(ROOM_REF) + '\n' + "CLIENT_NAME: " + str(player.name) + "MESSAGE: " + str(chat) + '\n\n' 
          
                if ROOM_REF in self.room_refs: #checks room refs dict for room name
                    self.rooms[self.room_refs[ROOM_REF]].broadcast(player, msg)   #SHOULD GIVE US A ROOM_NAME WITH ROOM_REF
                    
        
        elif "DISCONNECT" in msg:            
            player.socket.shutdown(1)
            self.remove_player(player)
            
        elif "LEAVE_CHATROOM" in msg: #receives from server sends to remove function
            
            ROOM_REF = msg.split()[1]
            JOIN_ID = msg.split()[3]
            name = msg.split()[5]
                
            player.name = name
            player.ID = JOIN_ID
            
            if ROOM_REF in self.room_refs:
                 old_room = self.room_player_map[player.name] #removes from the dict with corresponding room attached
                 self.rooms[old_room].remove_player(player, ROOM_REF)   
          

        elif "KILL_SERVICE\n" in msg:
            sys.exit(2)
    
        elif "print_map" in msg:
            print self.rooms
        

        elif 'HELO BASE_TEST\n' in msg:
            data = 'HELO text\nIP:'+'134.226.44.143'+'\n'+'Port:'+'22222'+'\n'+'StudentID: '+str(STUDENT_ID)+'\n'
            player.socket.sendall(data)
              
        else:
             #check if in a room (or not) first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg)
            
    
    def remove_player(self, player, ROOM_REF): #server side 
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player, ROOM_REF) #calls remove_player in ROOM class
            del self.room_player_map[player.name]
        print "User: " + player.name + " has left\n" #server side 

    
class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
   

    #def welcome_new(self, from_player):
        #msg = self.name + " welcomes: " + from_player.name + '\n'
        #for player in self.players:
            #player.socket.sendall(msg)
    
    def broadcast(self, from_player, msg): #BROADCASTS MESSSAGES 
       #msg = from_player.name + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)
            print (msg)

    def remove_player(self, player, ROOM_REF): #sends to all clients in chatroom
        self.players.remove(player)
        leave_msg = ('LEFT_CHATROOM: ' + str(ROOM_REF) + '\n' + 'JOIN_ID: ' + str(player.ID) + '\n')
        self.broadcast(player, leave_msg) #client side 

class Player:
    def __init__(self, socket, ID = '0', name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.ID = ID
		

    def fileno(self):
	    return self.socket.fileno()
