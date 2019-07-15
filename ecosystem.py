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
        root.title("너가 정해라 이거 ㅋㅋㅋ")
        root.geometry("500x500")
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




if __name__ == "__main__":
    root = tk.Tk()
    MainAppliaction(root).pack(side="top", fill="both", expand=True)
    root.mainloop()