import constants as cs
import tkinter as tk
from numpy import array, empty

class Rabbit(tk.Frame):
    pass

class Fox(tk.Frame):
    pass



class MainAppliaction(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        root.title("Tokki Survival")
        root.geometry("750x750")
        root.resizable(0, 0)

        self.world = tk.Canvas(root, width=1000, height=1000, highlightthickness=0, background="{}".format("#%02x%02x%02x" % (249,248,249)))
        self.world.pack()

        self.grids = empty([100,100])
        for col in range (0,100):
            for row in range (0,100):
                if cs.mapValues[col,row] == 0:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif cs.mapValues[col,row] == 1:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif cs.mapValues[col,row] == 2:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif cs.mapValues[col,row] == 3:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif cs.mapValues[col,row] == 4:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif cs.mapValues[col,row] == 5:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif cs.mapValues[col,row] == 6:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif cs.mapValues[col,row] == 7:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif cs.mapValues[col,row] == 8:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif cs.mapValues[col,row] == 9:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif cs.mapValues[col,row] == 10:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif cs.mapValues[col,row] == 11:
                    self.grids[col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))



if __name__ == "__main__":
    root = tk.Tk()
    MainAppliaction(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
