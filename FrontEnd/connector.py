import tkinter as tk
import tkinter.ttk as ttk

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
class ConnectorManager():
    def __init__(self, _app, _gui, _state ):
        self.app = _app
        self.gui = _gui
        self.state = _state
        self.parent_frame = self.gui.list_frame
        #self.state.connector_list = self.state.connector_list SE AGGIUNGO ELEMENTI FUNZIONA PERCHE' NON VIENE RI ASSEGNATO, MA SE FACCIO = NONE VIENE RI ASSEGNATO E QUESTA VARIABILE E QUELLA SU STATO FANNO RIFERIMENTO A OGGETTI DIVERSI
        #self.state.continuity = self.state.continuity
        #self.selected_connector_1 = self.state.selected_connector_1 UNA MODIFICA DI SELECTED CONNECTOR 1 NON PROVOCEREBBE UNA MODIFICA ALL'ATTRIBUTO DI STATE PERCHè SAREBBE UNA SEMPLICE RI ASSEGNAZIONE
        #self.selected_connector_2 = self.state.selected_connector_2 # selected connector deve essere sempre coerent -> None nei casi di implausibilità (lista vuota, connettore eliminato, connettore1 = connettore2)
        #ISTANCES TUTTA QUESTA ROBA POTREBBE ESSERE PORTATA NELLA CLASSE GUI PER POI ESSERE PASSATI PER RIFERIMENTO QUI SOLO I PULSANTI SENZA I METODI GRID
        self.label_conn_list = tk.Label(self.parent_frame, text="Lista connettori:")
        self.listbox_conn_list = tk.Listbox(self.parent_frame, selectmode = "SINGLE", exportselection=False)
        self.button_add_conn = tk.Button(self.parent_frame, text="ADD CONNECTOR", command=self.add_connector)
        self.button_del_conn = tk.Button(self.parent_frame, text="DEL CONNECTOR", command=self.del_connector)
        self.label_conn_2 = tk.Label(self.parent_frame, text="Connettore 2:")
        self.combobox_conn_2 = ttk.Combobox(self.parent_frame, values=["None"], postcommand=self.combobox_conn_2_update)
        self.connector_table = ConnectorTable(self.app, self.gui, self.state)
        #GRID METHODS
        self.label_conn_list.grid(row=0,column=0, padx=5, pady=1, sticky="WE")
        self.listbox_conn_list.grid(row=1,column=0, padx=5, pady=1, sticky="WE")
        self.label_conn_2.grid(row=2, column=0, sticky="WE")
        self.combobox_conn_2.grid(row=3, column=0, padx=5, pady=1, sticky="WE")
        self.button_add_conn.grid(row=4, column=0, sticky="WE")
        self.button_del_conn.grid(row=5, column=0, sticky="WE")
        
        #LISTBOX INIT
        self.listbox_conn_list.insert(0,"None")
        self.listbox_conn_list.bind("<<ListboxSelect>>", self.on_conn1_selection) # se non metto la proprietà exportselection a False ogni volta che 
        #COMBOBOX INIT
        self.combobox_conn_2.bind("<<ComboboxSelected>>",self.on_conn2_selection)
        self.combobox_conn_2.set("None")

    def update_selected_connectors(self):
        print("----update_selected_connectors----")
        self.update_selected_connector_1()
        self.update_selected_connector_2()

    
    def update_selected_connector_1(self):
        '''
        1) read the conn1 listbox
        2) if name selected is present in connector list, it update labels and connector1 selected
        3) if it isn't in the list it assign selected connetor to None and update the label
        '''
        print("----update_selected_connector1----")
        _listbox_selected = self.listbox_conn_list.get(self.listbox_conn_list.curselection())
        for c in self.state.connector_list:
            _c_name = c.get_name() 
            if _c_name == _listbox_selected:
                print("selected connector1 = "+ _c_name)
                self.state.set_selected_connector_1(c)
                if self.state.selected_connector_2 == self.state.selected_connector_1:
                    print("connettori selezionati uguali, connettore 2 viene settato a None")
                    self.state.set_selected_connector_2(None)
                    self.combobox_conn_2.set("None")
                    print("selected connector2 = None")
                self.connector_table.update()
                return
        self.state.set_selected_connector_1(None) #SE NON è RITORNATO SIGNIFICA CHE L'ELEMENTO SELEZIONATO NON ESISTE NELLA LISTA DEI CONNETTORI E QUINDI è STATO SELEZIONATO NONE
        self.listbox_conn_list.activate(tk.END) #QUESTO DOVREBBE SERVIRE QUANDO VIENE CANCELLATO UN ELEMENTO E RESTA UNA SELEZIONE AD UN ELEMENTO CHE NON ESISTE
        print("selected connector1 = None")
        self.connector_table.update()

    def update_selected_connector_2(self, eventObject=None):
        '''
        1) legge la combobox2 e se il connettore 2 selezionato è nella lista dei connettori e non è uguale al connettore 1 già selezionato, lo seleziona come conn2
        2) se la scelta di conn 2 non è valida seleziona None
        '''
        print("----update_selected_connector2----")
        _combobox_selected = self.combobox_conn_2.get()
        for c in self.state.connector_list:
            _c_name = c.get_name()
            if _combobox_selected == _c_name:  #così ho pescato l'istanza c selezionata dalla combobox
                #controllo validità dei _c_name
                if self.state.selected_connector_1 == None:
                    print("conn 2 != conn 1 (None) - OK")
                    print("selected connector2 = "+ _c_name)
                    self.state.set_selected_connector_2(c)
                    self.connector_table.update()
                    return
                elif _c_name == self.state.selected_connector_1.get_name():
                    print("connettore 2 selezionato uguale a connettore selezionato 1")
                else:
                    print("conn 2 != conn 1 - OK")
                    print("selected connector2 = "+ _c_name)
                    self.state.set_selected_connector_2(c)
                    self.connector_table.update()
                    return
            #else:
            #    print("selezionato connettore 2 None (nessun connettore nella lista connectors[] coincide con la combobox)")
        self.state.set_selected_connector_2(None)
        self.combobox_conn_2.set("None")
        #self.label_conn_name["text"] = "--"
        print("selected connector2 = None")
        self.connector_table.update()
        
    def render(self):
        self.app.render_grid_matrix()

    def on_conn1_selection(self,eventObject):
        '''
        when an element of the connector listbox is selected:
            1) if the name selected is present in the connector list update the selected connector label
            2) update the connector2 combobox with all the others connectors
            3) render grid matrix
        '''
        print("---- on_conn1_selection ----")
        self.update_selected_connectors()
        self.render()
    
    def on_conn2_selection(self,eventObject = None):
        '''
        when an element of the conn combobox is selected:
            1) if the name selected is present in the connector list update the selected connector label
            2) render grid matrix
        '''
        print("---- on_conn2_selection ----")
        self.update_selected_connector_2()
        self.render()
        
    def add_connector(self):
        self.frame = tk.Toplevel(self.gui.main_frame)
        self.frame.grab_set() #blocca la selezione su questo frame. @grab_release() or .withdraw()/.deiconify() per far comparire o scomparire
        self.frame.resizable(height=False, width=False)
        self.upper_frame = tk.Frame(self.frame)  #, bg ="blue"
        self.lower_frame = tk.Frame(self.frame)  #, bg = "red"
        self.upper_frame.grid(row=0, column=0, sticky="WE")
        self.lower_frame.grid(row=1, column=0, sticky="WE")
        
        #UPPER FRAME
        self.label_new_conn_name = tk.Label(self.upper_frame,text="Nome nuovo connettore: ")
        self.label_new_conn_name.grid(row=0,column=0,sticky="WE")
        self.entry_name = tk.Entry(self.upper_frame, textvariable = "inserisci n_pin_conn")
        self.entry_name.grid(row=0, column=1, padx=5, pady=1, sticky="WE")
        self.label_new_conn_n_pin = tk.Label(self.upper_frame,text="numero pin nuovo connettore: ")
        self.label_new_conn_n_pin.grid(row=1,column=0,sticky="WE")
        self.combobox_n_pin_new = ttk.Combobox(self.upper_frame, values=list(range(128)))
        self.combobox_n_pin_new.set("0")
        self.combobox_n_pin_new.grid(row=1, column=1, padx=5, pady=1, sticky="WE")
        #LOWER FRAME
        self.ok_btn = tk.Button(self.lower_frame, text = "Ok", command=self.ok_btn_add_connector)
        self.ok_btn.pack(side="right", fill="x",expand=True, padx=1, pady=2)#sticky="WE"
        # ok_btn.bind("<<Button-1>>", ok_btn_add_connector(self, msg_box))
        self.cancel_btn = tk.Button(self.lower_frame, text = "Cancel", command=self.cancel_btn_add_connector)
        #cancel_btn.bind("<<Button-1>>", cancel_btn_add_connector(self, msg_box))
        self.cancel_btn.pack(side="left", fill="x", expand=True, padx=1, pady=2)
        #self.cancel_btn.grid(row=0,column=0, padx=5, pady=1, sticky='nesw')
    
    def ok_btn_add_connector(self):
        '''
        when OK is pressed:
            1) read from entry fields and IF these fields are consistent
                2) create new connector
                3) add it to the top of the listbox
                4) destroy the popup window
                5) update available connector in combobox2 
        '''
        print("premuto ok")
        _text_input = (self.entry_name.get())
        print(_text_input)
        #controlli sull0input nome
        if _text_input == "":
            print("digita un nome valido")
            return
        if _text_input.isdigit():
            print("il nome del connettore non può essere un numero")
            return
        for _conn in self.state.connector_list:
            if _text_input == _conn.get_name():
                print("Nome connettore già esistente, digita un nome valido")
                return
        #controlli sull'input numerico
        _raw_input = self.combobox_n_pin_new.get() #ritorna sempre una stringa
        print(_raw_input)
        if _raw_input.isdigit():
            _int_input = int(self.combobox_n_pin_new.get())
            if _int_input < 1: #alla fine questo controlla solo se è zero, perchè i numeri float o negativi se inseriti dall'entry ritornano falso in isdigit()
                print("inserisci un numero di pin valido")
                return
        else:
            print("inserisci un numero di pin valido (intero)")
            return
        #procedi a creare il nuovo connettore
        _new_conn = Connector(_int_input,_text_input,1)
        self.state.connector_list.append(_new_conn)
        self.state.continuity[_new_conn.get_name()]={}
        #aggiungi il nuovo connettore al dizionario dei connettori
        for _conn in self.state.connector_list:
            if _conn.get_name() != _new_conn.get_name():
                self.state.continuity[_new_conn.get_name()][_conn.get_name()]=[]
                #_connection_matrix = [[3]*_conn.get_n_pin()]*_new_conn.get_n_pin()
                _connection_matrix = []
                for i in range(_new_conn.get_n_pin()):
                    _connection_matrix.append([])     
                    for j in range(_conn.get_n_pin()):
                        _connection_matrix[i].append(3)
                self.state.continuity[_new_conn.get_name()][_conn.get_name()] = _connection_matrix
        #aggiungi il dizionario che descrive il collegamento dei vecchi connettori al nuovo connettore
        for _conn in self.state.connector_list:
            if _conn.get_name() != _new_conn.get_name():
                #_connection_matrix = [[3]*_new_conn.get_n_pin()]*_conn.get_n_pin() # NO! QUESTO CREA UNA LISTA E n RIFERIMENTI ALLA STESSA LISTA, UNA MODIFICA DI UN ELEMENTO SI RIPERQUOTE SU TUTTI GLI ALTRI
                _connection_matrix = []
                for i in range(_conn.get_n_pin()):
                    _connection_matrix.append([])     
                    for j in range(_new_conn.get_n_pin()):
                        _connection_matrix[i].append(3)
                self.state.continuity[_conn.get_name()][_new_conn.get_name()] = _connection_matrix
        
        self.listbox_update()
        self.to_first_list_connectors()
        #self.listbox_conn_list.insert(0,_new_conn.get_name()) #volevo metterci END al posto di 0, ma non è definito
        #self.entry_name.destroy()
        #self.combobox_n_pin_new.destroy()
        self.frame.destroy()
        #self.combobox_conn_2_update()
    
     #questa andrà aggiunta alla classe listbox
    def listbox_clean(self):
        self.listbox_conn_list.delete(0,tk.END)
        self.listbox_conn_list.insert(0,"None")
        self.listbox_conn_list.activate(tk.END)

    def listbox_update(self):
        self.listbox_conn_list.delete(0,tk.END)
        self.listbox_conn_list.insert(0,"None")
        for _conn in self.state.connector_list:
            self.listbox_conn_list.insert(0,_conn.get_name())
        
    def to_none_selected_connectors(self):
        self.listbox_conn_list.select_set(tk.END)
        #devo richiamare update seleted connector1?
        self.combobox_conn_2.set("None")
        # devo richiamare update selected connector2
        self.update_selected_connectors()
    
    def to_first_list_connectors(self):
        self.listbox_conn_list.select_set(0)
        self.update_selected_connectors()

    def cancel_btn_add_connector(self):
        '''
        when CANCEL btn is pressed:
            1) destroy the popup window
        '''
        print("cancel btn pressed")
        self.frame.destroy() 
        #crea nuovo connettore, lo appende alla lista di connettori e alla listobox
    def del_connector(self):
        '''
        onClick del_connector:
            1) delete the element selected on the connetor listbox each in the listbox each in the list of the connectors
            2) update connector2 combobox
        '''
        print("start del")
        for c in self.state.connector_list:
            print(c.get_name())
        
        try:
            _idx = self.listbox_conn_list.curselection()[0]
            print(_idx)
        except:
            print("errore: elemento cancellato")
            print("end del")
            return
        try:
            print("a")
            _conn_del_name = self.state.connector_list[-_idx-1].get_name()
            print("deleting")
            print(_conn_del_name)
            print("a")
            del self.state.connector_list[-_idx-1]  #nella listbox gli ultimi inseriti sono gli indici verso lo zero, nella lista invece gli ultimi appesi sono quelli verso END
            print("a")
            del self.state.continuity[_conn_del_name]
            print("a")
            for _conn in self.state.connector_list:
                print(self.state.continuity)
                del self.state.continuity[_conn.get_name()][_conn_del_name]        
            print("a")
            ##qui forse posso mettere direttamente un update che mi ricostruisce tutta la lista
            #self.listbox_conn_list.delete(_idx)
            #print("a")
            self.listbox_update()
            self.to_none_selected_connectors()
           
            ##self.listbox_conn_list.ac##(TODO tk.END)
            #self.update_selected_connector_1()
            print("ok")
        except:
            print("errore: indice selezionato inesistente")
        print("end del")
        for c in self.state.connector_list:
            print(c.get_name())
    
    def combobox_conn_2_update(self, eventObject=None):
        print("----entered in combobox_conn_2_update()----")
        _conns = ["None"]
        for _conn in self.state.connector_list:
            _name = _conn.get_name()
            #non appende il connettore 1 già selezionato
            if self.state.selected_connector_1 == None:
                _conns.append(_name)
                print("name: "+_name)
            elif _name == self.state.selected_connector_1.get_name():
                print("name: "+_name)
            else:
                _conns.append(_name)
                print("name: "+_name)
        #aggiorna la combobox con tutti i connettori tranne l'1 già selezionato
        self.combobox_conn_2["values"] = _conns
    
    def update_all(self):
        self.listbox_update()
        self.connector_table.update()

class ConnectorTable():
    def __init__(self, _app, _gui, _state):
        self.app = _app
        self.gui = _gui
        self.state = _state
        self.parent_frame = self.gui.conn_table_frame
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
        if self.state.selected_connector_1:
            self.label_1_1.configure(text=self.state.selected_connector_1.get_name())
            self.label_2_1.configure(text=self.state.selected_connector_1.get_n_pin())
        else:
            self.label_1_1.configure(text=" -- ")
            self.label_2_1.configure(text=" -- ")
        if self.state.selected_connector_2:
            self.label_3_1.configure(text=self.state.selected_connector_2.get_name())
            self.label_4_1.configure(text=self.state.selected_connector_2.get_n_pin())
        else:
            self.label_3_1.configure(text=" -- ")
            self.label_4_1.configure(text=" -- ")    

    
