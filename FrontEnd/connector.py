import tkinter as tk

class Connector():
    '''
    Connettore 
    '''
    #costruttore
    def __init__(self, _nPin = 0, _name = "", _index = 0):
        self.__n_pin = _nPin
        self.__name = _name
        self.__index = _index

    def get_n_pin(self):
        return self.__n_pin
    def get_name(self):
        return self.__name
    def get_index(self):
        return self.__index
    '''
    __n_pin = 0 
    __name = ""
    __index = 0
    '''

class ConnectorTable():
    def __init__(self,_parent_frame, _app = None):
        self.app = _app
        self.parent_frame = _parent_frame
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.configure(pady=2,padx=2,relief="raised",borderwidth=1)
        self.frame_conn_1 = tk.Frame(self.parent_frame,relief="sunken",borderwidth=1)
        self.frame_conn_2 = tk.Frame(self.parent_frame,relief="sunken",borderwidth=1)
        self.frame_conn_1.grid_columnconfigure(1, weight=1) #necessario per far agire lo sticky, non ho dato un peso alla colonna 0 cosi si espande solo la 1
        self.frame_conn_2.grid_columnconfigure(1, weight=1)
        self.label_1  = tk.Label(self.frame_conn_1, text="CONN 1: ", anchor = "w", justify = "left")
        self.label_1_1  = tk.Label(self.frame_conn_1, text=" -- ", height = 1, width = 20)
        self.label_2  = tk.Label(self.frame_conn_1, text="N PIN 1:", anchor = "w")
        self.label_2_1  = tk.Label(self.frame_conn_1, text=" -- ", height = 1, width = 20)
        self.label_3  = tk.Label(self.frame_conn_2, text="CONN 2", anchor = "w")
        self.label_3_1  = tk.Label(self.frame_conn_2, text=" -- ", height = 1, width = 20)
        self.label_4  = tk.Label(self.frame_conn_2, text="N PIN 2", anchor = "w")
        self.label_4_1  = tk.Label(self.frame_conn_2, text=" -- ", height = 1, width = 20)
        self.grid_items()

    def grid_items(self):
        self.frame_conn_1.grid(sticky="ew")
        self.frame_conn_2.grid(sticky="ew")   #sticky significa raggiungi la stessa espansione che ha raggiunto l'elemento dello stesso livello griddato isieme a lui, altrimenti si trova allineato al centro di questo con bordi più corti

        self.label_1.grid(row=0,column=0)
        self.label_1_1.grid(row=0,column=1,sticky="ew")
        self.label_2.grid(row=1,column=0)
        self.label_2_1.grid(row=1,column=1,sticky="ew")
        self.label_3.grid(row=2,column=0)
        self.label_3_1.grid(row=2,column=1,sticky="ew")
        self.label_4.grid(row=3,column=0)
        self.label_4_1.grid(row=3,column=1,sticky="ew")
    
    def update(self):
        print("update connector_table")
        if self.app.selected_connector_1:
            self.label_1_1.configure(text=self.app.selected_connector_1.get_name())
            self.label_2_1.configure(text=self.app.selected_connector_1.get_n_pin())
        else:
            self.label_1_1.configure(text=" -- ")
            self.label_2_1.configure(text=" -- ")
        if self.app.selected_connector_2:
            self.label_3_1.configure(text=self.app.selected_connector_2.get_name())
            self.label_4_1.configure(text=self.app.selected_connector_2.get_n_pin())
        else:
            self.label_3_1.configure(text=" -- ")
            self.label_4_1.configure(text=" -- ")    

class ConnectorManager():
    '''
    gestore di più istanze connettore e delle matrici di collegamento tra i connettori
    '''
    def __init__(self):
        self.__conns = []
        pass
    def load_connector(self):
        pass
    def save_connector(self):
        pass
    def add_connector(self):
        pass
    def del_connector(self):
        pass


    
