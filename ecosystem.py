import constants as cs
import tkinter as tk
from numpy import array, empty


class MainApp:

    def __init__(self, master):
        self.master = master
        
        self.master.title("Tokki_Survival")
        self.master.geometry("1000x700") 
        self.master.resizable(0,0)

        self.map = Map(self.master)


 
class Map(MainApp):

    def __init__(self,master):
        self.master = master
        self.world = tk.Canvas(self.master, width=cs.mapSize, height=cs.mapSize, highlightthickness=0, background="#f9f8f9")
        self.world.pack(side="left")

        self.grids = empty([100,100])
        
        self.miniMapValues = empty([cs.zoomPix,cs.zoomPix])
        self.miniGrids = empty([cs.zoomPix,cs.zoomPix])
        self.miniLocation = [0,0]
        
        self.count = -1
        self.pressed = False

        self.Create_map()
        self.Create_menu()

    def Create_map(self):
        for col in range (0,100): # Reads the grid colors and status
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

    def Create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.subMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="View", menu=self.subMenu)
        self.subMenu.add_command(label="Zoom in",command=self.Zoom_in)
        self.subMenu.add_command(label="Zoom out",command=self.Zoom_out)
        self.subMenu.entryconfigure("Zoom out", state="disabled")

    def Create_minimap(self):
        for col in range (0,100): # Reads the grid colors and status
            for row in range (0,100):
                pin = cs.mapSize - cs.miniMapSize
                if cs.mapValues[col,row] == 0:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif cs.mapValues[col,row] == 1:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif cs.mapValues[col,row] == 2:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif cs.mapValues[col,row] == 3:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif cs.mapValues[col,row] == 4:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif cs.mapValues[col,row] == 5:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif cs.mapValues[col,row] == 6:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif cs.mapValues[col,row] == 7:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif cs.mapValues[col,row] == 8:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif cs.mapValues[col,row] == 9:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif cs.mapValues[col,row] == 10:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif cs.mapValues[col,row] == 11:
                    self.grids[col,row] = self.world.create_rectangle(pin+row*cs.miniGridSize, pin+col*cs.miniGridSize,pin+(row+1)*cs.miniGridSize, pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

        self.world.create_line(pin+self.miniLocation[0],pin+self.miniLocation[1],pin+self.miniLocation[0]+cs.barSize,pin+self.miniLocation[1], fill="white", width = 2)
        self.world.create_line(pin+self.miniLocation[0],pin+self.miniLocation[1],pin+self.miniLocation[0],pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.world.create_line(pin+self.miniLocation[0],pin+self.miniLocation[1]+cs.barSize,pin+self.miniLocation[0]+cs.barSize,pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.world.create_line(pin+self.miniLocation[0]+cs.barSize,pin+self.miniLocation[1],pin+self.miniLocation[0]+cs.barSize,pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)

    def Zoom_in(self):
        self.subMenu.entryconfigure("Zoom in", state="disabled")
        self.subMenu.entryconfigure("Zoom out", state="normal")

        self.world.bind('<Motion>', self.Motion)
        self.world.bind('<ButtonPress-1>', self.OnClick)
        self.world.bind('<ButtonRelease-1>', self.OffClick)

        self.Zoom_in_process()      

    def Zoom_in_process(self):
        self.world.delete("all")
        self.Minimap_fetch()
        self.Minimap_enlarge()
        self.Create_minimap()
        self.master.update()

    def Zoom_out(self):
        self.subMenu.entryconfigure("Zoom in", state="normal")
        self.subMenu.entryconfigure("Zoom out", state="disabled")

        self.world.unbind('<Motion>')
        self.world.unbind('<ButtonPress-1>')
        self.world.unbind('<ButtonRelease-1>')

        self.world.delete("all")
        self.Create_map()

    def Minimap_fetch(self):
        
        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                self.miniMapValues[col,row] = cs.mapValues[self.miniLocation[0]+col,self.miniLocation[1]+row]        

    def Minimap_enlarge(self):
        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                if self.miniMapValues[col,row] == 0:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif self.miniMapValues[col,row] == 1:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif self.miniMapValues[col,row] == 2:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif self.miniMapValues[col,row] == 3:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif self.miniMapValues[col,row] == 4:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif self.miniMapValues[col,row] == 5:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif self.miniMapValues[col,row] == 6:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif self.miniMapValues[col,row] == 7:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif self.miniMapValues[col,row] == 8:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif self.miniMapValues[col,row] == 9:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif self.miniMapValues[col,row] == 10:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif self.miniMapValues[col,row] == 11:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

    def Motion(self,event):
        a = [0,0]
        b = [0,0]
        
        if self.pressed:
            if self.count == -1:
                a = [event.x//cs.zoomPix,event.y//cs.zoomPix]
                self.count += 1

            elif self.count == 0:
                b = [event.x//cs.zoomPix,event.y//cs.zoomPix]
                self.miniLocation[0] = b[0] - a[0]
                self.miniLocation[1] = b[1] - a[1]
                print(self.miniLocation)
                self.count += 1

            elif self.count == 1:
                a = [event.x//cs.zoomPix,event.y//cs.zoomPix]
                self.miniLocation[0] = a[0] - b[0]
                self.miniLocation[1] = a[1] - b[1]
                print(self.miniLocation)
                self.count -= 1

            self.Zoom_in_process()

    def OnClick(self,event):
        self.pressed = True

    def OffClick(self,event):
        self.pressed = False

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__": 
    main()
