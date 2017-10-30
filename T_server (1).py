import select, socket, pdb, sys, re
from t_util import Hall, Room, Player
import t_util

RECV_BUFFER = 4096

host = sys.argv[1] if len (sys.argv) >=2 else ''
listen_sock = t_util.create_socket((host, t_util.PORT))

hall = Hall() #essentially a constructor for class "Block"
connection_list = [] #starts out empty connection list
connection_list.append(listen_sock) #updates connection list with with listen socket

while True:
	
	# get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
	#here we handle the new players/sockets, intially passed to the select function
	
	read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
       	if player is listen_sock: # compares returned readable sockets/players to the connection made to client(listen_sock)
		    new_socket, add = player.accept()
		    new_player = Player(new_socket) #this passes this new socket to the player class and updates
            connection_list.append(new_player) #update our connection list with each new player
			hall.welcome_new(new_player) #calls welcome function in Hall

		else: #new message incoming
		    msg = player.socket.recv(RECV_BUFFER)
		    if msg:
			    hall.process_msg(player, msg)
				
	        else:
				data = ("ERROR_CODE: [] \n' + 'ERROR_DESCRIPTION: Error in connection.' + '\n')
				player.socket.sendall(data)
			    player.socket.close()
			    connection_list.remove(player)

	for sock in error_sockets: #close alll error sockets returned by select.select
	    sock.close()
	    connection_list.remove(sock)


