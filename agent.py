"""
Legend:
. = visited tile
A = agent
G = gold
W = wumpus
S = stench
w = potential wumpus
nw = no wumpus
P = pit
B = breeze
p = potential pit
np = no pit
"""

import time


class Agent():
    """Defining Agent"""

    def __init__(self, world, label_grid):
        self.world = world  # world is already build by world module
        self.knowledge_base = [[[] for i in range(self.world.cols)] for j in range(
            self.world.rows)]  # knowledge base of size of world dimensions
        self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
            'A')  # setting up Agent position
        self.stenches = 0  # total stenches
        self.path_out_cave = [[self.world.agent_row, self.world.agent_col]]
        self.visited()
        self.world.cave_entrance_row = self.world.agent_row
        self.world.cave_entrance_col = self.world.agent_col
        self.found_gold = False
        self.got_gold = False
        self.exited = False
        self.label_grid = label_grid

        self.rebuild_world()

    def rebuild_world(self):
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                updated_text = []
                if 'A' in self.knowledge_base[i][j]:
                    updated_text.append('A')
                if 'w' in self.knowledge_base[i][j]:
                    updated_text.append('W')
                if 'p' in self.knowledge_base[i][j]:
                    updated_text.append('P')
                if 'B' in self.knowledge_base[i][j]:
                    updated_text.append('B')
                if 'S' in self.knowledge_base[i][j]:
                    updated_text.append('S')
                if 'G' in self.knowledge_base[i][j]:
                    updated_text.append('G')

                updated_str = ""  # for gui representation
                self.label_grid[i][j].change_text(
                    updated_str.join(updated_text))
                if '.' in self.knowledge_base[i][j]:
                    self.label_grid[i][j].label.config(bg="green")
                if 'G' in self.knowledge_base[i][j] and '.' in self.knowledge_base[i][j]:
                    self.label_grid[i][j].label.config(bg="gold")

                self.label_grid[i][j].label.update()

    def backtrack(self):
        # print(self.path_out_cave)
        print("path out of cave: ", self.path_out_cave[-1][0])
        if self.world.agent_row-1 == self.path_out_cave[-1][0]:
            self.move('u')
        if self.world.agent_row+1 == self.path_out_cave[-1][0]:
            self.move('d')
        if self.world.agent_col+1 == self.path_out_cave[-1][1]:
            self.move('r')
        if self.world.agent_col-1 == self.path_out_cave[-1][1]:
            self.move('l')

        del self.path_out_cave[-1]

    def leave_cave(self):
        print("in leave"+str(self.path_out_cave))
        for tile in reversed(self.path_out_cave):
            if self.world.agent_row-1 == tile[0]:
                self.move('u')
            if self.world.agent_row+1 == tile[0]:
                self.move('d')
            if self.world.agent_col+1 == tile[1]:
                self.move('r')
            if self.world.agent_col-1 == tile[1]:
                self.move('l')

            if self.world.cave_entrance_row == self.world.agent_row:
                if self.world.cave_entrance_col == self.world.agent_col:
                    if self.found_gold == True:
                        self.exited = True
                        break

    def explore_world(self):
        last_move = ''
        already_moved = False
        print("knowledge_base: ", self.knowledge_base)
        while self.found_gold == False:
            if self.found_gold == True:
                break

            try:
                if '.' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col] and self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('u'):
                            already_moved = True
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1] and self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                    if already_moved == False:
                        if self.move('r'):
                            already_moved = True
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col] and self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('d'):
                            already_moved = True
                    # print(self.path_out_cave)
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1] and self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                    if already_moved == False:
                        if self.move('l'):
                            already_moved = True
                    # print(self.path_out_cave)
            except IndexError:
                pass

            if already_moved == False:
                self.backtrack()

            already_moved = False

    def move(self, direction):

        self.rebuild_world()

        if self.found_gold == True and self.got_gold == False:
            self.got_gold == True
            if 'G' in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].remove(
                    'G')

        successful_move = False
        if direction == 'u':
            if self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                successful_move = self.move_up()
        if direction == 'r':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right()
        if direction == 'd':
            if self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down()
        if direction == 'l':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left()

        if successful_move:
            self.add_indicators_knowledge_base()
            self.visited()
            self.predict_wumpus()
            self.predict_pits()
            self.clean_predictions()
            self.confirm_wumpus_knowledge()

            if 'G' in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                # print("You found the gold! Time to leave!")
                self.found_gold = True

            if self.found_gold == False:
                self.path_out_cave.append(
                    [self.world.agent_row, self.world.agent_col])

        # print("Successful move: " + str(successful_move))

            time.sleep(1.5)

        return successful_move

    def add_indicators_knowledge_base(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'B' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                    'B')
        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'S' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                    'S')
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                    'G')
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                    'P')
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'W' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                    'W')

    def predict_pits(self):
        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'p' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row -
                                                1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'p' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col+1].append(
                                'p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'p' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row +
                                                1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'p' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col-1].append(
                                'p')
        except IndexError:
            pass

    def predict_wumpus(self):
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'w' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row -
                                                1][self.world.agent_col].append('w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'w' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col+1].append(
                                'w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'w' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row +
                                                1][self.world.agent_col].append('w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'w' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col-1].append(
                                'w')
        except IndexError:
            pass

    def clean_predictions(self):
        self.stenches = 0

        for i in range(self.world.rows):
            for j in range(self.world.cols):
                if 'S' in self.knowledge_base[i][j]:
                    self.stenches += 1
                if 'w' in self.knowledge_base[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge_base[i-1][j]:
                                if 'S' not in self.knowledge_base[i-1][j]:
                                    self.knowledge_base[i][j].remove('w')
                                    self.knowledge_base[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if '.' in self.knowledge_base[i][j+1]:
                                if 'S' not in self.knowledge_base[i][j+1]:
                                    self.knowledge_base[i][j].remove('w')
                                    self.knowledge_base[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if '.' in self.knowledge_base[i+1][j]:
                                if 'S' not in self.knowledge_base[i+1][j]:
                                    self.knowledge_base[i][j].remove('w')
                                    self.knowledge_base[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge_base[i][j-1]:
                                if 'S' not in self.knowledge_base[i][j-1]:
                                    self.knowledge_base[i][j].remove('w')
                                    self.knowledge_base[i][j].append('nw')
                    except IndexError:
                        pass

                if 'p' in self.knowledge_base[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge_base[i-1][j]:
                                if 'B' not in self.knowledge_base[i-1][j]:
                                    self.knowledge_base[i][j].remove('p')
                                    self.knowledge_base[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if '.' in self.knowledge_base[i][j+1]:
                                if 'B' not in self.knowledge_base[i][j+1]:
                                    self.knowledge_base[i][j].remove('p')
                                    self.knowledge_base[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if '.' in self.knowledge_base[i+1][j]:
                                if 'B' not in self.knowledge_base[i+1][j]:
                                    self.knowledge_base[i][j].remove('p')
                                    self.knowledge_base[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge_base[i][j-1]:
                                if 'B' not in self.knowledge_base[i][j-1]:
                                    self.knowledge_base[i][j].remove('p')
                                    self.knowledge_base[i][j].append('np')
                    except IndexError:
                        pass

    def confirm_wumpus_knowledge(self):
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                if 'w' in self.knowledge_base[i][j]:
                    stenches_around = 0
                    try:
                        if i-1 >= 0:
                            if 'S' in self.knowledge_base[i-1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if 'S' in self.knowledge_base[i][j+1]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if 'S' in self.knowledge_base[i+1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if 'S' in self.knowledge_base[i][j-1]:
                                stenches_around += 1
                    except IndexError:
                        pass

                    if stenches_around < self.stenches:
                        self.knowledge_base[i][j].remove('w')
                        self.knowledge_base[i][j].append('nw')

    def move_up(self):
        try:
            if self.world.agent_row-1 >= 0:
                self.remove_agent()
                self.world.agent_row -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_right(self):
        try:
            if self.world.agent_col+1 < self.world.cols:
                self.remove_agent()
                self.world.agent_col += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_down(self):
        try:
            if self.world.agent_row+1 < self.world.rows:
                self.remove_agent()
                self.world.agent_row += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_left(self):
        try:
            if self.world.agent_col-1 >= 0:
                self.remove_agent()
                self.world.agent_col -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def remove_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].remove(
            'A')
        self.knowledge_base[self.world.agent_row][self.world.agent_col].remove(
            'A')

    def add_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].append(
            'A')
        self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
            'A')

    def visited(self):
        if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append(
                '.')
            self.knowledge_base[self.world.agent_row][self.world.agent_col].append(
                '.')

    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have been slayed by the Wumpus 👾!")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have fallen into the pit 🕳!")
            return True
        else:
            return False

    def is_safe_move(self, row, col):
        try:
            if 'w' in self.knowledge_base[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'p' in self.knowledge_base[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'W' in self.knowledge_base[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.knowledge_base[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass

        return True
