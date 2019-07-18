import constants as cs
import tkinter as tk
from numpy import array, empty, set_printoptions, inf
from random import randint



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

        self.grids = empty([2,100,100], dtype=int)
        
        self.miniMapValues = empty([cs.zoomPix,cs.zoomPix], dtype=int)
        self.miniGrids = empty([cs.zoomPix,cs.zoomPix], dtype=int)
        self.miniLocation = [0,0]
        self.pin = cs.mapSize - cs.miniMapSize

        self.count = -1
        self.pressed = False

        self.box = empty([4], dtype=int)

        self.Create_map()
        self.Create_menu()

        self.game = Game(self.master,self.world,self.grids)

    def Create_map(self):
        for col in range (0,100): # Reads the grid colors and status
            for row in range (0,100):
                if cs.mapValues[col,row] == 0:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif cs.mapValues[col,row] == 1:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif cs.mapValues[col,row] == 2:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif cs.mapValues[col,row] == 3:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif cs.mapValues[col,row] == 4:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif cs.mapValues[col,row] == 5:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif cs.mapValues[col,row] == 6:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif cs.mapValues[col,row] == 7:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif cs.mapValues[col,row] == 8:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif cs.mapValues[col,row] == 9:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif cs.mapValues[col,row] == 10:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif cs.mapValues[col,row] == 11:
                    self.grids[0,col,row] = self.world.create_rectangle(row*cs.gridSize, col*cs.gridSize,(row+1)*cs.gridSize, (col+1)*cs.gridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

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
                if cs.mapValues[col,row] == 0:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif cs.mapValues[col,row] == 1:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif cs.mapValues[col,row] == 2:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif cs.mapValues[col,row] == 3:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif cs.mapValues[col,row] == 4:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif cs.mapValues[col,row] == 5:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif cs.mapValues[col,row] == 6:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif cs.mapValues[col,row] == 7:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif cs.mapValues[col,row] == 8:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif cs.mapValues[col,row] == 9:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif cs.mapValues[col,row] == 10:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif cs.mapValues[col,row] == 11:
                    self.grids[0,col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

        self.box[0] = self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1], fill="white", width = 2)
        self.box[1] = self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1],self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.box[2] =self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.box[3] =self.world.create_line(self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)

    def Zoom_in(self):
        self.subMenu.entryconfigure("Zoom in", state="disabled")
        self.subMenu.entryconfigure("Zoom out", state="normal")

        self.world.bind('<Button-1>', self.OnClick)
 

        self.world.bind('<Up>', self.Up)
        self.world.bind('<Down>', self.Down)
        self.world.bind('<Left>', self.Left)
        self.world.bind('<Right>', self.Right)
        self.world.focus_set()

        self.Zoom_in_init()

    def Zoom_in_init(self):
        self.world.delete("all")
        self.Minimap_fetch()
        self.Minimap_enlarge()
        self.Create_minimap()
        self.master.update()

    def Zoom_in_process(self):

        self.Minimap_fetch()
        self.Minimap_update()
        self.master.update()
        

    def Zoom_out(self):
        self.subMenu.entryconfigure("Zoom in", state="normal")
        self.subMenu.entryconfigure("Zoom out", state="disabled")

        self.world.bind('<Button-1>')

        self.world.unbind('<Up>')
        self.world.unbind('<Down>')
        self.world.unbind('<Left>')
        self.world.unbind('<Right>')

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
        self.master.update()
        
    def Minimap_update(self):
        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                if self.miniMapValues[col,row] == 0:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif self.miniMapValues[col,row] == 1:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif self.miniMapValues[col,row] == 2:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif self.miniMapValues[col,row] == 3:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif self.miniMapValues[col,row] == 4:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif self.miniMapValues[col,row] == 5:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif self.miniMapValues[col,row] == 6:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif self.miniMapValues[col,row] == 7:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif self.miniMapValues[col,row] == 8:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif self.miniMapValues[col,row] == 9:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif self.miniMapValues[col,row] == 10:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif self.miniMapValues[col,row] == 11:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

        self.world.coords(self.box[0], self.pin+self.miniLocation[1],self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0] )
        self.world.coords(self.box[1], self.pin+self.miniLocation[1],self.pin+self.miniLocation[0],self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize )
        self.world.coords(self.box[2], self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0]+cs.barSize)
        self.world.coords(self.box[3], self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0]+cs.barSize )


    def OnClick(self,event):
        v = (cs.mapSize - cs.miniMapSize)
        center = cs.barSize // 2
        vx =event.x-v-center
        vy =event.y-v-center

        if event.x >= v and event.y >= v: # if minimap is pressed
            if vx < 0:
                vx = 0
            if vx >= cs.miniMapSize - cs.barSize:
                vx = cs.miniMapSize - cs.barSize 
            if vy < 0:
                vy = 0
            if vy >= cs.miniMapSize - cs.barSize:
                vy = cs.miniMapSize - cs.barSize 
            
            self.miniLocation = [vy,vx]
        self.Zoom_in_process()

    def Up(self,event):
        self.miniLocation[0] -= 2
        self.Zoom_in_process()
    
    def Down(self,event):
        self.miniLocation[0] += 2
        self.Zoom_in_process()

    def Left(self,event):
        self.miniLocation[1] -= 2
        self.Zoom_in_process()
    
    def Right(self,event):
        self.miniLocation[1] += 2
        self.Zoom_in_process()


class Game(Map):

    def __init__(self,master,world,grids):
        self.master = master # Load the necessary values from the upper class, Map
        self.world = world
        self.grids = grids

        self.Game_init()


    def Game_init(self):
        self.Gen_layer()
        self.Gen_water()


    def Gen_layer(self): # Generates a null value to all of the second layer, the null value is 0
        for col in range(0,100):
            for row in range(0,100):
                self.grids[1,col,row] = 0


    def Gen_plant(self):
        pass

    def Spawn_plant(self):
        

    def Gen_water(self): # Locates the water value in second layer of grids based on first layer, the water value is 1
        for col in range(0,100):
            for row in range(0,100):
                if cs.mapValues[col,row] == 0 or cs.mapValues[col,row] == 1 or cs.mapValues[col,row] == 2 or cs.mapValues[col,row] == 3:
                    self.grids[1,col,row] = 1



def main():
    root = tk.Tk()
    
    set_printoptions(threshold=inf)

    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__": 
    main()
