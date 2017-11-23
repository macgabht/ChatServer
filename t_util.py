import socket, pdb, re, random, sys
from time import gmtime, strftime 


MAX_CLIENTS = 30
PORT = 22222
STUDENT_ID = 13325213
QUIT_STRING = '<$leave$>'
SERVER_IP = '134.226.44.155'


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
	

        #print(player.name + " says: " + msg)
	msg2 = msg.split()
        #print(msg2[0])
        if "JOIN_CHATROOM" in msg:
            same_room = False
            
            if len(msg.split()) >= 2: # error check
                
                room_name = msg.split()[1]
                SERVER_IP = msg.split()[3]
                PORT = msg.split()[5]
                name = msg.split()[7]                
                player.name = name 
                	 
               
                if player.name in self.room_player_map: # Case old person 
                    #if self.room_player_map[player.name] != room_name: #not in that room already
                    if not room_name in self.rooms: # not in rooms dictionary, NEW ROOM
                        new_room = Room(room_name) #object new room
                        self.rooms[room_name] = new_room #update in rooms {ROOM_1:room_name}
                        self.rooms[room_name].players.append(player) #add player to list of sockets in Room
                        self.room_refs.append(room_name) #add to list of sockets in room 
                        self.room_player_map[player.name] = room_name
                        ROOM_REF = self.room_refs.index(room_name)
                        
                    else:
                        self.rooms[room_name].players.append(player) #OLD PERSON, OLD ROOM
                        self.room_player_map[player.name] = room_name #assigns player.name to room_name,
                        
                       
                        
                else:
                     if not room_name in self.rooms: #new person new room
                        new_room = Room(room_name) #object new room, NEW PERSON
                        self.rooms[room_name] = new_room #update in rooms {ROOM_1:room_name}
                        self.rooms[room_name].players.append(player) #add player to list of sockets in Room
                        self.room_player_map[player.name] = room_name #assigns player.name to room_name
                        self.room_refs.append(room_name) #add room_name to room_refs list 
                        ROOM_REF = self.room_refs.index(room_name)
                        JOIN_ID = strftime("%Y%m%d%H%M%S", gmtime())
                        player.ID = JOIN_ID 
                        self.join_ids[JOIN_ID] = player.name #updates dict {JOIN_ID: player.name}    
                     else:     
                        self.rooms[room_name].players.append(player) #new person old room 
                        self.room_player_map[player.name] = room_name #assigns player.name to room_name,
                        JOIN_ID = strftime("%Y%m%d%H%M%S", gmtime())
                        player.ID = JOIN_ID 
                        self.join_ids[JOIN_ID] = player.name #updates dict {JOIN_ID: player.name}    
                    
		            
                msg = ('JOINED_CHATROOM: '+ str(room_name) +'\n'+ 'SERVER_IP: ' + '134.226.44.155\n'
                 + 'PORT: ' + str(PORT) + '\nROOM_REF: ' + str(self.room_refs.index(room_name)) +'\nJOIN_ID: ' + str(player.ID) + '\n')
                player.socket.sendall(msg)
                
                
                    
                data = (str(player.name) + ' has joined this chatroom')
                msg3 = ('CHAT: ' + str(self.room_refs.index(room_name)) + '\nCLIENT_NAME: ' + str(player.name) +'\nMESSAGE: ' + data + '\n\n')          
                #print self.rooms
                
                #for room in self.rooms:
                    #print self.rooms[room].name
                #print '\n'  
                #print 'room_name = ' + room_name
                #print 'self.rooms[room_name].name = ' + self.rooms[room_name].name + '\n\n'
                self.rooms[room_name].broadcast(player, msg3)  
           
                
        elif msg2[0] == 'CHAT:':
          
            ROOM_REF = msg2[1] #breaks the string up and stores in array
            JOIN_ID = msg2[3]
            name = msg2[5] 
            x = 7
            chat = ''
            while msg2[x] != len(msg2):
                chat = chat + str(msg2[x])
                x = x + 1
            print (chat)
            player.name = name           
            if JOIN_ID in self.join_ids:
                player.ID = JOIN_ID
                
                msg = "CHAT: " + str(ROOM_REF) + '\n' + "CLIENT_NAME: " + str(player.name) + "\nMESSAGE: " + str(chat) + '\n\n' 
          
                if ROOM_REF in self.room_refs: #checks room refs dict for room name
                    self.rooms[self.room_refs[ROOM_REF]].broadcast(player, msg)   #SHOULD GIVE US A ROOM_NAME WITH ROOM_REF
                    
        
        elif "DISCONNECT" in msg:            
            player.socket.shutdown(1)
            self.remove_player(player)
            
        elif "LEAVE_CHATROOM" in msg: #receives from server sends to remove function
            
            ROOM_REF = msg2[1]
            JOIN_ID = msg2[3]
            name = msg2[5]
                
            player.name = name
            player.ID = JOIN_ID
            
            msg3 = ('LEFT_CHATROOM: ' + str(ROOM_REF) + '\nJOIN_ID: ' + str(JOIN_ID) + '\n') 
            player.socket.sendall(msg3) 
            
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].remove_player(player, ROOM_REF) 
               
          

        elif "KILL_SERVICE\n" in msg:
            sys.exit(2)
    
        elif "print_map" in msg:
            print self.rooms
        

        elif 'HELO BASE_TEST\n' in msg:
            data = 'HELO text\nIP:'+ '134.226.44.155' +'\nPort:'+'22222'+'\nStudentID: '+str(STUDENT_ID)+'\n'
            player.socket.sendall(data)
              
        
            
    
    def remove_player(self, player, ROOM_REF): #server side 
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player, ROOM_REF) #calls remove_player in ROOM class
            del self.room_player_map[player.name]

    
class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
       # self.room_ref = room_ref
   

    #def welcome_new(self, from_player):
        #data = (str(player.name) + ' has joined this chatroom')
        #msg2 = ('CHAT: ' + str(self.room_refs.index(room_name)) + '\nCLIENT_NAME: ' + str(player.name) +'\nMESSAGE: ' + data +
        #for player in self.players:
            #player.socket.sendall(msg2)
    
    def broadcast(self, from_player, msg): #BROADCASTS MESSSAGES 
        for player in self.players:
            player.socket.sendall(msg)
            

    def remove_player(self, player, ROOM_REF): #sends to all clients in chatroom
        #print('leave2')
       
        left = (str(player.name) + ' has left this chatroom')
        leave_msg = ('CHAT: ' + str(ROOM_REF) + '\nCLIENT_NAME: ' + str(player.name) + '\nMESSAGE: ' + str(player.name) + ' has left this chatroom\n\n')
        self.broadcast(player, leave_msg) #client side 
        self.players.remove(player)

class Player:
    def __init__(self, socket, ID = '0', name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.ID = ID
		

    def fileno(self):
	    return self.socket.fileno()
