import tkinter as tk
from matrix import Matrix

'''
This clas app represents the user interface of 'Game Of Life'
'''
class App:
    def __init__(self, size, cell_size, chromosome, generations):
        self.counter = 0
        self.length = size
        self.cell_size = cell_size
        self.generations = generations
        self.root = tk.Tk()
        self.root.title("Maman 12 by Noam Sadeh")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.mat = Matrix(size, chromosome)
        self.canvas = tk.Canvas(self.root, height=size * cell_size, width=size * cell_size, bg="white")
        self.create_canvas()
        self.canvas.pack()
        self.update_canvas([[0] * size for i in range(size)])
        tk.Button(self.root, text="start", command=self.game_of_life).pack()
        self.root.mainloop()

    '''
    create_canvas: initialize the canvas rows and columns
    '''
    def create_canvas(self):
        x = 0
        y = 0
        for i in range(self.length):
            for j in range(self.length):
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size)
                x += self.cell_size
            y += self.cell_size
            x = 0

    '''
        update_canvas: updates the canvas according to 'Game Of Life' rules
    '''
    def update_canvas(self, old_mat):
        x = 0
        y = 0
        for j in range(self.length):
            for i in range(self.length):
                if self.mat.cells[i][j] != old_mat[i][j]:
                    if self.mat.cells[i][j]:
                        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="black")
                    else:
                        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="white")
                x += self.cell_size
            y += self.cell_size
            x = 0

    '''
        reset_canvas: delete all the rectangles drawn on the canvas and draw them again 
    '''
    def reset_canvas(self):
        self.canvas.delete("all")
        self.create_canvas()
        x = 0
        y = 0
        for j in range(self.length):
            for i in range(self.length):
                if self.mat.cells[i][j]:
                    self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="black")
                x += self.cell_size
            y += self.cell_size
            x = 0

    '''
    game_of_life: the main method for looping the app.
    '''
    def game_of_life(self):
        self.counter += 1
        self.label.config(text=f'generation {self.counter}')
        if self.counter == self.generations:
            return
        if self.counter % 15 == 0: #drawing infinite squares will slow down the program, reset every 15 generations
            self.reset_canvas()
        old_mat = self.mat.cells
        self.mat.change_mat()
        self.update_canvas(old_mat)
        self.root.after(100, self.game_of_life)