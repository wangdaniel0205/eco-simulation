
import tkinter as tk
#from numpy import array, empty

class MainAppliaction(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        



#class Map(object):
#    def __init__(self):
#        self.world = tk.Canvas(root, width=1000, height=1000, background="{}".format("#%02x%02x%02x" % (249,248,249)))
#        self.world.pack()




if __name__ == "__main__":
    root = tk.Tk()
    MainAppliaction(root).pack(side="top", fill="both", expand=True)
    root.mainloop()