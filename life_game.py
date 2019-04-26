from sys import stdout

class LifeGame:

	def __init__(self, filename):
		self.current_generation_grid = []
		self.row = []
		self.next_generation_grid = []
		self.read_file(filename)
		self.initialize_next_generation()
		self.mapping = { 1: { 0:0, 1:0, 2:1, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0 },
          	0: {0:0, 1:0, 2:0, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0}
		}
		
	def read_file(self, filename):
		""" Populate grid from file """
		with open(filename) as file_object:
			line = file_object.readline() 
			while line:
				self.row = []
				for index in range(len(line)):
					if line[index] != '\n':
						self.row.append(int(line[index]))
				self.current_generation_grid.append(self.row)
				line = file_object.readline()

	def initialize_next_generation(self):
		"""" initialize the next generation grid """	
		for row in range(len(self.current_generation_grid)):
			clone_of_row = []
			for cell in range(len(self.row)):
				clone_of_row.append(0)
			self.next_generation_grid.append(clone_of_row)	

	def get_alive_neighbours_count(self, x_coordinate, y_coordinate):
		"Get the number of alive neighbours of a given cell"
		alive_neighbours = 0
		grid_size = len(self.current_generation_grid)-1
		x_axis_start = x_coordinate-1 if x_coordinate > 0 else 0 
		x_axis_end = x_coordinate+2 if x_coordinate < grid_size else x_coordinate+1
		y_axis_start = y_coordinate-1 if y_coordinate > 0 else 0 	
		y_axis_end = y_coordinate+2 if y_coordinate < len(self.row)-1 else y_coordinate+1

		for row_index in range(x_axis_start, x_axis_end):
			for column_index in range(y_axis_start, y_axis_end):
				if self.current_generation_grid[row_index][column_index] == 1:
					alive_neighbours += 1
		if self.current_generation_grid[x_coordinate][y_coordinate] == 1:
			return alive_neighbours-1
		else: 
			return alive_neighbours

	def populate_new_generation(self):
		"populate new generation after applying life rules"
		for row in range(len(self.current_generation_grid)):
			for cell in range(len(self.row)):
				life_status = self.current_generation_grid[row][cell]
				alive_cells = self.get_alive_neighbours_count(row,cell)
				self.next_generation_grid[row][cell] = self.mapping[life_status][alive_cells]	

	def display_new_generation(self):
		"display the grid of new generation"
		for row in self.next_generation_grid:
			for cell in row:
				stdout.write(str(cell))		
			stdout.write('\n')	

	def change_transition(self):
		self.current_generation_grid = self.next_generation_grid			
		self.next_generation_grid = []
		self.initialize_next_generation()