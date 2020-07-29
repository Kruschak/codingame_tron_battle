import math
import sys

# constants
# import time
from copy import deepcopy
from queue import Queue

GRID_SIZE_X = 30
GRID_SIZE_Y = 20


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Item:
    def __init__(self, owner):
        self._owner = owner
        self._dist = [math.inf] * 4
        self._closest_owner = -1

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner

    # gets the distance of a player
    def get_distance(self, player):
        return self._dist[player]

    # set the distance of a player
    def set_distance(self, player, distance):
        self._dist[player] = distance

    def get_closest_owner(self):
        return self._closest_owner

    def set_closest_owner(self):
        # Case 1: all inf
        # Case 2: 2 with same dist
        # Case 3: 1 min
        closest_player = 9
        if min(self._dist) != math.inf:
            min_distance = min(self._dist)
            if self._dist.count(min_distance) != 1:
                closest_player = 8
            else:
                closest_player = self._dist.index(min_distance)
        self._closest_owner = closest_player


class Grid:
    # contains the current positions of the players
    # TODO: needs to be set every round
    x_cur = [-1] * 4
    y_cur = [-1] * 4

    sum_closest_owner = -1

    def __init__(self):
        # self.data = [[Item(9)] * GRID_SIZE_Y for i in range(GRID_SIZE_X)]
        self.data = [[Item(9) for y in range(GRID_SIZE_Y)] for x in range(GRID_SIZE_X)]
        # print('LenX: ' + str(len(self.data)) + ' LenY: ' + str(len(self.data[0])), file=sys.stderr, flush=True)

    def get_item(self, x, y, debug=False):
        if debug:
            print('X: ' + str(x) + 'Y: ' + str(y), file=sys.stderr, flush=True)
        if 0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y:
            return self.data[x][y]
        else:
            return Item(-1)

    def print_grid_owner(self):
        print('Owners of the grid', file=sys.stderr, flush=True)
        for y in range(len(self.data[0])):
            for x in range(len(self.data)):
                print(self.get_item(x, y).get_owner(), file=sys.stderr, flush=True, end=' ')
            print('', file=sys.stderr, flush=True)

    def print_closest_owner(self):
        print('Print closest owner: ', file=sys.stderr, flush=True)
        for y in range(len(self.data[0])):
            for x in range(len(self.data)):
                print(self.get_item(x, y).get_closest_owner(), file=sys.stderr, flush=True, end=' ')
            print('', file=sys.stderr, flush=True)

    def print_grid_dist(self, player):
        print('Distance for player: ' + str(player), file=sys.stderr, flush=True)
        for y in range(len(self.data[0])):
            for x in range(len(self.data)):
                print('{:>3}'.format(self.get_item(x, y).get_distance(player)), file=sys.stderr, flush=True, end=' ')
            print('', file=sys.stderr, flush=True)

    def reset_grid_distance(self):
        for y in range(len(self.data[0])):
            for x in range(len(self.data)):
                self.get_item(x, y).set_distance(0, math.inf)
                self.get_item(x, y).set_distance(1, math.inf)
                self.get_item(x, y).set_distance(2, math.inf)
                self.get_item(x, y).set_distance(3, math.inf)

    # calculates the distance for each player to each grid pos
    def calc_shortest_path_for_grid(self):
        def calc_helper():
            if self.get_item(x_item_new, y_item_new).get_owner() == 9:
                if self.get_item(x_item_new, y_item_new).get_distance(player) == math.inf:
                    # print('Item added: x_item_new: ' + str(x_item_new) + ' y_item_new: ' + str(y_item_new),
                    # file=sys.stderr, flush=True) set's the new distance
                    dist = self.get_item(x_item, y_item).get_distance(player)
                    # print('Distance calced from x: ' + str(x_item) + ' y: ' + str(y_item) + ' dist: ' + str(dist),
                    # file=sys.stderr, flush=True)
                    self.data[x_item_new][y_item_new].set_distance(player, dist + 1)
                    knot_queue.put([x_item_new, y_item_new])
                    return True
            return False

        # counts the number of calculates distances
        calc_counter = 0
        for player in range(number_players):
            # print('Player: ' + str(player), file=sys.stderr, flush=True)
            # set's the distance of the starting point
            # self.get_item(self.x_cur[player], self.y_cur[player]).set_distance(player, 0)
            self.data[self.x_cur[player]][self.y_cur[player]].set_distance(player, 0)
            # test_dist = self.data[self.x_cur[player]][self.y_cur[player]].get_distance(player)
            # print('Distance loop initial pos: ' + str(test_dist), file=sys.stderr, flush=True)
            knot_queue = Queue()
            knot_queue.put([self.x_cur[player], self.y_cur[player]])

            debug_hold = 0

            while not knot_queue.empty() and debug_hold < 200000:
                debug_hold += 1
                # print('Calc Counter: ' + str(debug_hold), file=sys.stderr, flush=True)
                # print('Size but not sure: ' + str(knot_queue.qsize()), file=sys.stderr, flush=True)

                x_item, y_item = knot_queue.get()
                # print('Starting point x: ' + str(x_item) + ' y: ' + str(y_item), file=sys.stderr, flush=True)
                # no for loop cause every time only 4 possible ways
                # left x-1
                x_item_new = x_item - 1
                y_item_new = y_item
                if calc_helper():
                    calc_counter += 1
                # right x+1
                x_item_new = x_item + 1
                y_item_new = y_item
                if calc_helper():
                    calc_counter += 1

                # up y-1
                x_item_new = x_item
                y_item_new = y_item - 1
                if calc_helper():
                    calc_counter += 1

                # down y+1
                x_item_new = x_item
                y_item_new = y_item + 1
                if calc_helper():
                    calc_counter += 1

        print('Calculations to for distance made: ' + str(calc_counter), file=sys.stderr, flush=True)

    # calculates which field is probably got by which player
    def calc_closest_owner(self):
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                self.data[x][y].set_closest_owner()

    # sum's the fields up of each player
    def calc_sum_closest_owner(self):
        # calculate only for mme
        # for player in range(number_players):
        player = your_number
        sum_closest_owner = 0
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                # print('closest_owner: ' + str(self.data[x][y].get_closest_owner()) + ' player: ' + str(player),
                # file=sys.stderr, flush=True)
                if self.data[x][y].get_closest_owner() == player:
                    sum_closest_owner += 1
        # print('sum: ' + str(sum_closest_owner), file=sys.stderr, flush=True)
        self.sum_closest_owner = sum_closest_owner


