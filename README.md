# ChatServer
Internet Applications Project
Tiarnan MacGabhann
13325213

Utilities code is made up of Hall, Room and Player classes. 
Hall stores a number of lists and dictionaries. 
- 'rooms' is a dictionary that stores room_names as keys, that act as objects to the Room class
- 'key_room' map is a dictionary that stores a key unique to each room_name - player combination, and returns the corresponding room name
- 'room_refs' is just a list of room names. The ROOM_REF variable is assigned the value of the index of the room name it corresponds to in this list 
- join_ids is a dictionary with the JOIN_ID as the key that returns the corresponding player name
- clients is a list containing the player names as the join (the indices of the list are used to assign the JOIN_ID variables)

In the Hall class, the process_msg function is called when the server receives a message, taking the player instance and the msg as its parameters. It handles any possible strings that the client may send.
The first if statement handles the "JOIN_CHATROOM" message. Within this there are four permutations dealt with:
   a)A new player joins to create a new room: 
      a new_room instance of the Room class is created taking the room_name as its parameter
      The player socket passed in from the server is added to the players[] list in that room instance
      The various other lists are appended and the ROOM_REF and JOIN_ID are assigned
      The key assigned to each player/room combo in the dictionary is created by adding the players JOIN_ID with the ROOM_REF which should 
      give us a unique integer used later on. This key will be created every time a player joins another room
    b)A new player joins an existing room:  
    c)An existing player creates a new room:
    d) An existing player player joins an existing room.
    
   The response message to the client and relevant chatroom is sent to confirm joining. The relevant chatroom is accessed by using the        ROOM_REF to retrieve a room_name from the rooms:dictionary and using this object to create an instance using the broadcast function        from the Room class. This method of retrieving room_names from the relevant lists and dictionaries is used throughout to access Room      functions. 
   

Room class:

    takes single parameter name from server
    contains a list of sockets called player 
    contains broadcase and remove functions

Player class:

    takes socket, key and name as parameters
    
    
*******PROBLEMS ON TEST SERVER******
   -currently on 53% 
   -getting stuck on receiving messages from second client, somewhere in the parsing of the messages
   -Receiving and acknowledging the first client fine but second one getting ERROR: First string not of form 'CHAT::XXXXX'
   -feel like its a small thing but can't put my finger on it
   
   -
    
    
   
