import json
import constants as cs
import tkinter as tk
from numpy import empty, set_printoptions, inf
from random import randint
import os

dirname, filename = os.path.split(os.path.abspath(__file__))
data = {}

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

        self.grids = empty([100,100], dtype=int) # the first layer will contain rectangle values as the ground itself, and second layer wil take the object image values of rabbit, carrot and fox
        self.object = empty([100,100], dtype=int) # array caontains the object values, 0 as none, 1 as water, 2 as plant, 3 as rabbit, 4 as fox
        
        self.zoom = False
        self.miniMapValues = empty([2,cs.zoomPix,cs.zoomPix], dtype=int) # the zoom in version of cs.mapValue
        self.miniGrids = empty([cs.zoomPix,cs.zoomPix], dtype=int) # the zoom in version of self.grids
        self.objectList = []
        self.miniLocation = [0,0] # 2 values locating the x and y value of zoom

        self.pin = cs.mapSize - cs.miniMapSize

        self.count = -1
        self.pressed = False

        self.box = empty([4], dtype=int)

        self.Image_init()

        self.Create_map()
        self.Create_menu()
        
        self.game = Game(self.master,self.world,self.object)

        self.Update_object()

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

        self.file = tk.Menu(self.menu)
        self.view = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Load",command=self.Load_file)
        self.file.add_command(label="Save",command=self.Save_file)
        self.file.add_command(label="Save and exit",command=self.Save_and_exit)

        self.menu.add_cascade(label="View", menu=self.view)
        self.view.add_command(label="Zoom in",command=self.Zoom_in)
        self.view.add_command(label="Zoom out",command=self.Zoom_out)
        self.view.entryconfigure("Zoom out", state="disabled")

    def Load_file(self):
        global data

        if self.zoom == True:
            self.Zoom_out()

        self.Clear_object()
        with open('{}\\data.json'.format(dirname)) as json_file:
            data = json.load(json_file)

        # Write the position to local grid
        for carrot in data['carrot']:
            self.object[carrot['y'],carrot['x']] = 2
        for meat in data['meat']:
            self.object[meat['y'],meat['x']] = 3
        #for rabbit in data['rabbit']:
        #    self.object[rabbit['y'],rabbit['x']] = 4
        #for fox in data['fox']:
        #    self.object[fox['y'],fox['x']] = 5

        self.Update_object()

    def Save_file(self):
        with open('{}\\data.json'.format(dirname), 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def Save_and_exit(self):
        print(self.object)

    def Create_minimap(self):
        for col in range (0,100): # Reads the grid colors and status
            for row in range (0,100):
                if cs.mapValues[col,row] == 0:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif cs.mapValues[col,row] == 1:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif cs.mapValues[col,row] == 2:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif cs.mapValues[col,row] == 3:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif cs.mapValues[col,row] == 4:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif cs.mapValues[col,row] == 5:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif cs.mapValues[col,row] == 6:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif cs.mapValues[col,row] == 7:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif cs.mapValues[col,row] == 8:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif cs.mapValues[col,row] == 9:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif cs.mapValues[col,row] == 10:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif cs.mapValues[col,row] == 11:
                    self.grids[col,row] = self.world.create_rectangle(self.pin+row*cs.miniGridSize, self.pin+col*cs.miniGridSize,self.pin+(row+1)*cs.miniGridSize, self.pin+(col+1)*cs.miniGridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))

        self.box[0] = self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1], fill="white", width = 2)
        self.box[1] = self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1],self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.box[2] =self.world.create_line(self.pin+self.miniLocation[0],self.pin+self.miniLocation[1]+cs.barSize,self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)
        self.box[3] =self.world.create_line(self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1],self.pin+self.miniLocation[0]+cs.barSize,self.pin+self.miniLocation[1]+cs.barSize, fill="white", width = 2)

    def Zoom_in(self):
        self.zoom = True
        self.view.entryconfigure("Zoom in", state="disabled")
        self.view.entryconfigure("Zoom out", state="normal")

        self.world.bind('<Button-1>', self.OnClick)
 

        self.world.bind('<Up>', self.Up)
        self.world.bind('<Down>', self.Down)
        self.world.bind('<Left>', self.Left)
        self.world.bind('<Right>', self.Right)
        self.world.focus_set()

        self.objectList = []
        self.Zoom_in_init()

    def Zoom_in_init(self):
        self.world.delete("all")
        self.Minimap_fetch()
        self.Minimap_enlarge()
        self.Create_minimap()
        self.Update_object_zoom()
        self.master.update()

    def Zoom_in_process(self):

        self.Minimap_fetch()
        self.Minimap_update()
        self.Update_object_zoom()
        self.master.update()
        
    def Zoom_out(self):
        self.zoom = False
        self.view.entryconfigure("Zoom in", state="normal")
        self.view.entryconfigure("Zoom out", state="disabled")

        self.world.bind('<Button-1>')

        self.world.unbind('<Up>')
        self.world.unbind('<Down>')
        self.world.unbind('<Left>')
        self.world.unbind('<Right>')

        self.objectList = []

        self.world.delete("all")
        self.Create_map()
        self.Update_object()

    def Minimap_fetch(self):
        while(len(self.objectList) != 0):
            self.world.delete(self.objectList.pop(0))


        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                self.miniMapValues[0,col,row] = cs.mapValues[self.miniLocation[0]+col,self.miniLocation[1]+row]  

        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                self.miniMapValues[1,col,row] = self.object[self.miniLocation[0]+col,self.miniLocation[1]+row] 

    def Minimap_enlarge(self):

        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                if self.miniMapValues[0,col,row] == 0:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif self.miniMapValues[0,col,row] == 1:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif self.miniMapValues[0,col,row] == 2:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif self.miniMapValues[0,col,row] == 3:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif self.miniMapValues[0,col,row] == 4:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif self.miniMapValues[0,col,row] == 5:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif self.miniMapValues[0,col,row] == 6:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif self.miniMapValues[0,col,row] == 7:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif self.miniMapValues[0,col,row] == 8:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif self.miniMapValues[0,col,row] == 9:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif self.miniMapValues[0,col,row] == 10:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif self.miniMapValues[0,col,row] == 11:
                    self.miniGrids[col,row] = self.world.create_rectangle(row*cs.zoomGridSize, col*cs.zoomGridSize,(row+1)*cs.zoomGridSize, (col+1)*cs.zoomGridSize, fill="{}".format(cs.mapColors[11]), outline="{}".format(cs.mapColors[11]))
        self.master.update()
        
    def Minimap_update(self):
        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                if self.miniMapValues[0,col,row] == 0:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[0]), outline="{}".format(cs.mapColors[0]))
                elif self.miniMapValues[0,col,row] == 1:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[1]), outline="{}".format(cs.mapColors[1]))
                elif self.miniMapValues[0,col,row] == 2:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[2]), outline="{}".format(cs.mapColors[2]))
                elif self.miniMapValues[0,col,row] == 3:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[3]), outline="{}".format(cs.mapColors[3]))
                elif self.miniMapValues[0,col,row] == 4:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[4]), outline="{}".format(cs.mapColors[4]))
                elif self.miniMapValues[0,col,row] == 5:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[5]), outline="{}".format(cs.mapColors[5]))
                elif self.miniMapValues[0,col,row] == 6:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[6]), outline="{}".format(cs.mapColors[6]))
                elif self.miniMapValues[0,col,row] == 7:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[7]), outline="{}".format(cs.mapColors[7]))
                elif self.miniMapValues[0,col,row] == 8:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[8]), outline="{}".format(cs.mapColors[8]))
                elif self.miniMapValues[0,col,row] == 9:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[9]), outline="{}".format(cs.mapColors[9]))
                elif self.miniMapValues[0,col,row] == 10:
                    self.world.itemconfig(self.miniGrids[col,row], fill="{}".format(cs.mapColors[10]), outline="{}".format(cs.mapColors[10]))
                elif self.miniMapValues[0,col,row] == 11:
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

    def Image_init(self):       
        resource = dirname + "\\resources"

        gif1 = tk.PhotoImage(file='{}//rabbit.png'.format(resource))
        gif1 = gif1.zoom(cs.zoomGridSize)
        gif1 = gif1.subsample(227)
        self.rabbit_big = gif1

        gif1 = tk.PhotoImage(file='{}//rabbit.png'.format(resource))
        gif1 = gif1.zoom(cs.gridSize)
        gif1 = gif1.subsample(227)
        self.rabbit_small = gif1

        gif2 = tk.PhotoImage(file='{}//fox.png'.format(resource))
        gif2 = gif2.zoom(cs.zoomGridSize)
        gif2 = gif2.subsample(289)
        self.fox_big = gif2

        gif2 = tk.PhotoImage(file='{}//fox.png'.format(resource))
        gif2 = gif2.zoom(cs.gridSize)
        gif2 = gif2.subsample(289)
        self.fox_small = gif2

        gif3 = tk.PhotoImage(file='{}//meat.png'.format(resource))
        gif3 = gif3.zoom(cs.zoomGridSize)
        gif3 = gif3.subsample(256)
        self.meat_big = gif3

        gif3 = tk.PhotoImage(file='{}//meat.png'.format(resource))
        gif3 = gif3.zoom(cs.gridSize)
        gif3 = gif3.subsample(256)
        self.meat_small = gif3

        gif4 = tk.PhotoImage(file='{}//carrot.png'.format(resource))
        gif4 = gif4.zoom(cs.zoomGridSize)
        gif4 = gif4.subsample(256)
        self.carrot_big = gif4

        gif4 = tk.PhotoImage(file='{}//carrot.png'.format(resource))
        gif4 = gif4.zoom(cs.gridSize)
        gif4 = gif4.subsample(256)
        self.carrot_small = gif4

    def Update_object(self):
        for col in range(0,100):
            for row in range(0,100):
                if self.object[col,row] == 2:
                    self.objectList.append(self.world.create_image(row*cs.gridSize+cs.imageAdjustSmall,col*cs.gridSize+cs.imageAdjustSmall,image=self.carrot_small))
                elif self.object[col,row] == 3:
                    self.objectList.append(self.world.create_image(row*cs.gridSize+cs.imageAdjustSmall,col*cs.gridSize+cs.imageAdjustSmall,image=self.meat_small))
                elif self.object[col,row] == 4:
                    self.objectList.append(self.world.create_image(row*cs.gridSize+cs.imageAdjustSmall,col*cs.gridSize+cs.imageAdjustSmall,image=self.rabbit_small))
                elif self.object[col,row] == 5:
                    self.objectList.append(self.world.create_image(row*cs.gridSize+cs.imageAdjustSmall,col*cs.gridSize+cs.imageAdjustSmall,image=self.fox_small))
        self.master.update()

    def Update_object_zoom(self):
        for col in range(0,cs.zoomPix):
            for row in range(0,cs.zoomPix):
                if self.miniMapValues[1,col,row] == 2:
                    self.objectList.append(self.world.create_image(row*cs.zoomGridSize+cs.imageAdjustBig,col*cs.zoomGridSize+cs.imageAdjustBig,image=self.carrot_big))
                elif self.object[col,row] == 3:
                    self.objectList.append(self.world.create_image(row*cs.zoomGridSize+cs.imageAdjustBig,col*cs.zoomGridSize+cs.imageAdjustBig,image=self.meat_big))
                elif self.miniMapValues[1,col,row] == 4:
                    self.objectList.append(self.world.create_image(row*cs.zoomGridSize+cs.imageAdjustBig,col*cs.zoomGridSize+cs.imageAdjustBig,image=self.rabbit_big))
                elif self.miniMapValues[1,col,row] == 5:
                    self.objectList.append(self.world.create_image(row*cs.zoomGridSize+cs.imageAdjustBig,col*cs.zoomGridSize+cs.imageAdjustBig,image=self.fox_big))

        self.master.update()

    def Delete_object(self,x,y):
        for i in range (0,len(data["carrot"])):
            if data["carrot"][i]["x"] == x and data["carrot"][i]["y"] == y:
                del data["carrot"][i]
                self.object[y][x] = 0
                return None
        for i in range (0,len(data["meat"])):
            if data["meat"][i]["x"] == x and data["meat"][i]["y"] == y:
                del data["meat"][i]
                self.object[y][x] = 0
                return None
        for i in range (0,len(data["rabbit"])):
            if data["rabbit"][i]["x"] == x and data["rabbit"][i]["y"] == y:
                del data["rabbit"][i]
                self.object[y][x] = 0
                return None
        for i in range (0,len(data["fox"])):
            if data["fox"][i]["x"] == x and data["fox"][i]["y"] == y:
                del data["fox"][i]
                self.object[y][x] = 0
                return None
        

    def Clear_object(self):
        for carrot in data["carrot"]:
            self.world.delete(self.objectList.pop(0))
            self.object[carrot["y"],carrot["x"]] = 0
        for meat in data["meat"]:
            self.world.delete(self.objectList.pop(0))
            self.object[meat["y"],meat["x"]] = 0
        for rabbit in data["rabbit"]:
            self.world.delete(self.objectList.pop(0))
            self.object[rabbit["y"],rabbit["x"]] = 0
        for fox in data["fox"]:
            self.world.delete(self.objectList.pop(0))
            self.object[fox["y"],fox["x"]] = 0
        NewData()







