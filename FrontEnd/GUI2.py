from tkinter import *
import csv

class App(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master

        self.frames = []
        #for loop per impostare i 4 frame
        for i in range(4):
            self.frames.append(Frame(master,name="frame" + str(i),relief = GROOVE, bd =2))
            self.frames[i].pack()
        #for loop per i pulsanti nel frame 2
        self.frames[2].buttons = []
        for i in range(3):
            self.frames[2].buttons.append(Button(self.frames[2],name="btn2_" + str(i),relief = GROOVE, bd =2))
            self.frames[2].buttons[i].pack()
        self.frames[0].config(
    







sizex = 600
sizey = 400
posx  = 0
posy  = 0

root = Tk()
root.title("wiring tester v 0.00")
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

#root.geometry('600x400')
app = App(root)

root.mainloop()
