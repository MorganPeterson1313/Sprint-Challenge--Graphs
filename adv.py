from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

traversal_path = []


graph = {}

class Queue:
    def __init__(self):
        self.storage = []

    def enqueue(self, item):
        self.storage.append(item)

    def dequeue(self):
        return self.storage.pop(0)

    def size(self):
        return len(self.storage)

def get_inverse_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    elif direction == "e":
        return "w"


def bft_rooms(graph, starting_room):
    """
    Print each vertex in breadth-first order
    beginning from starting_vertex.
    """
    q = Queue()
    
    # Create an empty Visited dict
    visited = set()  # Note that this is a dictionary, not a set
    
    # Add A PATH TO the starting vertex to the queue
    pathToTraverse = []
    q.enqueue([starting_room])
    
    # While the queue is not empty...
    while q.size() > 0:
        
        # Dequeue the first PATH
        path = q.dequeue()
        # Grab the last vertex of the path
        current_room = path[-1]
        # Check if it's our destination

        # If it has not been visited...
        if current_room not in visited:
            
            visited.add(current_room)
           
           # If we reach a room in our graph of searched rooms
           # That contains a "?", return the shortest path
           # THat leads to that room
            for room in graph[current_room]:
                if graph[current_room][room] == "?":
                    return path
                    

            # From current position, search the current
            # graph for the nearest room with a "?"
            # add each step to the path list so it can 
            # be used to traverse to the room
            for room_exit in graph[current_room]:

                pathToTraverse.append(room_exit)
                next_room = graph[current_room][room_exit]
                path_copy = path.copy()
                path_copy.append(next_room)
                q.enqueue(path_copy)

    




while len(graph) < len(room_graph):
    
    currentRoomID = player.current_room.id
    
    # If the current room hasn't been visited yet
    # add it to the visited set and add to the graph
    if currentRoomID not in graph:
        graph[currentRoomID] = {}
        
        # Mark each path with a "?" to keep track of the 
        # rooms that haven't been searched
        for exit in player.current_room.get_exits():
            graph[currentRoomID][exit] = "?"
 
    # traverse through the room graph from the starting point,
    # creating a graph/map of each room we encounter
    for path in graph[currentRoomID]:

        # If there is no valid path in the current room
        # We've hit a dead end and need to bfs for the nearest
        # room with an unsearched path
        if path not in graph[currentRoomID]:
            break

        # If a path has a "?"
        # Enter the room and add the new room and all
        # of it's paths to the graph with "?"
        if graph[currentRoomID][path] == "?":
            exit_path = path

            # enter the room with a "?"
            # Add this new room to the graph if it
            # hasn't been visited before
            if exit_path is not None:
                traversal_path.append(exit_path)
                player.travel(exit_path)
                new_roomID = player.current_room.id

                if new_roomID not in graph:
                    graph[new_roomID] = {}

                    for exit in player.current_room.get_exits():
                        graph[player.current_room.id][exit] = "?"

            # Mark the current path and the new room's inverse path
            # With the correct room numbers
            # Set the current room number ID to the new room number ID
            graph[currentRoomID][exit_path] = new_roomID
            graph[new_roomID][get_inverse_direction(
                exit_path)] = currentRoomID
            currentRoomID = new_roomID
            print(graph)
            

    # After we've hit a dead end,
    # Search for the nearest room with a "?" in the graph
    # and return the path of directions to get there
    paths = bft_rooms(graph, currentRoomID)

    # If there's a path returned from bfs
    # use those directions to traverse to the room
    # with an unsearched "?", enter that room and continue searching
    if paths is not None:
        for room_number in paths:
            for room in graph[currentRoomID]:
                if graph[currentRoomID][room] == room_number:
                    traversal_path.append(room)
                    player.travel(room)
    currentRoomID = player.current_room.id
    

    # Choose random unexplored direction
    # Go there
    # Update this room and the previous room
    # if the new room isn't in the graph, add it

    ## bfs
    # search for an unexplored room (using graph, not room_graph)
    # then it will return the shortest path to the question mark
    # then get the directions, and player walks it



#def find_traversal_path(world,player):

# import random
# # def randomDirection(stringLength=1):
#         # letters = ["n", "s", "w", "e"]
#         # for i in range(stringLength):
#         #     return random.choice(letters)

# directions = ["n", "s", "w", "e"]