class Game(Map):

    def __init__(self,master,world,nObject):
        self.master = master # Load the necessary values from the upper class, Map
        self.world = world
        self.object = nObject

        self.Game_init()

    def Json_save_carrot(self,x,y,health):
        global data
        data['carrot'].append({
            'x': x,
            'y': y,
            'health': health
        })
    

    def Game_init(self):
        self.Gen_layer()
        self.Gen_water()
        self.Gen_carrot()

    def Gen_layer(self): # Generates a null value to all of object, 0 as null
        for col in range(0,100):
            for row in range(0,100):
                self.object[col,row] = 0

    
    def Gen_water(self): # Locates the water value the water value is 1
        for col in range(0,100):
            for row in range(0,100):
                if cs.mapValues[col,row] == 0 or cs.mapValues[col,row] == 1 or cs.mapValues[col,row] == 2 or cs.mapValues[col,row] == 3:
                    self.object[col,row] = 1


    def Gen_carrot(self):
        for i in range (0,10):
            self.Spawn_carrot()

    def Spawn_carrot(self):
        ranX = randint(0,99) # Generate a random number that is not taken and spawn a plant, the plant value is 2
        ranY = randint(0,99)   
        while self.object[ranY,ranX] != 0: # while the location is not null
            ranX = randint(0,99)
            ranY = randint(0,99)
        
        self.Json_save_carrot(ranX,ranY,100)

        self.object[ranY,ranX] = 2

def NewData():
    global data
    data = {} # Start a new data
    data['carrot'] = []
    data['meat'] = []
    data['rabbit'] = []
    data['fox'] = []

def main():
    root = tk.Tk()
    
    NewData()
    set_printoptions(threshold=inf)

    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__": 
    main()
