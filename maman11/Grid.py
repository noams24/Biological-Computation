from Cell import Cell

'''
Grid: the grid of the map
'''
class Grid():
    def __init__(self, starting_air_pollution, air_pollution_factor):
        self.air_pollution_factor = air_pollution_factor
        self.starting_air_pollution = starting_air_pollution

        self.cells_matrix = self.load_map("map.csv")
        self.width = len(self.cells_matrix[0])
        self.height = len(self.cells_matrix)


    '''
    load_map: loads the map from the file 'map.csv'
        Input
            > 'filename' the file of the map
        Returns
            > the cells of the matrix
    '''
    def load_map(self, filename):
        with open(filename) as file:
            lines = file.read().splitlines()
            map = [line.split(",") for line in lines]
            width = len(map[0])
            height = len(map)
            cells_matrix = [[0] * width for i in range(height)]
            for x in range(height):
                for y in range(width):
                    cells_matrix[x][y] = Cell(map[x][y], self.starting_air_pollution,self.air_pollution_factor)
            return cells_matrix
