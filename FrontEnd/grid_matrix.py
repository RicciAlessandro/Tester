import tkinter as tk
from connector import Connector
from tkinter import ttk
'''
qui il dubbio è:
    se io ora passo per riferimento la matrice di continuità, ed un'altra istanza la modifica, in automatico
    avrei le modifiche anche nell'attributo di questa classe, quindi dovrei richiamare solo il metodo render() indicando quali connettori devo visualizzare
'''
class GridMatrix():
    def __init__(self, _main_frame, _continuity = {}, _n_pin_1=0, _n_pin_2=0, _conn_1_name="--", _conn_2_name="--", _app=None):
        self.scroll_height = 800
        #self.scroll_width = 400
        self.app = _app
        self.main_frame = _main_frame #Container = {canvas[main_frame_2 (frame+upper_frame+left_frame)+myscrollbar]}
        self.main_frame_2 = tk.Frame(self.main_frame, relief = "flat",borderwidth=1)#, height=self.scroll_height, width=self.scroll_width ) #bg = "blue"
        self.myscrollbar = tk.Scrollbar(self.main_frame,orient="vertical")#,command=self.canvas.yview)
        self.myscrollbar2 = tk.Scrollbar(self.main_frame,orient="horizontal")
        self.canvas = tk.Canvas(self.main_frame_2, yscrollcommand=self.myscrollbar.set, xscrollcommand=self.myscrollbar2.set)#, height=self.scroll_height, width=self.scroll_width, relief = "flat",borderwidth=2) #bg = "green",
        self.canvas_1 = tk.Canvas(self.main_frame_2, yscrollcommand=self.myscrollbar.set, height=self.scroll_height, width=20, relief = "flat",borderwidth=2) # bg = "purple",
        self.canvas_2 = tk.Canvas(self.main_frame_2, xscrollcommand=self.myscrollbar2.set, height=20)#, width=self.scroll_width, relief = "flat",borderwidth=2) # bg = "white",
        self.main_frame.grid_columnconfigure(1,weight=1)
        self.main_frame_2.grid_columnconfigure(1,weight=1)
        self.canvas.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(1,weight=1)
        self.main_frame_2.grid_rowconfigure(1,weight=1)
        self.canvas.grid_rowconfigure(0,weight=1)
        #self.main_frame_2.grid_propagate(0)
        #self.canvas.grid_propagate(0)
        #self.canvas_1.grid_propagate(0)
        #self.canvas_2.grid_propagate(0)
        #self.main_frame_2.configure(height=1000,width=500)
        #self.main_frame_2.configure(yscrollcommand=self.myscrollbar.set)
        self.myscrollbar.config(command = self.scroll_y)
        self.myscrollbar2.config(command = self.scroll_x)
        self.frame = tk.Frame(self.canvas) # , bg = "pink"
        self.frame_pin_1 = tk.Frame(self.canvas_1) # , bg = "white"
        self.frame_pin_2 = tk.Frame(self.canvas_2) #, bg = "brown"
        self.upper_frame = tk.Frame(self.main_frame, relief = "flat",borderwidth=2) # , bg = "red"
        self.left_frame = tk.Frame(self.main_frame, relief = "flat",borderwidth=2) #, bg = "yellow"
        #
        self.frame.bind("<Configure>",self.myfunction)
        self.frame_pin_1.bind("<Configure>",self.myfunction_1)
        self.frame_pin_2.bind("<Configure>",self.myfunction_2)
        #self.btn_prova = tk.Button(self.frame_pin_2,text="ok")
        #self.btn_prova.pack()
        self.canvas.create_window((0,0),window=self.frame,anchor='nw') #devo usare questo altrimenti se uso pack() per self.frame non funzionano le scroll
        self.canvas_1.create_window((0,0),window=self.frame_pin_1,anchor='nw') #devo usare questo altrimenti se uso pack() per self.frame non funzionano le scroll
        self.canvas_2.create_window((0,0),window=self.frame_pin_2,anchor='nw') #devo usare questo altrimenti se uso pack() per self.frame non funzionano le scroll
        #self.canvas.configure(yscrollcommand=self.myscrollbar.set)

        #self.myfunction(None)
        self.main_frame_2.grid(row=1,column=1,sticky="we")
        '''
        self.canvas.pack(side="left", fill="both", expand=True)
        self.myscrollbar.pack(side="left",fill="y")'''
        '''self.canvas.grid(row=1,column=1)
        self.canvas_1.grid(row=1,column=0)
        self.canvas_2.grid(row=0,column=1)'''

        self.canvas.grid(row=1,column=1,sticky="nswe")
        self.canvas_1.grid(row=1,column=0,sticky="ns")
        self.canvas_2.grid(row=0,column=1,sticky="we")
        self.myscrollbar.grid(row=1,column=2, sticky="ns")
        self.myscrollbar2.grid(row=2,column=1, sticky="we")
        
        #self.continuity = {}
        self.continuity = _continuity
        self._n_pin_1 = _n_pin_1
        self._n_pin_2 = _n_pin_2
        self.conn_1_name = _conn_1_name
        self.conn_2_name = _conn_2_name
        self.rows = 50
        self.cols = 50
        self.left_frame.grid_rowconfigure(0,weight=1) #OK questo serve veramente a dare alla riga il 100% dello spazio e farla espandere, solo con stiky non si espandeva
        self.upper_frame.grid_columnconfigure(0,weight=1) #OK questo serve veramente a dare alla riga il 100% dello spazio e farla espandere, solo con stiky non si espandeva
        self.label_conn_1 = tk.Label(self.left_frame, text="CONNETTORE 1", wraplength=1, anchor="center")#, bg="blue")
        self.label_conn_2 = tk.Label(self.upper_frame, text="CONNETTORE 2")
        self.label_conn_1_name = tk.Label(self.left_frame, text=self.conn_1_name, wraplength=1, width=1)
        self.label_conn_2_name = tk.Label(self.upper_frame, text=self.conn_2_name, height=1)
        self.label_conn_2.grid(row=0,column=0, sticky = "we")
        self.label_conn_2_name.grid(row=1,column=0, sticky = "we")
        self.label_conn_1.grid(row=0,column=0, sticky = "ns")
        self.label_conn_1_name.grid(row=0,column=1, sticky = "ns") 
        self.left_frame.grid(row=1,column=0, sticky="ns")
        self.upper_frame.grid(row=0,column=1, sticky="ew")
        #self.label_conn_1_name.grid(row=1,column=0)
        #self.label_conn_2_name.grid(row=0,column=1)
        self.labels_pin_index_1 = []
        self.labels_pin_index_2 = []
        _bg="white"
        _relief="solid"
        for _row in range(self.rows):
            if _row == self._n_pin_1:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_1.append(tk.Label(self.frame_pin_1, text=str(_row+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,))
            self.labels_pin_index_1[_row].grid(row=_row+1, column=0, sticky="nsew")
        _bg="white"
        _relief="solid"
        for _col in range(self.cols):
            if _col == self._n_pin_2:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_2.append(tk.Label(self.frame_pin_2, text=str(_col+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,))
            self.labels_pin_index_2[_col].grid(row=0, column=_col+1)
        
        #riempimento label centro
        self.labels_list = []
        #se esiste la matrice di continuità
        if self.continuity: #se il dizionario non è vuoto
            if self.continuity[self.conn_1_name][self.conn_2_name]:    
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                if(self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]==1):    
                                    #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                    self.labels_list[_row].append(tk.Label(self.frame, text="x", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                                    self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                                elif(self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]==3):    
                                    self.labels_list[_row].append(tk.Label(self.frame, text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                                    self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                                else:
                                    self.labels_list[_row].append(tk.Label(self.frame, text=" ", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                                    self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                                self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
            else: # IN QUESTO CASE NON CI CAPITERA' MAI VISTO CHE LA MATRICE DI CONTINUITA' ORMAI VIENE CREATA CON IL CONNETTORE
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row].append(tk.Label(self.frame, text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                                self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                                self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        else: #ANCHE QUESTO NON VERRA' MAI IMPIEGATO PERCHè SIA IL DIZIONARIO CHE LA MATRICE DI CONTINUITA' VENGONO CREATE CON IL CONNETTORE #se il dizionario di continuità ancora non esiste, fai il render con le linee per i pin che sono compresi nel connettore e grigio altrove
            for _row in range(self.rows):
                #print("row= "+str(_row))
                self.labels_list.append([])
                if _row < self._n_pin_1:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        if _col < self._n_pin_2:
                            self.labels_list[_row].append(tk.Label(self.frame, text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                        else:
                            #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                else:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                        self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        #self.frame.grid(row=1,column=1)
        self.myfunction(None)
        #self.update_values(n_pin_1,n_pin_2,list(continuity.keys())[0],list(continuity.keys())[1],continuity)
        #self.render()
        '''
        #prova del metodo update
        self.continuity = continuity
        self._n_pin_1 = n_pin_1
        self._n_pin_2 = n_pin_2
        self.conn_1_name = list(continuity.keys())[0]
        self.conn_2_name = list(continuity.keys())[1]
        print("in sleep")
        self.render()
        print("rendered")
        '''


    def scroll_x(self, *args):
        print("scroll_x")
        self.canvas.xview(*args)
        self.canvas_1.xview(*args)
        self.canvas_2.xview(*args)
    
    def scroll_y(self,*args):
        print("scroll_y")
        self.canvas.yview(*args)
        self.canvas_1.yview(*args)
        self.canvas_2.yview(*args)

    def myfunction(self, event):
        print("myfunction")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))#,width=200,height=200)
    def myfunction_1(self, event):
            print("myfunction_1")
            self.canvas_1.configure(scrollregion=self.canvas_1.bbox("all"))#,width=200,height=200)
    def myfunction_2(self, event):
            print("myfunction_2")
            self.canvas_2.configure(scrollregion=self.canvas_2.bbox("all"))#,width=200,height=200)

    def update_values(self, _n_pin_1, _n_pin_2, _conn_1_name, _conn_2_name, _continuity = None):
        if _continuity:
            self.continuity = _continuity
        self.conn_1_name = _conn_1_name
        self.conn_2_name = _conn_2_name
        self._n_pin_1 = _n_pin_1
        self._n_pin_2 = _n_pin_2        

    def render(self):
        '''
        aggiorna la vista quando vengono cambiati i connettori selezionati
        DEVO PRIMA CAMBIARE NPIN1,NPIN2, NOMI DEI CONNETTORI E MATRICE DI CONTINUITA' E POI POSSO CHIAMARE QUESTO METODO
        '''
        self.label_conn_1_name.configure(text=self.conn_1_name, wraplength=1, width=1)
        self.label_conn_2_name.configure(text=self.conn_2_name, height=1)
        _bg="white"
        _relief="solid"
        for _row in range(self.rows):
            if _row == self._n_pin_1:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_1[_row].configure(text=str(_row+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_1[_row].grid(row=_row+1, column=0, sticky="nsew")
        _bg="white"
        _relief="solid"
        for _col in range(self.cols):
            if _col == self._n_pin_2:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_2[_col].configure(text=str(_col+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_2[_col].grid(row=0, column=_col+1)
       
        #se esiste la matrice di continuità
        if self.continuity: #se il dizionario non è vuoto
            if self.continuity[self.conn_1_name][self.conn_2_name]:    
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                if(self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]==1):    
                                    #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                    self.labels_list[_row][_col].configure(text="x", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                                elif(self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]==3):
                                    self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                else:
                                    self.labels_list[_row][_col].configure(text=" ", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="gray")
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="red")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
            else:  #se esistorno i connettori ma non esiste la matrice di continuità
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="yellow")
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="pink")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        else: #se il dizionario di continuità ancora non esiste, fai il render con le linee per i pin che sono compresi nel connettore e grigio altrove
            #print("OCCHIO CHE SONO ENTRATO IN UN FLUSSO STRANO: NON ESISTE IL DIZIONARIO DI CONTINUITA' O E' VUOTO MA ESISTONO GIA I CONNETTORI")
            for _row in range(self.rows):
                #print("row= "+str(_row))
                #self.labels_list.append([])
                if _row < self._n_pin_1:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        if _col < self._n_pin_2:
                            self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                        else:
                            #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="black")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                else:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg="green")
                        #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        #self.frame.grid(row=1,column=1)
        self.myfunction(None)

    def render_2(self):
        '''
        aggiorna la vista quando vengono cambiati i connettori selezionati
        DEVO PRIMA CAMBIARE NPIN1,NPIN2, NOMI DEI CONNETTORI E MATRICE DI CONTINUITA' E POI POSSO CHIAMARE QUESTO METODO
        '''
        print("render 2")
        #questo sarebbe l'update
        if self.app.selected_connector_1:
            _conn_1_name = self.app.selected_connector_1.get_name()
            _n_pin_1 = self.app.selected_connector_1.get_n_pin()
            #print("ok")
        else:
            _conn_1_name = "--"
            _n_pin_1 = 0
        if self.app.selected_connector_2:
            _conn_2_name = self.app.selected_connector_2.get_name()
            _n_pin_2 = self.app.selected_connector_2.get_n_pin()
            #print("ok")
        else:
            _conn_2_name = "--"
            _n_pin_2 = 0

        self.label_conn_1_name.configure(text=_conn_1_name, wraplength=1, width=1)
        self.label_conn_2_name.configure(text=_conn_2_name, height=1)
        _bg="white"
        _relief="solid"
        for _row in range(self.rows):
            if _row == _n_pin_1:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_1[_row].configure(text=str(_row+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_1[_row].grid(row=_row+1, column=0, sticky="nsew")
        _bg="white"
        _relief="solid"
        for _col in range(self.cols):
            if _col == _n_pin_2:
                _bg=self.frame.cget("bg")
                _relief="sunken"
            self.labels_pin_index_2[_col].configure(text=str(_col+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_2[_col].grid(row=0, column=_col+1)
       
        if _conn_1_name == "--" or _conn_2_name == "--":
            for _row in range(self.rows):
                for _col in range(self.cols):
                    self.labels_list[_row][_col].configure(text=" ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
            #se esiste la matrice di continuità
        elif self.app.continuity: #se il dizionario non è vuoto
            if self.app.continuity[_conn_1_name][_conn_2_name]:    
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < _n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < _n_pin_2:
                                if self.app.continuity[_conn_1_name][_conn_2_name][_row][_col]==1:    
                                    #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                    self.labels_list[_row][_col].configure(text="x", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                                elif self.app.continuity[_conn_1_name][_conn_2_name][_row][_col]==3:
                                    self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                else:
                                    self.labels_list[_row][_col].configure(text=" ", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
            else:  #se esistorno i connettori ma non esiste la matrice di continuità (lista dei valori)
                for _row in range(self.rows):
                    #print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < _n_pin_1:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            if _col < _n_pin_2:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            #print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        else: #se il dizionario di continuità ancora non esiste, fai il render con le linee per i pin che sono compresi nel connettore e grigio altrove
            for _row in range(self.rows):
                #print("row= "+str(_row))
                #self.labels_list.append([])
                if _row < _n_pin_1:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        if _col < _n_pin_2:
                            self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                        else:
                            #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                else:
                    for _col in range(self.cols):
                        #print("col= "+str(_col))
                        self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, bg=self.frame.cget("bg"))
                        #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        #self.frame.grid(row=1,column=1)
        self.myfunction(None)

if __name__ == "__main__":
    main_frame = tk.Tk()
    #main_frame.geometry("100x100")
    n_pin_1 = 2
    n_pin_2 = 3
    n_pin_3 = 4
    #la lista di liste [n_pin_1][n_pin_2] mi è ritornata dall'automatic tester
    #gli associo una chiave conn2 e ho creato un dizionario
    #poi dovrei creare un dizionario che come chiavi ha tutti i connettori e associo la chiave conn1 al dizionatrio contnuty conn_1
    continuity_conn_1 = {"conn2":[[1,0,0],[0,1,0]],"conn3":[[0,0,1,0],[0,0,0,1]]}
    continuity_conn_2 = {"conn1":[[1,0],[0,1],[0,0]],"conn3":[[1,0,0,0],[0,0,0,0],[0,0,0,0]]}
    continuity_conn_3 = {"conn1":[[0,0],[0,0],[1,0],[0,1]],"conn2":[[0,1,0],[0,0,0],[0,0,0],[0,0,0]]}

    continuity = {"conn1":continuity_conn_1,"conn2":continuity_conn_2,"conn3":continuity_conn_3}

    print(continuity_conn_1["conn2"])
    print(type(continuity_conn_1["conn2"]))
    print(continuity_conn_1["conn2"][0])
    print(type(continuity_conn_1["conn2"][0]))
    print(continuity_conn_1["conn2"][0][0])
    print(type(continuity_conn_1["conn2"][0][0]))

    continuity_conn_1_2 = {"conn2":[],"conn3":[]}
    continuity_conn_2_2 = {"conn1":[],"conn3":[]}
    continuity_conn_3_2 = {"conn1":[],"conn2":[]}

    continuity_2 = {"conn1":continuity_conn_1_2,"conn2":continuity_conn_2_2,"conn3":continuity_conn_3_2}
    
    continuity_3 = {}

    #grid_matrix = GridMatrix(main_frame, continuity_3, n_pin_1,n_pin_2, list(continuity.keys())[0], list(continuity.keys())[1])
    grid_matrix = GridMatrix(main_frame)
 
    main_frame.mainloop()