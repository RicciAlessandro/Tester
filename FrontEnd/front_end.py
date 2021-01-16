import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from connector import *
from grid_matrix import *
from data_file_stream import *
from serial_manager import *
#import connector
      
class Front_End():
    def __init__(self):
        #METODI PER LA CONFIGURAZIONE DELLA FINESTRA principale
        self.version = 0.01
        self.main_frame = tk.Tk()
        self.__init__main_frame()
        self.left_1_frame = tk.Frame(self.main_frame)# relief = "raised", borderwidth=1,padx=2,pady=1) #bg = "pink")
        self.left_1_frame.grid_columnconfigure(0,weight=1)
        self.left_2_frame = tk.Frame(self.main_frame)#, relief = "raised", borderwidth=1,padx=2,pady=1) # bg = "green")
        self.frame_serial_dash = tk.Frame(self.left_1_frame, relief = "ridge", borderwidth = 4, padx = 2, pady = 1)# bg = "black")
        self.frame_serial_command = tk.Frame(self.left_2_frame, bg = "blue")
        self.frame_IO = tk.Frame(self.left_1_frame, relief = "flat", borderwidth = 4, padx = 2, pady = 1) #, bg="red", relief = "raised", borderwidth=1,
        self.debug = True
        self.connectors = []
        self.continuity = {}
        self.selected_connector_1 = None
        self.selected_connector_2 = None # selected connector deve essere sempre coerent -> None nei casi di implausibilità (lista vuota, connettore eliminato, connettore1 = connettore2)
        
        self.row_index = 0
        self.col_index = 0
        
        self.serial_manager = SerialManager(self.frame_serial_dash, self.frame_serial_command,self, self.connectors)
        self.frame_serial_dash.grid(row=0, column=0, padx=0, pady=1) # sticky="we")
        self.frame_serial_command.grid(row=10, column=0, padx=5, pady=1, sticky="we")
        self.serial_manager.disable_commands()
        self.row_index += 1
        #LISTA CONNETTORI
        self.list_frame = tk.Frame(self.left_1_frame, relief = "ridge", borderwidth = 4, padx = 2, pady = 2)
        self.list_frame.grid_columnconfigure(0,weight=1)
        self.list_frame.grid(sticky="we")
        self.label_conn_list = tk.Label(self.list_frame, text="Lista connettori:")
        self.label_conn_list.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.row_index+=1
        self.listbox_conn_list = tk.Listbox(self.list_frame, selectmode = "SINGLE", exportselection=False)
        self.listbox_conn_list.insert(0,"None")
        self.listbox_conn_list.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.listbox_conn_list.bind("<<ListboxSelect>>", self.on_conn1_selection) # se non metto la proprietà exportselection a False ogni volta che 
        self.row_index+=1
        #AGGIUNGI, ELIMINA CONNETTORE
        self.button_add_conn = tk.Button(self.list_frame, text="ADD CONNECTOR", command=self.add_connector)
        self.button_del_conn = tk.Button(self.list_frame, text="DEL CONNECTOR", command=self.del_connector)
        self.button_add_conn.grid(row=5, column=0, sticky="WE")
        self.row_index+=1
        self.button_del_conn.grid(row=6, column=0, sticky="WE")
        self.row_index+=1
        self.data_file_stream = DataFileStream(self.frame_IO, self) # self.continuity
        self.frame_IO.grid(row=self.row_index, column=0, sticky="WE")
        #COL2
        self.connectors_frame = tk.Frame(self.left_2_frame)
        self.connector_table = ConnectorTable(self.connectors_frame, self)
        self.connectors_frame.grid(row=10,column=0)
        self.row_index = 0
        #self.col_index = 1
        #connettore1
        #self.label_conn = tk.Label(self.left_2_frame, text="Connettore selezionato:")
        #self.label_conn.grid(row=self.row_index, column=self.col_index, sticky="WE")
        #self.row_index+=1
        #self.label_conn_name = tk.Label(self.left_2_frame, text="--")
        #self.label_conn_name.grid(row=self.row_index, column=self.col_index, sticky="WE")
        #self.row_index+=1
        #self.label_n_pin_con_1 = tk.Label(self.left_2_frame, text="n pin conn: -- ")
        #self.label_n_pin_con_1.grid(row=self.row_index, column=self.col_index, sticky="WE")
        #self.row_index+=1
        #connettore2
        self.label_conn_2 = tk.Label(self.list_frame, text="Connettore 2:")
        self.label_conn_2.grid(row=3, column=0, sticky="WE")
        #self.row_index+=1
        self.combobox_conn_2 = ttk.Combobox(self.list_frame, values=["None"], postcommand=self.combobox_conn_2_update)
        self.combobox_conn_2.bind("<<ComboboxSelected>>",self.update_selected_connector_2)
        self.combobox_conn_2.set("None")
        self.combobox_conn_2.grid(row=4, column=0, padx=5, pady=1, sticky="WE")
        #self.combobox_conn_2.bind("<<ComboboxSelected>>", self.combobox_conn_2_update)
        self.row_index+=1
        self.grid_matrix_frame = tk.Frame(self.main_frame, relief = "ridge", borderwidth=3)
        self.grid_matrix = GridMatrix(self.grid_matrix_frame, self.continuity, 0, 0, "--", "--", self)
        self.row_index = 0
        self.col_index += 1
        self.left_1_frame.grid(row=0, column=0, sticky="nwe")
        self.left_2_frame.grid(row=0, column=1, sticky="n")
        self.grid_matrix_frame.grid(row=0, column=2, sticky="n")

        if self.debug:
            self.btn_print_cont = tk.Button(self.left_1_frame, text="print cont", command=self.print_cont)
            self.btn_print_cont.grid()

            self.btn_render = tk.Button(self.left_1_frame, text="render", command=self.grid_matrix.render_2)
            self.btn_render.grid()
        
    def print_cont(self):
        self.data_file_stream.app.connector_table.update()
        print("continuity 1: \n", self.continuity)
        print("connectors: \n" , self.connectors)
        _conn_name = []
        for k in self.connectors:
            _conn_name.append(k.get_name())
        print("connectors name: \n" , _conn_name) 
        print("selected connector 1: ", self.selected_connector_1)
        print("selected connector 2: ", self.selected_connector_2)
        if self.selected_connector_1:
            print("selected connector 1 name: ", self.selected_connector_1.get_name())
        else:
            print("selected connector 1 name: --")
        if self.selected_connector_2:
            print("selected connector 2 name: ", self.selected_connector_2.get_name())
        else:
            print("selected connector 2 name: --")
    
    def __init__main_frame(self):
        self.main_frame.geometry("800x500")
        self.main_frame.title("Wiring Tester V"+ str(self.version))
        self.main_frame.resizable(height=False, width=False)
    
    def update_selected_connectors(self):
        '''
        1)update selected connector_1
        2)update selected connector_2
        '''
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
        for c in self.connectors:
            _c_name = c.get_name() 
            if _c_name == _listbox_selected:
                print("selected connector1 = "+ _c_name)
                self.selected_connector_1 = c
                #self.label_conn_name["text"] = _c_name
                #self.label_n_pin_con_1["text"] = "n pin conn: "+str(c.get_n_pin())
                if self.selected_connector_2 == self.selected_connector_1:
                    print("connettori selezionati uguali, connettore 2 viene settato a None")
                    self.selected_connector_2 == None
                    self.combobox_conn_2.set("None")
                    print("selected connector2 = None")
                self.connector_table.update()
                return
        self.selected_connector_1 = None
        self.listbox_conn_list.activate(tk.END)
        #self.label_conn_name["text"] = "--"
        #self.label_n_pin_con_1["text"] = "n pin conn: -- "
        print("selected connector1 = None")
        self.connector_table.update()
        self.grid_matrix.render_2()

    def update_selected_connector_2(self, eventObject=None):
        '''
        1) legge la combobox2 e se il connettore 2 selezionato è nella lista dei connettori e non è uguale al connettore 1 già selezionato, lo seleziona come conn2
        2) se la scelta di conn 2 non è valida seleziona None
        '''
        print("----update_selected_connector2----")
        _combobox_selected = self.combobox_conn_2.get()
        for c in self.connectors:
            _c_name = c.get_name()
            if _combobox_selected == _c_name:  #così ho pescato l'istanza c selezionata dalla combobox
                #controllo validità dei _c_name
                if self.selected_connector_1 == None:
                    print("conn 2 != conn 1 (None) - OK")
                    print("selected connector2 = "+ _c_name)
                    self.selected_connector_2 = c
                    self.grid_matrix.render_2()
                    self.connector_table.update()
                    return
                elif _c_name == self.selected_connector_1.get_name():
                    print("connettore 2 selezionato uguale a connettore selezionato 1")
                else:
                    print("conn 2 != conn 1 - OK")
                    print("selected connector2 = "+ _c_name)
                    self.selected_connector_2 = c
                    self.grid_matrix.render_2()
                    self.connector_table.update()
                    return
            #else:
            #    print("selezionato connettore 2 None (nessun connettore nella lista connectors[] coincide con la combobox)")
        self.selected_connector_2 = None
        self.combobox_conn_2.set("None")
        #self.label_conn_name["text"] = "--"
        print("selected connector2 = None")
        self.grid_matrix.render_2()
        self.connector_table.update()

    
    

    def on_conn1_selection(self,eventObject):
        '''
        when an element of the connector listbox is selected:
            1) if the name selected is present in the connector list update the selected connector label
            2) update the connector2 combobox with all the others connectors
        '''

        print("---- on_conn1_selection ----")
        self.update_selected_connector_1()
        self.update_selected_connector_2()

    def add_connector(self):
        self.frame = tk.Toplevel(self.main_frame)
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
        for _conn in self.connectors:
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
        self.connectors.append(_new_conn)
        self.continuity[_new_conn.get_name()]={}
        #aggiungi il nuovo connettore al dizionario dei connettori
        for _conn in self.connectors:
            if _conn.get_name() != _new_conn.get_name():
                self.continuity[_new_conn.get_name()][_conn.get_name()]=[]
                #_connection_matrix = [[3]*_conn.get_n_pin()]*_new_conn.get_n_pin()
                _connection_matrix = []
                for i in range(_new_conn.get_n_pin()):
                    _connection_matrix.append([])     
                    for j in range(_conn.get_n_pin()):
                        _connection_matrix[i].append(3)
                self.continuity[_new_conn.get_name()][_conn.get_name()] = _connection_matrix
        #aggiungi il dizionario che descrive il collegamento dei vecchi connettori al nuovo connettore
        for _conn in self.connectors:
            if _conn.get_name() != _new_conn.get_name():
                #_connection_matrix = [[3]*_new_conn.get_n_pin()]*_conn.get_n_pin() # NO! QUESTO CREA UNA LISTA E n RIFERIMENTI ALLA STESSA LISTA, UNA MODIFICA DI UN ELEMENTO SI RIPERQUOTE SU TUTTI GLI ALTRI
                _connection_matrix = []
                for i in range(_conn.get_n_pin()):
                    _connection_matrix.append([])     
                    for j in range(_new_conn.get_n_pin()):
                        _connection_matrix[i].append(3)
                self.continuity[_conn.get_name()][_new_conn.get_name()] = _connection_matrix
                
        self.listbox_conn_list.insert(0,_new_conn.get_name()) #volevo metterci END al posto di 0, ma non è definito
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
        for _conn in self.connectors:
            self.listbox_conn_list.insert(0,_conn.get_name())
        
    def to_none_selected_connectors(self):
        #self.selected_connector_1 = None
        #self.selected_connector_2 = None
        self.listbox_conn_list.select_set(tk.END)
        #devo richiamare update seleted connector1?
        self.combobox_conn_2.set("None")
        # devo richiamare update selected connector2
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
        for c in self.connectors:
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
            _conn_del_name = self.connectors[-_idx-1].get_name()
            print("deleting")
            print(_conn_del_name)
            print("a")
            del self.connectors[-_idx-1]  #nella listbox gli ultimi inseriti sono gli indici verso lo zero, nella lista invece gli ultimi appesi sono quelli verso END
            print("a")
            del self.continuity[_conn_del_name]
            print("a")
            for _conn in self.connectors:
                print(self.continuity)
                del self.continuity[_conn.get_name()][_conn_del_name]        
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
        for c in self.connectors:
            print(c.get_name())

        
        
    """ #self.combobox_conn_2_update()
    def connect_to_HW(self):
        _port = self.combobox_serial_port.get()
        print(_port)
        if _port == "None":
            print("seleziona una porta seriale valida")
        else:
            #va inserito un blocco try except con la gestione degli errori.
            if not(self.ser.is_open): # Establish the connection on a specific port
                if _port in self.get_serial_ports():
                    print("connessione in corso")
                    self.ser.baudrate = self.baudrate 
                    self.ser.port = _port
                    self.ser.timeout = 1
                    self.ser.open()
                    print("connessione aperta")
                    #self.enable_commands() TODO PER ORA è DISABILITATO
                else:
                    print("la porta è stata sconnessa, impossibile connettersi")
            else:
                print("comunicazione seriale già aperta")
    def disconnect_from_HW(self):
        if self.ser.is_open:    # Establish the connection on a specific port
            print("disconnessione in corso")
            self.ser.close()
            print("connessione chiusa")
            #self.disable_commands()    TODO
        else:
            print("nessuna comunicazione seriale aperta")
    def combobox_serial_update(self):
        print("COMBOBOX SERIAL postcommand entered")
        ports = self.get_serial_ports()
        self.combobox_serial_port["values"] = ports
    """
    def combobox_conn_2_update(self, eventObject=None):
        print("----entered in combobox_conn_2_update()----")
        _conns = ["None"]
        for _conn in self.connectors:
            _name = _conn.get_name()
            #non appende il connettore 1 già selezionato
            if self.selected_connector_1 == None:
                _conns.append(_name)
                print("name: "+_name)
            elif _name == self.selected_connector_1.get_name():
                print("name: "+_name)
            else:
                _conns.append(_name)
                print("name: "+_name)
        #aggiorna la combobox con tutti i connettori tranne l'1 già selezionato
        self.combobox_conn_2["values"] = _conns

