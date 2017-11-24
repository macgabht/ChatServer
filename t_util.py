import socket, pdb, re, random, sys
from time import gmtime, strftime 


MAX_CLIENTS = 30
PORT = 22222
STUDENT_ID = 13325213
SERVER_IP = '134.226.44.149'

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
        self.room_player_map = {} # {special_key: roomName}
        self.room_refs = [] #{ROOM_REF: room_name}
        self.join_ids = {} #{JOIN_ID: player.name}
        self.clients = [] #list of names
        

    def process_msg(self, player, msg):
        
	msg2 = msg.split()
        
        if "JOIN_CHATROOM" in msg:
                
                room_name = msg.split()[1]
                SERVER_IP = msg.split()[3]
                PORT = msg.split()[5]
                name = msg.split()[7]                
                player.name = name 
            
    
                	 
                if player.name in self.clients: # Case old person, already in client list 
                    if not room_name in self.rooms: # not in rooms dictionary, NEW ROOM
                        new_room = Room(room_name) #object new room
                        self.rooms[room_name] = new_room #update in rooms {ROOM_1:room_name}
                        self.rooms[room_name].players.append(player) #add player to list of sockets in Room
                        self.room_refs.append(room_name)  
                        self.room_player_map[player.key] = room_name
                        ROOM_REF = self.room_refs.index(room_name)

                       
                    else:
                        self.rooms[room_name].players.append(player) #OLD PERSON, OLD ROOM
                        self.room_player_map[player.key] = room_name #assigns player.name to room_name,
                        
                        
                else: #player.name not in client list, needs a join_id 

                     if not room_name in self.rooms: #new person creating a new room

                        new_room = Room(room_name) #object new room, NEW PERSON
                        self.rooms[room_name] = new_room #update in rooms {ROOM_1:room_name}
                        self.rooms[room_name].players.append(player) #add player to list of sockets in Room
                        self.room_refs.append(room_name) #add room_name to room_refs list 
                        ROOM_REF = self.room_refs.index(room_name) #ASSIGN ROOM_REF 
                        self.clients.append(player.name)
                        JOIN_ID = self.clients.index(player.name)#ASSIGN JOIN_ID
                        self.join_ids[JOIN_ID] = player.name
                        tmp = self.room_refs.index(room_name) 
                        player.key = JOIN_ID + tmp
                        self.room_player_map[player.key] = room_name #assigns player.name to room_name
                        
                     else:
                        self.clients.append(player.name)
                        self.rooms[room_name].players.append(player) #new person old room, need a special key
                        JOIN_ID = self.clients.index(player.name)#ASSIGN JOIN_ID
                        self.join_ids[JOIN_ID] = player.name
                        tmp = self.room_refs.index(room_name) 
                        player.key = JOIN_ID + tmp
                        self.room_player_map[player.key] = room_name #assigns player.name to room_name
                        
                    
		            
                msg = ('JOINED_CHATROOM: '+ str(room_name) +'\n'+ 'SERVER_IP: ' + '134.226.44.149\n'
                 + 'PORT: ' + str(PORT) + '\nROOM_REF: ' + str(self.room_refs.index(room_name)) +'\nJOIN_ID: ' + str(self.clients.index(player.name)) + '\n')
                player.socket.sendall(msg)
                
                    
                data = (str(player.name) + ' has joined this chatroom')
                msg3 = ('CHAT: ' + str(self.room_refs.index(room_name)) + '\nCLIENT_NAME: ' + str(player.name) +'\nMESSAGE: ' + data + '\n\n')          
                
                self.rooms[room_name].broadcast(player, msg3)  
           
                
        elif msg2[0] == 'CHAT:':
          
            room_ref = msg2[1] #breaks the string up and stores in array
            ROOM_REF = int(room_ref)
            join_id = msg2[3]
            JOIN_ID = int(join_id)
            name = msg2[5] 
            player.name = name 
            words = msg.split("MESSAGE:", 1)[1]
            #print msg2
            #x = 7
            #chat = ''
            #while msg2[x] != len(msg2):
                #chat = chat + str(msg2[x])
                #x = x + 1
           
            print self.join_ids             
            msg = ("CHAT: " + str(ROOM_REF) + '\n' + "CLIENT_NAME: " + str(player.name) + "\nMESSAGE: " + str(words) + '\n\n') 
            self.rooms[self.room_refs[ROOM_REF]].broadcast(player, msg)   #SHOULD GIVE US A ROOM_NAME WITH ROOM_REF its index
                    
        
        elif "DISCONNECT" in msg:            
            player.socket.shutdown(1)
            #self.remove_player(player)
            
        elif msg2[0] == 'LEAVE_CHATROOM:': #receives from server sends to remove function
            
            room_ref = msg2[1]
            ROOM_REF = int(room_ref)
            join_id = msg2[3]
            JOIN_ID = int(join_id)
            name = msg2[5]
            player.name = name
            player.key = ROOM_REF + JOIN_ID             

            msg3 = ('LEFT_CHATROOM: ' + str(ROOM_REF) + '\nJOIN_ID: ' + str(JOIN_ID) + '\n') 
            player.socket.sendall(msg3) 
            
            leave_msg = ('CHAT: ' + str(ROOM_REF) + '\nCLIENT_NAME: ' + str(player.name) + '\nMESSAGE: ' + str(player.name) + ' has left this chatroom\n\n')

           
            self.rooms[self.room_refs[ROOM_REF]].broadcast(player, leave_msg)
            self.rooms[self.room_refs[ROOM_REF]].remove_player(player, ROOM_REF) #pass room_refs[room_ref] = room_name=
           
            if player.key in self.room_player_map:
                #print self.room_player_map
                del self.room_player_map[player.key] 
                #print self.room_player_map

        elif "KILL_SERVICE\n" in msg:
            sys.exit(2)
    
        elif "print_map" in msg:
            print self.rooms
        

        elif 'HELO BASE_TEST\n' in msg:
            data = 'HELO text\nIP:'+ '134.226.44.149' +'\nPort:'+'22222'+'\nStudentID: '+str(STUDENT_ID)+'\n'
            player.socket.sendall(data)
                 

    
class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
       
    
    def broadcast(self, from_player, msg): #BROADCASTS MESSSAGES 
        for player in self.players:
            player.socket.sendall(msg)
            

    def remove_player(self, player, ROOM_REF): #sends to all clients in chatroom
       
        self.players.remove(player)

class Player:
    def __init__(self, socket, key = '', name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name 
        self.key = key
		

    def fileno(self):
        return self.socket.fileno()
