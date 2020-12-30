import tkinter as tk
'''
qui il dubbio è:
    se io ora passo per riferimento la matrice di continuità, ed un'altra istanza la modifica, in automatico
    avrei le modifiche anche nell'attributo di questa classe, quindi dovrei richiamare solo il metodo render() indicando quali connettori devo visualizzare
'''
class GridMatrix():
    def __init__(self, _main_frame, _continuity = {}, _n_pin_1=0, _n_pin_2=0, _conn_1_name=" -- ", _conn_2_name=" --"):
        self.main_frame = _main_frame
        self.frame = tk.Frame(self.main_frame)
        self.upper_frame = tk.Frame(self.main_frame)
        self.left_frame = tk.Frame(self.main_frame)
        #self.continuity = {}
        self.continuity = _continuity
        self._n_pin_1 = _n_pin_1
        self._n_pin_2 = _n_pin_2
        self.conn_1_name = _conn_1_name
        self.conn_2_name = _conn_2_name
        self.rows = 10
        self.cols = 15
        self.label_conn_1 = tk.Label(self.left_frame, text="CONNETTORE 1", wraplength=1)
        self.label_conn_2 = tk.Label(self.upper_frame, text="CONNETTORE 2")
        self.label_conn_1_name = tk.Label(self.left_frame, text=self.conn_1_name, wraplength=1, width=1)
        self.label_conn_2_name = tk.Label(self.upper_frame, text=self.conn_2_name, height=1)
        self.label_conn_2.grid(row=0,column=0)
        self.label_conn_2_name.grid(row=1,column=0)
        self.label_conn_1.grid(row=0,column=0)
        self.label_conn_1_name.grid(row=0,column=1) 
        self.left_frame.grid(row=1,column=0)
        self.upper_frame.grid(row=0,column=1)
        #self.label_conn_1_name.grid(row=1,column=0)
        #self.label_conn_2_name.grid(row=0,column=1)
        self.labels_pin_index_1 = []
        self.labels_pin_index_2 = []
        _bg="white"
        _relief="solid"
        for _row in range(self.rows):
            if _row == self._n_pin_1:
                _bg=None
                _relief="sunken"
            self.labels_pin_index_1.append(tk.Label(self.frame, text=str(_row+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,))
            self.labels_pin_index_1[_row].grid(row=_row+1, column=0, sticky="nsew")
        _bg="white"
        _relief="solid"
        for _col in range(self.cols):
            if _col == self._n_pin_2:
                _bg=None
                _relief="sunken"
            self.labels_pin_index_2.append(tk.Label(self.frame, text=str(_col+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,))
            self.labels_pin_index_2[_col].grid(row=0, column=_col+1)
        
        #riempimento label centro
        self.labels_list = []
        #se esiste la matrice di continuità
        if self.continuity: #se il dizionario non è vuoto
            if self.continuity[self.conn_1_name][self.conn_2_name]:    
                for _row in range(self.rows):
                    print("row= "+str(_row))
                    self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                if self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]:    
                                    #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                    self.labels_list[_row].append(tk.Label(self.frame, text="x", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
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
                            print("col= "+str(_col))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
            else:
                for _row in range(self.rows):
                    print("row= "+str(_row))
                    self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
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
                            print("col= "+str(_col))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        else: #se il dizionario di continuità ancora non esiste, fai il render con le linee per i pin che sono compresi nel connettore e grigio altrove
            for _row in range(self.rows):
                print("row= "+str(_row))
                self.labels_list.append([])
                if _row < self._n_pin_1:
                    for _col in range(self.cols):
                        print("col= "+str(_col))
                        if _col < self._n_pin_2:
                            self.labels_list[_row].append(tk.Label(self.frame, text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white"))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                        else:
                            #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                            self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                            self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                else:
                    for _col in range(self.cols):
                        print("col= "+str(_col))
                        self.labels_list[_row].append(tk.Label(self.frame,text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER))
                        self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        self.frame.grid(row=1,column=1)
        self.update_values(n_pin_1,n_pin_2,list(continuity.keys())[0],list(continuity.keys())[1],continuity)
        self.render()
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
                _bg=None
                _relief="sunken"
            self.labels_pin_index_1[_row].configure(text=str(_row+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_1[_row].grid(row=_row+1, column=0, sticky="nsew")
        _bg="white"
        _relief="solid"
        for _col in range(self.cols):
            if _col == self._n_pin_2:
                _bg=None
                _relief="sunken"
            self.labels_pin_index_2[_col].configure(text=str(_col+1),  borderwidth=1, relief=_relief, bg=_bg, width=2, height=1,)
            #self.labels_pin_index_2[_col].grid(row=0, column=_col+1)
       
        #se esiste la matrice di continuità
        if self.continuity: #se il dizionario non è vuoto
            if self.continuity[self.conn_1_name][self.conn_2_name]:    
                for _row in range(self.rows):
                    print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                if self.continuity[self.conn_1_name][self.conn_2_name][_row][_col]:    
                                    #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                    self.labels_list[_row][_col].configure(text="x", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                                else:
                                    self.labels_list[_row][_col].configure(text=" ", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                    #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
            else:  #se esistorno i connettori ma non esiste la matrice di continuità
                for _row in range(self.rows):
                    print("row= "+str(_row))
                    #self.labels_list.append([])
                    if _row < self._n_pin_1:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
                            if _col < self._n_pin_2:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                            else:
                                #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                                self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                                #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                    else:
                        for _col in range(self.cols):
                            print("col= "+str(_col))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        else: #se il dizionario di continuità ancora non esiste, fai il render con le linee per i pin che sono compresi nel connettore e grigio altrove
            for _row in range(self.rows):
                print("row= "+str(_row))
                #self.labels_list.append([])
                if _row < self._n_pin_1:
                    for _col in range(self.cols):
                        print("col= "+str(_col))
                        if _col < self._n_pin_2:
                            self.labels_list[_row][_col].configure(text="-", borderwidth=1, relief="solid", width=2, height=1, bg="white")
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                        else:
                            #self.labels_list[_row].append(tk.Label(self.frame, text=str(_row)+"-"+str(_col), borderwidth=1, relief="ridge", width=2, height=1))
                            self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                            #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
                else:
                    for _col in range(self.cols):
                        print("col= "+str(_col))
                        self.labels_list[_row][_col].configure(text= " ", borderwidth=1, relief="sunken", width=2, height=1, anchor=tk.CENTER)
                        #self.labels_list[_row][_col].grid(row=_row+1, column=_col+1, sticky="NSWE")
        self.frame.grid(row=1,column=1)

if __name__ == "__main__":
    main_frame = tk.Tk()
    
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