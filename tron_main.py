import math
import sys
# from queue import Queue

# constants
GRID_SIZE_X = 30
GRID_SIZE_Y = 20


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Item:
    def __init__(self, owner):
        self._owner = owner
        self._dist = [math.inf] * 4

    def get_owner(self):
        return self._owner

    # gets the distance of a player
    def get_distance(self, player):
        return self._dist[player]

    # set the distance of a player
    def set_distance(self, player, distance):
        self._dist[player] = distance


class Grid:
    # contains the current positions of the players
    # TODO: needs to be set every round
    x_cur = [-1] * 4
    y_cur = [-1] * 4

    def __init__(self):
        self._data = [[Item(9)] * GRID_SIZE_Y for i in range(GRID_SIZE_X)]
        print('LenX: ' + str(len(self._data)) + ' LenY: ' + str(len(self._data[0])), file=sys.stderr, flush=True)

    def set_data(self, x, y, owner):
        # print('Set Data ' + str(x) + ' ' + str(y), file=sys.stderr, flush=True)
        self._data[x][y] = Item(owner)

    def get_item(self, x, y, debug=False):
        if debug:
            print('X: ' + str(x) + 'Y: ' + str(y), file=sys.stderr, flush=True)

        if 0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y:
            return self._data[x][y]
        else:
            return Item(-1)

    def print_grid_owner(self):
        for y in range(len(self._data[0])):
            for x in range(len(self._data)):
                print(self.get_item(x, y).get_owner(), file=sys.stderr, flush=True, end=' ')
            print('', file=sys.stderr, flush=True)

    def print_grid_dist(self, player):
        print('Distance for player: ' + str(player), file=sys.stderr, flush=True)
        for y in range(len(self._data[0])):
            for x in range(len(self._data)):
                print(self.get_item(x, y).get_distance(player), file=sys.stderr, flush=True, end=' ')
            print('', file=sys.stderr, flush=True)

    def reset_grid_distance(self):
        for y in range(len(self._data[0])):
            for x in range(len(self._data)):
                self.get_item(x, y).set_distance(0, math.inf)
                self.get_item(x, y).set_distance(1, math.inf)
                self.get_item(x, y).set_distance(2, math.inf)
                self.get_item(x, y).set_distance(3, math.inf)

    # calculates the distance for each player to each grid pos
    def calc_shortest_path_for_grid(self):
        for player in range(number_players + 1):
            # fake to start with 0
            player = player - 1
            # set's the distance of the starting point
            self.get_item(self.x_cur[player], self.y_cur[player]).set_distance(player, 0)
            knot_queue = Queue()
            knot_queue.put([self.x_cur[player], self.y_cur[player]])

            while not knot_queue.empty():
                print('Size but not sure: ' + str(knot_queue.qsize()), file=sys.stderr, flush=True)
                x_item, y_item = knot_queue.get()
                # no for loop cause every time only 4 possible ways
                # left x-1
                x_item_new = x_item - 1
                y_item_new = y_item
                if self.get_item(x_item_new, y_item_new).get_owner() == 9:
                    if self.get_item(x_item_new, y_item_new).get_distance(player) == math.inf:
                        # set's the new distance
                        dist = self.get_item(x_item, y_item).get_distance(player)
                        self.get_item(x_item, y_item).set_distance(player, dist + 1)
                        knot_queue.put([x_item_new, y_item_new])

                # right x+1
                x_item_new = x_item + 1
                y_item_new = y_item
                if self.get_item(x_item_new, y_item_new).get_owner() == 9:
                    if self.get_item(x_item_new, y_item_new).get_distance(player) == math.inf:
                        # set's the new distance
                        dist = self.get_item(x_item, y_item).get_distance(player)
                        self.get_item(x_item, y_item).set_distance(player, dist + 1)
                        knot_queue.put([x_item_new, y_item_new])

                # up y-1
                x_item_new = x_item
                y_item_new = y_item - 1
                if self.get_item(x_item_new, y_item_new).get_owner() == 9:
                    if self.get_item(x_item_new, y_item_new).get_distance(player) == math.inf:
                        # set's the new distance
                        dist = self.get_item(x_item, y_item).get_distance(player)
                        self.get_item(x_item, y_item).set_distance(player, dist + 1)
                        knot_queue.put([x_item_new, y_item_new])

                # down y+1
                x_item_new = x_item
                y_item_new = y_item + 1
                if self.get_item(x_item_new, y_item_new).get_owner() == 9:
                    if self.get_item(x_item_new, y_item_new).get_distance(player) == math.inf:
                        # set's the new distance
                        dist = self.get_item(x_item, y_item).get_distance(player)
                        self.get_item(x_item, y_item).set_distance(player, dist + 1)
                        knot_queue.put([x_item_new, y_item_new])


# Function to find target direction
def get_next(x, y):
    print(str(x) + ' ' + str(y) + ' ' + str(grid.get_item(x, y, debug=False).get_owner()), file=sys.stderr, flush=True)
    if grid.get_item(x - 1, y).get_owner() == 9:
        return 'LEFT'
    elif grid.get_item(x + 1, y).get_owner() == 9:
        return 'RIGHT'
    elif grid.get_item(x, y - 1).get_owner() == 9:
        return 'UP'
    else:
        return 'DOWN'


grid = Grid()
first = True
x_user = 0
y_user = 0

# game loop
while True:
    # number_players: total number of players (2 to 4).
    # p: your player number (0 to 3).
    number_players, your_number = [int(i) for i in input().split()]
    for number_player in range(number_players):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        grid.set_data(x1, y1, number_player)

        # adds the players starting position on the first round
        # is needed because if i go second the starting pos is missing in the grid of the first going players
        if first:
            grid.set_data(x0, y0, number_player)

        # my current position
        if number_player == your_number:
            x_user = x1
            y_user = y1

        # set's the current position of a player
        grid.x_cur[number_player] = x1
        grid.y_cur[number_player] = y1


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # prints the whole grid for visualisation
    grid.print_grid_owner()
    grid.calc_shortest_path_for_grid()

    grid.print_grid_dist(your_number)

    # A single line with UP, DOWN, LEFT or RIGHT
    print(get_next(x_user, y_user))

    # reset's to infinite for next calc
    grid.reset_grid_distance()

    # set first to false
    first = False

# TODO:
# remove dead people from grid (needed as soon as more than two player
#
# calc dist for each pos for each player if reachable else -1
# do this for each step up down left right
# set pos owner to the person which its shortest
# sum them up so you know how many steps you can make before game over
# take the best of the four for you max(yours - thems)