# Function to find target direction
def get_next():
    # print(str(x) + ' ' + str(y) + ' ' + str(grid.get_item(x, y, debug=False).get_owner()), file=sys.stderr,
    # flush=True)

    max_own = max([gridL.sum_closest_owner, gridR.sum_closest_owner, gridU.sum_closest_owner, gridD.sum_closest_owner])
    if max_own == gridL.sum_closest_owner:
        return 'LEFT'
    elif max_own == gridR.sum_closest_owner:
        return 'RIGHT'
    elif max_own == gridU.sum_closest_owner:
        return 'UP'
    elif max_own == gridD.sum_closest_owner:
        return 'DOWN'
    else:
        print('WARNING: used default after finding no max', file=sys.stderr, flush=True)
        return 'LEFT'


grid = Grid()
first = True
x_user = 0
y_user = 0

# game loop
while True:
    # number_players: total number of players (2 to 4).
    # p: your player number (0 to 3).
    number_players, your_number = [int(i) for i in input().split()]
    print('start while', file=sys.stderr, flush=True)
    # for timing measurements
    # start_time = time.time()
    for number_player in range(number_players):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        grid.data[x1][y1].set_owner(number_player)

        # adds the players starting position on the first round
        # is needed because if i go second the starting pos is missing in the grid of the first going players
        if first:
            grid.data[x0][y0].set_owner(number_player)

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
    # grid.print_grid_owner()

    # calculates the shortest path but useless cause its just the current standing
    # grid.calc_shortest_path_for_grid()
    # grid.print_grid_dist(your_number)
    # grid.print_grid_dist(1)

    # every round to delete old data
    # copies the base item because it get's manipulated to simulate the next step
    print('253 before grid copies', file=sys.stderr, flush=True)
    gridL = deepcopy(grid)
    print('L copied', file=sys.stderr, flush=True)
    gridR = deepcopy(grid)
    print('R copied', file=sys.stderr, flush=True)
    gridU = deepcopy(grid)
    print('U copied', file=sys.stderr, flush=True)
    gridD = deepcopy(grid)
    print('D after grid copies', file=sys.stderr, flush=True)
    if grid.get_item(x_user - 1, y_user).get_owner() == 9:
        # set's the next step as owner to represent it as walked onto
        gridL.data[x_user - 1][y_user].set_owner(your_number)
        # set's the current position of you to represent step ahead
        gridL.x_cur[your_number] = x_user - 1
        gridL.y_cur[your_number] = y_user
        gridL.calc_shortest_path_for_grid()
        # gridL.print_grid_dist(your_number)
        gridL.calc_closest_owner()
        # gridL.print_closest_owner()
        gridL.calc_sum_closest_owner()
        print('L Sum closest owner: ' + str(gridL.sum_closest_owner), file=sys.stderr, flush=True)

    if grid.get_item(x_user + 1, y_user).get_owner() == 9:
        # set's the next step as owner to represent it as walked onto
        gridR.data[x_user + 1][y_user].set_owner(your_number)
        # set's the current position of you to represent step ahead
        gridR.x_cur[your_number] = x_user + 1
        gridR.y_cur[your_number] = y_user
        gridR.calc_shortest_path_for_grid()
        # gridL.print_grid_dist(your_number)
        gridR.calc_closest_owner()
        # gridL.print_closest_owner()
        gridR.calc_sum_closest_owner()
        print('R Sum closest owner: ' + str(gridR.sum_closest_owner), file=sys.stderr, flush=True)

    if grid.get_item(x_user, y_user - 1).get_owner() == 9:
        # set's the next step as owner to represent it as walked onto
        gridU.data[x_user][y_user - 1].set_owner(your_number)
        # set's the current position of you to represent step ahead
        gridU.x_cur[your_number] = x_user
        gridU.y_cur[your_number] = y_user - 1
        gridU.calc_shortest_path_for_grid()
        # gridL.print_grid_dist(your_number)
        gridU.calc_closest_owner()
        # gridL.print_closest_owner()
        gridU.calc_sum_closest_owner()
        print('U Sum closest owner: ' + str(gridU.sum_closest_owner), file=sys.stderr, flush=True)

    if grid.get_item(x_user, y_user + 1).get_owner() == 9:
        # set's the next step as owner to represent it as walked onto
        gridD.data[x_user][y_user + 1].set_owner(your_number)
        # set's the current position of you to represent step ahead
        gridD.x_cur[your_number] = x_user
        gridD.y_cur[your_number] = y_user + 1
        gridD.calc_shortest_path_for_grid()
        # gridD.print_grid_dist(your_number)
        gridD.calc_closest_owner()
        # gridD.print_closest_owner()
        gridD.calc_sum_closest_owner()
        print('D Sum closest owner: ' + str(gridD.sum_closest_owner), file=sys.stderr, flush=True)

    # set first to false
    first = False

    # A single line with UP, DOWN, LEFT or RIGHT
    print(get_next())

    # reset's to infinite for next calc not needed because it's just the copy base
    # grid.reset_grid_distance()



    # should be the last to measure loop time
    # print("--- %s seconds ---" % (time.time() - start_time), file=sys.stderr, flush=True)

# TODO:

# remove dead people from grid (needed as soon as more than two player perhaps calculate the biggest coherent area
# instead of pos_owner to calculate splittings the turn after into calculation calc dist for each pos for each player
# if reachable else -1 do this for each step up down left right set pos owner to the person which its shortest sum
# them up so you know how many steps you can make before game over take the best of the four for you max(yours -
# them's)
