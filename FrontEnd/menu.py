from tkinter import *
from tkinter import messagebox



def about():
    messagebox.showinfo('PythonGuides', 'Python Guides aims at providing best practical tutorials')

class TopMenu():
    def __init__(self, _topWindow, _app):
        self.app = _app
        self.topWindow = _topWindow
        self.menubar = Menu(self.topWindow)
        self.menuFile = Menu(self.menubar, tearoff=0) #tearoff=0/1?
        self.menuFile.add_command(label="New", command = self.new)
        self.menuFile.add_command(label="Open Config", command=self.app.data_file_stream.select_dir.on_press)
        self.menuFile.add_command(label="Save Config As", command=self.app.data_file_stream.save_button.on_press)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=self.topWindow.quit)
        self.menubar.add_cascade(label="File", menu=self.menuFile) 

        self.menuEdit = Menu(self.menubar, tearoff=0) #tearoff=0/1?
        self.menuEdit.add_command(label="Add Connector",command=self.app.connector_manager.add_connector)
        self.menuEdit.add_command(label="Del selected Connector",command=self.app.connector_manager.del_connector)
        self.menuEdit.add_separator()
        self.menuEdit.add_command(label="Preferences")
        self.menubar.add_cascade(label="Edit", menu=self.menuEdit) 

        self.menuAbout = Menu(self.menubar, tearoff=0) #tearoff=0/1?
        self.menuAbout.add_command(label="About", command=self.about)
        self.menuAbout.add_command(label="Help")
        self.menubar.add_cascade(label="?", menu=self.menuAbout)  

    def about(self):
        messagebox.showinfo("WiringTester","Svilippato da:\n\t-> Alessandro \
Ricci\ne-mail:\n\t-> ricci.alessandro.alberto@gmail.com\ndistribuito al \
link:\n\t-> https://github.com/RicciAlessandro/Tester ")

    def new(self):
        _input = messagebox.askyesno("ATTENZIONE",message="Sei sicuro di voler \
caricare una configurazione vuota?\nI progressi non salvati andranno persi.")
        print(_input)
        if _input:
            self.app.new_workspace()
    
if __name__ == "__main__":
    ws =Tk()
    ws.title("Python Guides")
    ws.geometry("300x250")
    menuIstance = TopMenu(ws, None) 
        
    ws.config(menu=menuIstance.menubar)
    ws.mainloop()
