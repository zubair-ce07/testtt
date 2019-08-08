"""
	file containing gamne of life class
"""
from sys import stdout

class LifeGame:
    """
        containing functions to generate next generation
        and display next generation
    """

    CELL_NEXT_GEN_MAP = {
        1: {0:0, 1:0, 2:1, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0},
        0: {0:0, 1:0, 2:0, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0}
        }

    def __init__(self, filename):
        """
            create all data members and call read file function
            :params
            argument (string) : name of file
        """
        self.current_gen_grid = []
        self.row = []
        self.next_gen_grid = []
        self.read_file(filename)
        self.initialize_next_generation()

    def read_file(self, filename):
        """
            Populate grid from file
            :params
                argument (string) : name of file
        """
        with open(filename) as file_object:
            line = file_object.readline()
            while line:
                self.row = []
                for index, _ in enumerate(line):
                    if line[index] != '\n':
                        self.row.append(int(line[index]))
                self.current_gen_grid.append(self.row)
                line = file_object.readline()

    def initialize_next_generation(self):
        """
            initialize the next generation grid
        """
        for _ in range(len(self.current_gen_grid)):
            clone_of_row = []
            for _ in range(len(self.row)):
                clone_of_row.append(0)
            self.next_gen_grid.append(clone_of_row)

    def get_alive_neighbours_count(self, x_coordinate, y_coordinate):
        """
            Get the number of alive neighbours of a given cell
            :params
                argument-1 (int) : x_coordinate of current cell
                argument-2 (int) : y_coordinate of current cell
                return (int) : number of alive neighbours
        """
        alive_neighbours = 0
        grid_size = len(self.current_gen_grid) - 1
        x_axis_start = x_coordinate - 1 if x_coordinate > 0 else 0
        x_axis_end = x_coordinate + 2 if x_coordinate < grid_size else x_coordinate + 1
        y_axis_start = y_coordinate - 1 if y_coordinate > 0 else 0
        y_axis_end = y_coordinate + 2 if y_coordinate < len(self.row) - 1 else y_coordinate + 1

        for row_index in range(x_axis_start, x_axis_end):
            for column_index in range(y_axis_start, y_axis_end):
                if self.current_gen_grid[row_index][column_index] == 1:
                    alive_neighbours += 1
        if self.current_gen_grid[x_coordinate][y_coordinate] == 1:
            return alive_neighbours - 1
        return alive_neighbours

    def populate_new_generation(self):
        """
            populate new generation after applying life rules
        """
        for row in range(len(self.current_gen_grid)):
            for cell in range(len(self.row)):
                life_status = self.current_gen_grid[row][cell]
                alive_cells = self.get_alive_neighbours_count(row, cell)
                self.next_gen_grid[row][cell] = self.CELL_NEXT_GEN_MAP[life_status][alive_cells]

    def display_new_generation(self):
        """
            display the grid of new generation
        """
        for row in self.next_gen_grid:
            for cell in row:
                stdout.write(str(cell))
            stdout.write('\n')

    def change_transition(self):
        """
        change the transition of after generating next generation
        """
        self.current_gen_grid = self.next_gen_grid
        self.next_gen_grid = []
        self.initialize_next_generation()