# array = []
# visited = {}
# route= random.choice(directions)
# # room_id = player.current_room.id
# # this_way = player.current_room.get_room_in_direction(route)
# # furthest_room = dft(room_id)

# # visited.update({f"{player.current_room.id}":f"{route}"})

# for i in range(len(room_graph)):
    
#     route= random.choice(directions)
#     room_id = player.current_room.id
#     this_way = player.current_room.get_room_in_direction(route)
#     furthest_room = dft(room_id)
    
#     player.travel(route)
#     #we_are_here = world.starting_room
#     print(f"current room id: {player.current_room.id}")
    

#     print(f"player current room: {player.current_room}")
#     #= world.starting_room
#     #print(f"current room: {we_are_here}")
#     #print(random.choice(directions))
#     room_exits = player.current_room.get_exits()
#     print(f"room e: {room_exits}") 
#     print(f"direction : {route}")
#     player.travel(route)
#     print(f"direction 2 : {route}")
#     room_pair = {f"{player.current_room.id}": f"{route}"}
#     #visited.update({f"{player.current_room.id}": f"{route}"})
#     if room_pair not in visited.values():
#         visited.setdefault({f"{player.current_room.id}", f"{route}"})
        
#         last_visited = visited.copy()
#         print(f"visited 1 : {visited}")
#         #print(f" where player has been: {array}")
#         if room_exits == None:
#             last_room_visited = last_visited.popitem()
#             array.append(last_room_visited)
#             print(f"last room visited : {last_room_visited}")
#             #array.append(last_room_visited)
#             back_track = bfs(last_room_visited , room_id)
#             player.travel(route)
#             print()

#             print(f"visited 2 : {visited}")
#         for room in room_exits:
#             room_pair = f"{player.current_room.id}: {route}"
#             visited.update({f"{player.current_room.id}": f"{route}"})
#             if len(room_exits) == 1 and room_pair not in visited.values():
            
#                 player.travel(route)
#                     #visited.update({f"{player.current_room.id}":f"{route}"})
#                 #visited.setdefault(f"{player.current_room.id}", f"{route}")
#                 this_way = player.current_room.get_room_in_direction(room)
#                     # #just added this in order to back track from the furthest room
#                     # back_track = bfs(last_room_visited , room_id)
#                 player.travel(route)
#                 # visited.update({f"{player.current_room.id}": {f"{player.current_room.id}":f"{route}"}})
#                 print(f"visited 3: {visited}")
#                 print(f"this way: {this_way}")
#                 back_track = bfs(last_room_visited , room_id)
#                 furthest_room =  dft(room_id)
#                 # go back to the room you started in after you are shown the way
#                 if len(room_exits) >= 1:

#                     #back_track = bfs(last_room_visited , room_id)
#                     furthest_room = dft(room_id)
#                     back_track = bfs(last_room_visited , room_id)
#                     player.travel(route)
#         # if player.current_room.id == "?":
                
#             if player.travel(route) == None:
                
#                 visited.update({f"{player.current_room.id}": f"{route}"})
#                 print(f"visited 4: {visited}")   
#                 last_visited = visited.copy()
#                 array.append(last_visited)           
#                 #furthest_room = dft(room_id, this_way)
#                     #just added this in order to back track from the furthest room
#                 last_room_visited = last_visited.popitem()
#                 back_track = bfs(last_room_visited , room_id)
#                 #what is the current way out
#                 this_way = player.current_room.get_room_in_direction(room)
#                 #furthest_room = dft(room)
#                 array.append(last_room_visited)    
#             else:
#                 if room_exits == route:
#                             #this_way = player.current_room.get_room_in_direction(way)
                            
#                     print(f"last room : {last_room_visited}")  
#                     array.append(last_room_visited)
#                     back_track = bfs(last_room_visited , room_id)
#                     for room , route in visited.items():
#                         if room and route not in visited:
#                             #visited.update({"room":"route"})
#                             print(f"visited 5 : {visited}")
#                             furthest_room = dft(way)
#                             back_track = bfs(last_room_visited , room_id)
#                             connected_rooms = player.current_room.connect_rooms(this_way,room_id)
                        
                        
#                         # for room in back_track:
#                         #     if room == 
#                 # if player.travel(directions[i]) != "?":
# for room, route in visited.items():
#     path = route
#     #if path != None: 
    
#     traversal_path.append(path)
                
# print(f"traversal : {traversal_path}")  
# print(f"array : {array}")   

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
