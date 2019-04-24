from sys import stdout

class LifeGame:

	def __init__(self, filename):
		self.current_generation_grid = []
		self.current_generation_row = []
		self.next_generation_grid = []
		self.next_generation_row = []
		self.read_file(filename)
		self.initialize_next_generation()
		
	def read_file(self, filename):
		""" Populate grid from file """
		with open(filename) as file_object:
			line = file_object.readline() 
			while line:
				self.current_generation_row = []
				for index in range(len(line)):
					if line[index] != '\n':
						self.current_generation_row.append(int(line[index]))
				self.current_generation_grid.append(self.current_generation_row)
				line = file_object.readline()

	def initialize_next_generation(self):
		"""" initialize the next generation grid """	
		for row_index in range(len(self.current_generation_grid)):
			self.next_generation_row = []
			for column_index in range(len(self.current_generation_row)):
				self.next_generation_row.append(0)
			self.next_generation_grid.append(self.next_generation_row)	

	def get_alive_neighbours_count(self, x_coordinate, y_coordinate):
		"Get the number of alive neighbours of a given cell"
		alive_neighbours = 0
		x_axis_start = x_coordinate - 1 if x_coordinate > 0 else 0 
		x_axis_end = x_coordinate + 2 if x_coordinate < len(self.current_generation_grid) - 1 else x_coordinate + 1
		y_axis_start = y_coordinate - 1 if y_coordinate > 0 else 0 	
		y_axis_end = y_coordinate + 2 if y_coordinate < len(self.current_generation_row) - 1 else y_coordinate + 1

		for row_index in range(x_axis_start, x_axis_end):
			for column_index in range(y_axis_start, y_axis_end):
				if self.current_generation_grid[row_index][column_index] == 1:
					alive_neighbours += 1
		return alive_neighbours

	def populate_new_generation(self):
		"populate new generation after applying life rules"
		for row_index in range(len(self.current_generation_grid)):
			for column_index in range(len(self.current_generation_row)):
				if self.current_generation_grid[row_index][column_index] == 1:
					alive_neighbours_count = self.get_alive_neighbours_count(row_index,column_index) - 1
					if alive_neighbours_count < 2:
						self.next_generation_grid[row_index][column_index] = 0
					elif alive_neighbours_count == 2 or alive_neighbours_count == 3:
						self.next_generation_grid[row_index][column_index] = 1
					else:
						self.next_generation_grid[row_index][column_index] = 0
				elif self.current_generation_grid[row_index][column_index] == 0:
					alive_neighbours_count = self.get_alive_neighbours_count(row_index,column_index) 
					if alive_neighbours_count == 3:
						self.next_generation_grid[row_index][column_index] = 1

	def display_new_generation(self):
		self.populate_new_generation()
		for row_index in range(len(self.current_generation_grid)):
			for column_index in range(len(self.current_generation_row)):
				stdout.write(str(self.next_generation_grid[row_index][column_index]))
			stdout.write('\n')


	def change_transition(self):
		self.current_generation_grid = self.next_generation_grid			
		self.next_generation_grid = []
		self.initialize_next_generation()