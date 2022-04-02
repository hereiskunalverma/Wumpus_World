from file_parser import File_Parser
from file_parser import File_Parser


class World():
    """Generating World"""

    def __init__(self):
        self.world = [[]]  # world dimensions is of row x col matrix
        self.rows = 0  # number of rows
        self.cols = 0  # number of cols
        self.agent_row = 0  # agent row number
        self.agent_col = 0  # agent col number
        self.cave_row = 0  # cave starting
        self.cave_col = 0

    def generate_world(self, file):
        file_parser = File_Parser(file)
        self.rows = int(file_parser.row_col[0])
        self.cols = int(file_parser.row_col[1])
        self.world = [[[] for i in range(self.cols)] for j in range(self.rows)]
        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.world[self.agent_row][self.agent_col].append('A')
        self.world[int(file_parser.wumpus[1])][int(
            file_parser.wumpus[2])].append(file_parser.wumpus[0])
        self.world[int(file_parser.gold[1])][int(
            file_parser.gold[2])].append(file_parser.gold[0])
        for pit in file_parser.pits:
            self.world[int(pit[1])][int(pit[2])].append(pit[0])

        self.populate()

    def populate(self):

        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(len(self.world[i][j])):
                    if self.world[i][j][k] == 'W':
                        try:
                            if i-1 >= 0:
                                if 'S' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('S')
                        except IndexError:
                            pass
                        try:
                            if j+1 < self.cols:
                                if 'S' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('S')
                        except Exception as e:
                            pass

                        try:
                            if i+1 < self.rows:
                                if 'S' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('S')
                        except Exception as e:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'S' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('S')
                        except Exception as e:
                            pass

                    if self.world[i][j][k] == 'P':
                        try:
                            if i-1 >= 0:
                                if 'B' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('B')
                        except IndexError:
                            pass
                        try:
                            if j+1 < self.cols:
                                if 'B' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('B')
                        except Exception as e:
                            pass

                        try:
                            if i+1 < self.rows:
                                if 'B' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('B')
                        except Exception as e:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'B' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('B')
                        except Exception as e:
                            pass
