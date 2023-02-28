import tkinter
import statistics
from Grid import Grid
from Cell import AVG_TEMP_STATS, AVG_AIR_POLLUTION_STATS


CELL_WIDTH = 50
CELL_HEIGHT = 30


class App:
    def __init__(self, starting_air_pollution=0, air_pollution_factor=0.15):
        self.day = 1
        # initialize the matrix:
        self.grid = Grid(starting_air_pollution, air_pollution_factor)
        self.matrix = self.grid.cells_matrix
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)

        # GUI:
        self.window = tkinter.Tk()
        self.window.title("Maman 11 by Noam Sadeh")
        self.label = tkinter.Label(text="Day 1")
        self.label.pack()
        self.canvas = tkinter.Canvas(self.window, height=self.height * CELL_HEIGHT, width=self.width * CELL_WIDTH)
        self.canvas.pack()
        self.update_canvas()
        tkinter.Button(text="Start", command=self.main).pack()


    '''
    main: loop through 1 year, every day updates each cell of the mat,
    and draw it on canvas.
    '''
    def main(self):
        self.day += 1
        if self.day == 366:  # after 1 year stop the program and write the stats
            f = open('temp.txt', 'w')
            for n in AVG_TEMP_STATS:
                f.write("{}\n".format(n))
            f.close()
            f = open('air.txt', 'w')
            for n in AVG_AIR_POLLUTION_STATS:
                f.write("{}\n".format(n))
            f.close()
            return

        self.label.config(text=f'Day {self.day}')
        self.update_cells()
        self.canvas.delete("all")
        self.update_canvas()  # draw new canvas
        self.stats()  # save she stats
        self.window.after(10, self.main)

    '''
    update_canvas: draw text and makes rectangle with color for each cell in the canvas
    '''
    def update_canvas(self):
        matrix = self.grid.cells_matrix
        for x in range(self.width):
            for y in range(self.height):
                cell = matrix[y][x]
                self.canvas.create_rectangle(x * CELL_WIDTH, y * CELL_HEIGHT, (x + 1) * CELL_WIDTH,
                                             (y + 1) * CELL_HEIGHT,
                                             fill=cell.color)
                self.canvas.create_text((x + 0.7) * CELL_WIDTH, (y + 0.3) * CELL_HEIGHT,
                                        text="{}%".format(round(cell.cloudiness)),
                                        fill="navy")
                self.canvas.create_text((x + 0.3) * CELL_WIDTH, (y + 0.3) * CELL_HEIGHT,
                                        text="{}".format(round(cell.air_pollution)), fill="red")
                self.canvas.create_text((x + 0.7) * CELL_WIDTH, (y + 0.7) * CELL_HEIGHT,
                                        text="{}".format(cell.wind_direction))

                self.canvas.create_text((x + 0.3) * CELL_WIDTH, (y + 0.7) * CELL_HEIGHT,
                                        text="{}C".format(round(cell.temperature)))
    '''
    update_cells: updates each cell in the mat object. each cell is influenced by his neighbors.    
    '''
    def update_cells(self):
        old_matrix = self.matrix
        for x in range(self.width):
            for y in range(self.height):
                neighbors = self.get_neighbors(y, x, old_matrix)
                self.matrix[y][x].update_values(neighbors)

    '''
    get_neighbors:  find the neighbors of a given cell
    Input
        > 'row' - index of the row
        > 'col' - index of the column
        > 'mat' - the object mat
    Returns
        > list of 4 cell objects (the neighbors) 
    '''
    def get_neighbors(self, row, col, mat):
        rows, cols = self.height, self.width
        neighbors = []

        # add right neighbor:
        if col == cols - 1:
            neighbors.append(mat[row][0])
        else:
            neighbors.append(mat[row][col + 1])
        # add left neighbor:
        if col == 0:
            neighbors.append(mat[row][cols - 1])
        else:
            neighbors.append(mat[row][col - 1])
        # add upper neighbor:
        if row == 0:
            neighbors.append(mat[rows - 1][col])
        else:
            neighbors.append(mat[row - 1][col])
        # add down neighbor:
        if row == rows - 1:
            neighbors.append(mat[0][col])
        else:
            neighbors.append(mat[row + 1][col])
        return neighbors

    '''
    stats: Save's the data of the program for analyzing the data in the jupyter notebook
    '''
    def stats(self):
        avg_temp = 0
        avg_pollution = 0
        for x in range(self.width):
            for y in range(self.height):
                avg_temp += self.matrix[y][x].temperature
                avg_pollution += self.matrix[y][x].air_pollution
        avg_temp = avg_temp / (self.width * self.height)
        AVG_TEMP_STATS.append(avg_temp)

        avg_pollution = avg_pollution / (self.width * self.height)
        AVG_AIR_POLLUTION_STATS.append(avg_pollution)


if __name__ == '__main__':
    app = App()
    app.window.mainloop()

    #print stats:
