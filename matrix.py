'''
Class Matrix represents the board of the game
'''
class Matrix:
    def __init__(self, size, chromosome):
        self.size = size
        self.cells = [[0] * self.size for i in range(self.size)]
        self.insert_chromosome(chromosome)

    '''
    insert_chromosome: insert the chromosome to the middle of the mat
        Input
            > 'chromosome': a list that contains 0,1.
    '''
    def insert_chromosome(self, chromosome):
        counter = 0
        mid = round(self.size / 2) - 1
        for i in range(mid, mid + 3):
            for j in range(mid, mid + 3):
                self.cells[i][j] = chromosome[counter]
                counter += 1

    '''
    change_mat: change the mat cells according to the 'game of life' rules
    '''
    def change_mat(self):
        new_cells = [[0] * self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                neighbors = self.count_neighbors(i, j)
                if self.cells[i][j] and (neighbors != 2 and neighbors != 3):
                    new_cells[i][j] = 0
                elif self.cells[i][j] == 0 and neighbors == 3:
                    new_cells[i][j] = 1
                elif self.cells[i][j] == 1:
                    new_cells[i][j] = 1
        self.cells = new_cells


    '''
    count_neighbors: counting how many alive cells is near a given cell
        Input
            > 'row' the row index
            > 'col' the column index
        Returns number of neighbors
    '''
    def count_neighbors(self, row, col):
        neighbours = 0
        neighbours -= self.cells[row][col]
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i >= 0 and j >= 0 and i < self.size and j < self.size:
                    neighbours += self.cells[i][j]
        return neighbours

    '''
    calculate_area: calculates the maximum area of rectangle that blocks the living cells
        Returns
            > the area
    '''

    def calculate_area(self):
        coordinates = []
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j]:
                    coordinates.append([i, j])
        if not coordinates:
            return 0

        sorted_x_coor = sorted(coordinates, key=lambda x: x[0])
        sorted_y_coor = sorted(coordinates, key=lambda x: x[1])
        height = sorted_x_coor[-1][0] - sorted_x_coor[0][0] + 1
        weight = sorted_y_coor[-1][1] - sorted_y_coor[0][1] + 1
        return height * weight

    '''
    sum_cells: sum of the living cells in the mat
        Returns
            > the sum
    '''
    def sum_cells(self):
        counter = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j]:
                    counter += 1
        return counter

