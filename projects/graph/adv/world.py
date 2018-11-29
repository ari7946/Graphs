from room import Room
from item import Item
import random

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class World:
    def __init__(self):
        self.startingRoom = None
        self.rooms = {}
        self.occupied = set()

    def getRandomDirection(self, room, coords):
        """
        Select a random direction from all valid connections.
        This checks if the connection is unnoccupied and if the
        adjacent grid is also unoccupied.
        """
        dirs = []
        if self._checkCoordinates(coords, "n"):
            dirs.append("n")
        if self._checkCoordinates(coords, "s"):
            dirs.append("s")
        if self._checkCoordinates(coords, "w"):
            dirs.append("w")
        if self._checkCoordinates(coords, "e"):
            dirs.append("e")
        random.shuffle(dirs)
        if len(dirs) > 0:
            return dirs[0]
        else:
            return None

    def _updateCoordinates(self, coords, direction):
        """
        Increment xy coordinates in one direction
        """
        new_coords = list(coords)
        if direction == "n":
            new_coords[1] += 1
        if direction == "s":
            new_coords[1] -= 1
        if direction == "e":
            new_coords[0] += 1
        if direction == "w":
            new_coords[0] -= 1
        return new_coords

    def _checkCoordinates(self, coords, direction):
        """
        Check if the grid in an adjoining direction is unoccupied
        """
        return str(self._updateCoordinates(coords, direction)) not in self.occupied

    ####
    # MODIFY THIS CODE
    ####
    def generateRooms(self, numRooms):
        """
        Generate a random graph of rooms
        """
        self.rooms = {}

        if numRooms < 1:
            print("Must create at least 1 room")
            return None

        # The coordinates of our room. We start from (0,0)
        xy = [0,0]

        # Keep track of which grid spots are occupied
        self.occupied = set()

        # Create a set that will hold the IDs of rooms with valid connections available
        validRooms = set()

        # Create n rooms
        for i in range(0, numRooms):
            # Create a room
            new_room = Room(f"Room {i}", "You are standing in an empty room.")
            self.rooms[i] = new_room
            if i == 0:
                # Our first room is always valid
                validRooms.add(i)
                self.occupied.add(str(xy))
            else:
                # If it's not the first room....
                # ...connect to the previous room in a random direction
                random_dir = None

                # In case we run into a room with no valid connections, keep looping
                # until we find a room with valid connections.
                # Note that there will ALWAYS be a valid room available
                while random_dir is None:
                    # Get a room that we think is valid
                    connectingRoom = validRooms.pop()
                    # Get the coordinates of that room
                    xy = self.rooms[connectingRoom].xy
                    # See if we can get a random direction from that room
                    random_dir = self.getRandomDirection(self.rooms[connectingRoom], xy)
                    # If our room is valid (i.e. not None) then we put it back in our
                    # set of valid rooms.
                    if random_dir is not None:
                        validRooms.add(connectingRoom)
                    # If it's NOT valid, then we don't put it back into validRooms
                    # and we try again with a different room.

                # We have a valid direction, so update the room and make the connection
                xy = self._updateCoordinates(xy, random_dir)
                self.rooms[connectingRoom].connectRooms(random_dir, new_room)
                self.occupied.add(str(xy))
                new_room.xy = xy
                validRooms.add(i)
                if i == numRooms - 1:
                    new_room.addItem(Item("Treasure", "This is treasure"))

        # Set the starting room to the first room. Change this if you want a new starting room.
        self.startingRoom = self.rooms[0]

        if len(self.occupied) == numRooms:
            print("World successfully created!")
        else:
            print("Something is wrong....")

        return self.rooms
    def findTreasure(self, startRoom):
        q = Queue()
        visited = set()
        q.enqueue(([], startRoom))
        while q.size() > 0:
            path_and_room = q.dequeue()
            room = path_and_room[1]
            if room not in visited:
                if len(room.items) > 0:
                    for item in room.items:
                        if item.name == "Treasure":
                            return path_and_room[0]
                visited.add(room)
                if room.n_to is not None:
                    new_path = list(path_and_room[0])
                    new_path.append("n")
                    q.enqueue((new_path, room.n_to))
                if room.s_to is not None:
                    new_path = list(path_and_room[0])
                    new_path.append("s")
                    q.enqueue((new_path, room.s_to))
                if room.e_to is not None:
                    new_path = list(path_and_room[0])
                    new_path.append("e")
                    q.enqueue((new_path, room.e_to))
                if room.w_to is not None:
                    new_path = list(path_and_room[0])
                    new_path.append("w")
                    q.enqueue((new_path, room.w_to))
        return None