#version = 0.01
#BAUDRATE = 9600

'''
#definizione command
def single_check():
    ser.write([0b10010000])


# GRAFICA


def combo_address_1_update(eventObject):
    print(eventObject)
    print("binded funcion entered")
    _readed_values = int(combobox_n_pin_conn_1.get())
    if(_readed_values>0):
        _pins = list(range(1,_readed_values+1,1))  #questi parametri quando vengono inseriti nella combobox diventano stringhe
    else:
        print("Non sono disponibili pin per questo connettore\n")
        combobox_address_1.set("None")
        _pins = ["None"]
    combobox_address_1["values"]=_pins
    


#--------------------------INIZIO CODICE SEQUENZIALE---------------------
print("______________________________________________\nWiring Tester V"+ str(version)+"\n\n")
#INIZIALIZZAZIONE SERIALE E OGGETTO GRAFICO
main_frame = tk.Tk()        # istanzia un oggetto Tk
ser = serial.Serial()       # istanzio un oggetto seriale senza aprire la comunicazione
ports = get_serial_ports()  # controllo quali porte COM sono disponibili per poter aprire una comunicazione seriale
row_index = 0
col_index = 0
connectors = []

#METODI PER LA CONFIGURAZIONE DELLA FINESTRA principale
main_frame.geometry("800x500")
main_frame.title("Wiring Tester V"+ str(version))
main_frame.resizable(height=False, width=False)
#CONFIGURAZIONE DELLA LABEL
label_ports = tk.Label(main_frame, text="Seriali disponibili")
label_ports.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
#CONFIGURAZIONE DELLA COMBOBOX SERIALI DISPONIBILI
combobox_serial_port = ttk.Combobox(main_frame, values=ports, postcommand=combo_update)
combobox_serial_port.set("None")
combobox_serial_port.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
#CONFIGURAZIONE DEI PULSANTI CONNETTI/DISCONNETTI SERIALE
button_connect = tk.Button(main_frame, text="CONNETTI", command=connect_to_HW)
button_connect.grid(row=row_index, column=0, sticky="WE", padx=5, pady=1)
row_index+=1
button_disconnect = tk.Button(main_frame, text="DISCONNETTI", command=disconnect_from_HW)
button_disconnect.grid(row=row_index, column=0, sticky="WE", padx=5, pady=1)
row_index+=1
#LISTA CONNETTORI
label_conn_list = tk.Label(main_frame, text="Lista connettori:")
label_conn_list.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
listbox_conn_list = tk.Listbox(main_frame)
listbox_conn_list.insert(0,"None")
listbox_conn_list.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
listbox_conn_list.bind("<<ListboxSelect>>", 1)
row_index+=1
#AGGIUNGI, ELIMINA CONNETTORE
button_add_conn = tk.Button(main_frame, text="ADD CONNECTOR", command=add_connector)
button_del_conn = tk.Button(main_frame, text="DEL CONNECTOR", command=del_connector)
button_add_conn.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_del_conn.grid(row=row_index, column=0, sticky="WE")
row_index+=1
#CONFIGURAZIONE DELLA COMBOBOX SCELTA CONNETTORE
'''
'''
label_conn = tk.Label(main_frame, text="Scegli connettore:")
label_conn.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
combobox_conn = ttk.Combobox(main_frame, values=["CONN. 1","CONN. 2"])
combobox_conn.set("CONN. 1")
combobox_conn.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
'''
'''
#CONFIGURAZIONE DELLA COMBOBOX SCELTA NUMERO DI PIN CONNETTORE1
label_n_pin_con_1 = tk.Label(main_frame, text="Numero pin connettore 1: ")
label_n_pin_con_1.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
pins = list(range(128))
#print(pins)
combobox_n_pin_conn_1 = ttk.Combobox(main_frame, values=pins)
combobox_n_pin_conn_1.set("0")
combobox_n_pin_conn_1.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
combobox_n_pin_conn_1.bind("<<ComboboxSelected>>", combo_address_1_update) # associa all'evento selezione il callback combocox_address_update()
row_index+=1
#CONFIGURAZIONE DELLA COMBOBOX SCELTA NUMERO DI PIN CONNETTORE2
label_n_pin_con_2 = tk.Label(main_frame, text="Numero pin connettore 2: ")
label_n_pin_con_2.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
pins = list(range(128)) # QUESTA è UNA RIPETIZIONE
#print(pins)
combobox_n_pin_conn_2 = ttk.Combobox(main_frame, values=pins)
combobox_n_pin_conn_2.set("0")
combobox_n_pin_conn_2.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
combobox_n_pin_conn_2.bind("<<ComboboxSelected>>", combo_address_2_update) # associa all'evento selezione il callback combocox_address_update()
row_index+=1
'''
'''
#CONFIGURAZIONE LISTA ADDRESS SELECTION
label_address = tk.Label(main_frame, text="Seleziona l'address 1 da comandare")
label_address.grid(row=row_index, column=0, sticky="WE")
row_index+=1
listbox_address = tk.Listbox(main_frame)
for i in(range(16)):        
    print(i)    #questo non serve - era un mio debug a terminale
    listbox_address.insert(i,str(i))
listbox_address.grid(row=row_index, column=0, sticky="WE")
row_index+=1
'''
'''
#CONFIGURAZIONE COMBOBOX ADDRESS SELECTION 1
label_address_1 = tk.Label(main_frame, text="Seleziona l'address 2 da comandare")
label_address_1.grid(row=row_index, column=0, sticky="WE")
row_index+=1
combobox_address_1 = ttk.Combobox(main_frame, values=["None"])
combobox_address_1.set("None")
combobox_address_1.grid(row=row_index, column=0, padx=5, pady=1, sticky="WE")
row_index+=1
#CONFIGURAZIONE COMBOBOX ADDRESS SELECTION 2
label_address_2 = tk.Label(main_frame, text="Seleziona l'address da comandare")
label_address_2.grid(row=row_index, column=0, sticky="WE")
row_index+=1
combobox_address_2 = ttk.Combobox(main_frame, values=["None"])
combobox_address_2.set("None")
combobox_address_2.grid(row=row_index, column=0, padx=5, pady=1, sticky="WE")
row_index+=1

#CONFIGURAZIONE PULSANTI INVIA COMANDI
button_address = tk.Button(main_frame, text="SEND ADDRESS", command=send_address)
button_single_check = tk.Button(main_frame, text="CHECK CONTINUITY", command=single_check)
button_total_check = tk.Button(main_frame, text="CHECK ALL", command=total_check)
button_read = tk.Button(main_frame, text="READ RESPONSE", command=read_response)

button_address.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_single_check.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_total_check.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_read.grid(row=row_index, column=0, sticky="WE")
row_index+=1

#COL2
row_index = 0
col_index = 1
#connettore1
label_conn = tk.Label(main_frame, text="Connettore selezionato:")
label_conn.grid(row=row_index, column=col_index, sticky="WE")
row_index+=1
label_conn_name = tk.Label(main_frame, text="--")
label_conn_name.grid(row=row_index, column=col_index, sticky="WE")
row_index+=1
label_n_pin_con_1 = tk.Label(main_frame, text="n pin conn: -- ")
label_n_pin_con_1.grid(row=row_index, column=col_index, sticky="WE")
row_index+=1
#connettore2
label_conn_2 = tk.Label(main_frame, text="Connettore 2:")
label_conn_2.grid(row=row_index, column=col_index, sticky="WE")
row_index+=1
combobox_conn_2 = ttk.Combobox(main_frame, values=["None"])
combobox_conn_2.set("None")
combobox_conn_2.grid(row=row_index, column=col_index, padx=5, pady=1, sticky="WE")
row_index+=1
#text_console = tks.ScrolledText(main_frame)
#text_console.insert("console >>")
#text_console.grid(row=8, column=0, sticky="WE")

#comandi disabilitati fuìinchè non viene aperta una comunicazione
disable_commands()
'''
front_end = Front_End()
front_end.main_frame.mainloop()
#INIZIO L'ESSECUZIONE E L'EVENT HANDLING
#main_frame.mainloop() 