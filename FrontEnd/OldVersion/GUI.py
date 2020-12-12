from tkinter import *
from tkinter import ttk
import csv

class App(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master

        self.nConn = 0
        self.nConnLabel = StringVar()
        self.nConnLabel.set('nConn = ' + str(self.nConn))
        self.connName = []
        self.labels5 = []
        self.connMatrix = []

        self.labelConnName = []
        
        self.frame1 = Frame(master,name="mainFrame",relief = GROOVE, bd =2, bg= "red")
        self.frame2 = Frame(master,name="buttonFrame",relief = GROOVE, bd =2, bg= "blue")
        self.frame3 = Frame(master,name="leftFrame",relief = GROOVE, bd =2, bg= "green")
        self.frame4 = Frame(master,name="bottomFrame",relief = GROOVE, bd =2, bg= "yellow")
        self.frame5 = Frame(self.frame3,name="labels",relief = GROOVE, bd =2,bg= "pink")
        self.frame6 = Frame(self.frame3,name="combobox",relief = GROOVE, bd =2,bg= "orange")

        self.frame1["width"]=530-20
        self.frame1["height"]=300
        self.frame2["width"]=50
        self.frame2["height"]=400
        self.frame3["width"]=520
        self.frame3["height"]=100
        self.frame4["width"]=20
        self.frame4["height"]=400
        
        self.frame1.place(x=20,y=0)
        self.frame2.place(x=550,y=0)
        self.frame3.place(x=0,y=300)
        self.frame4.place(x=0,y=0)
        self.frame5.pack(side=RIGHT)
        self.frame6.pack(side=RIGHT)
        
        self.button1 = Button(self.frame2,text = "Test Wire", command = self.testWire)
        self.button2 = Button(self.frame2,text = "Load DB", command = self.importConfig)
        self.button3 = Button(self.frame2,text = "Save DB", command = self.testWire)
        self.button4 = Button(self.frame2,text = "Add conn", command = self.addConn)
        self.button5 = Button(self.frame2,text = "Del conn", command = self.delConn)

        self.combobox1 = ttk.Combobox(self.frame5,values=self.connName)
        self.combobox2 = ttk.Combobox(self.frame6,values=self.connName)
        
        self.button1.pack(side=BOTTOM, fill='x')
        self.button2.pack(side=TOP,fill='x')
        self.button3.pack(side=TOP,fill='x')
        self.button4.pack(side=TOP,fill='x')
        self.button5.pack(side=TOP,fill='x')

        self.label2 = Label(self.frame5,text = "CONN-1:")
        self.label3 = Label(self.frame6,text = "CONN-2:")                        

        self.combobox1.pack(side=RIGHT)
        self.label2.pack(side=RIGHT)

        self.combobox2.pack(side=RIGHT)
        self.label3.pack(side=RIGHT)
        
        
        self.label1 = Label(self.frame3,textvariable = self.nConnLabel)
        self.label1.pack(side=LEFT)

        

        self.importConfig()
        self.importConnMatrix()

        
        
    def testWire(self):
        print("testing")

    def addConn(self):
        #
        #   aggiunge un connettore, quindi 
        #   aumenta nConn, chiede il nome e i pin, lo aggiunge alla combobox e 
        #
        #
        nop

    def delConn(self):
        nop
        
    def importConfig(self):
        print(self.connName)
        with open('DB/config.csv', newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=';', quotechar='|')
            rowList = list(rows)
            self.nConn = int(rowList[0][0])
            self.connName = rowList[1]
            self.combobox1["value"] = self.connName
            self.combobox2["value"] = self.connName
            
            self.nConnLabel.set('nConn = ' + str(self.nConn))
            
            self.plotLabels5()
                                    
            self.nPin = rowList[2]
            print(rowList)
            print(self.nConn)
            print(self.connName)

            for file in self.connName:
                print('DB/'+ file + '.csv')
                try:
                    with open('DB/'+ file + '.csv', newline='') as csvfile:
                        print('ok')
                except:
                    print('exception 001: can\'t open file')
                    #o una messagbox o crea il file
                    #proviamo a crearlo
                    try:
                        open('DB/'+ file + '.csv','w', newline='')
                    except:
                        print('exception 002: impossible to write')

    #def plotConnName(self):
    #    del self.labels5[:]
    #    print("222222222")
    #    print(self.nConn)
    #    for i in range(self.nConn):
    #        self.labels5.append( Label(self.frame5, textvariable = self.connNameLabels[i]))
    #        self.labels5[i].pack()

    def plotLabels5(self):
        ############################
        #       legge 
        #   cancella il vettore labels, e ne crea uno nuovo con i testi del vettore connName
        #
        ############################
        self.labels5 = []
        del self.labels5[:]
        for i in range(self.nConn):
            self.labels5.append(Label(self.frame3,text= self.connName[i]))
            self.labels5[i].pack()
            #name = StringVar()
            #name.set(self.connName[i])
            #self.connNameLabels.append(name)
            print("tutto ok")

    def importConnMatrix(self):
        print("")
              
        
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

