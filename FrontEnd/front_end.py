import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from connector import *
from grid_matrix import *
#import connector
      
class Front_End():
    def __init__(self):
        self.main_frame = tk.Tk()
        self.left_1_frame = tk.Frame(self.main_frame)
        self.left_2_frame = tk.Frame(self.main_frame)
        self.connectors = []
        self.continuity = {}
        self.selected_connector_1 = None
        self.selected_connector_2 = None # selected connector deve essere sempre coerent -> None nei casi di implausibilità (lista vuota, connettore eliminato, connettore1 = connettore2)
        self.ser = serial.Serial()       # istanzio un oggetto seriale senza aprire la comunicazione
        self.baudrate = 9600
        self.version = 0.01
        self.ports = self.get_serial_ports()  # controllo quali porte COM sono disponibili per poter aprire una comunicazione seriale
        self.row_index = 0
        self.col_index = 0
        #METODI PER LA CONFIGURAZIONE DELLA FINESTRA principale
        self.__init__main_frame()
        #CONFIGURAZIONE DELLA LABEL
        self.label_ports = tk.Label(self.left_1_frame, text="Seriali disponibili")
        self.label_ports.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.row_index+=1
        #CONFIGURAZIONE DELLA COMBOBOX SERIALI DISPONIBILI
        self.combobox_serial_port = ttk.Combobox(self.left_1_frame, values=self.ports, postcommand=self.combobox_serial_update)
        self.combobox_serial_port.set("None")
        self.combobox_serial_port.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.row_index+=1
        #CONFIGURAZIONE DEI PULSANTI CONNETTI/DISCONNETTI SERIALE
        self.button_connect = tk.Button(self.left_1_frame, text="CONNETTI", command=self.connect_to_HW)
        self.button_connect.grid(row=self.row_index, column=0, sticky="WE", padx=5, pady=1)
        self.row_index+=1
        self.button_disconnect = tk.Button(self.left_1_frame, text="DISCONNETTI", command=self.disconnect_from_HW)
        self.button_disconnect.grid(row=self.row_index, column=0, sticky="WE", padx=5, pady=1)
        self.row_index+=1
        #LISTA CONNETTORI
        self.label_conn_list = tk.Label(self.left_1_frame, text="Lista connettori:")
        self.label_conn_list.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.row_index+=1
        self.listbox_conn_list = tk.Listbox(self.left_1_frame, selectmode = "SINGLE", exportselection=False)
        self.listbox_conn_list.insert(0,"None")
        self.listbox_conn_list.grid(row=self.row_index,column=0, padx=5, pady=1, sticky="WE")
        self.listbox_conn_list.bind("<<ListboxSelect>>", self.on_conn1_selection) # se non metto la proprietà exportselection a False ogni volta che 
        self.row_index+=1
        #AGGIUNGI, ELIMINA CONNETTORE
        self.button_add_conn = tk.Button(self.left_1_frame, text="ADD CONNECTOR", command=self.add_connector)
        self.button_del_conn = tk.Button(self.left_1_frame, text="DEL CONNECTOR", command=self.del_connector)
        self.button_add_conn.grid(row=self.row_index, column=0, sticky="WE")
        self.row_index+=1
        self.button_del_conn.grid(row=self.row_index, column=0, sticky="WE")
        self.row_index+=1
        #COL2
        self.row_index = 0
        #self.col_index = 1
        #connettore1
        self.label_conn = tk.Label(self.left_2_frame, text="Connettore selezionato:")
        self.label_conn.grid(row=self.row_index, column=self.col_index, sticky="WE")
        self.row_index+=1
        self.label_conn_name = tk.Label(self.left_2_frame, text="--")
        self.label_conn_name.grid(row=self.row_index, column=self.col_index, sticky="WE")
        self.row_index+=1
        self.label_n_pin_con_1 = tk.Label(self.left_2_frame, text="n pin conn: -- ")
        self.label_n_pin_con_1.grid(row=self.row_index, column=self.col_index, sticky="WE")
        self.row_index+=1
        #connettore2
        self.label_conn_2 = tk.Label(self.left_2_frame, text="Connettore 2:")
        self.label_conn_2.grid(row=self.row_index, column=self.col_index, sticky="WE")
        self.row_index+=1
        self.combobox_conn_2 = ttk.Combobox(self.left_2_frame, values=["None"], postcommand=self.combobox_conn_2_update)
        self.combobox_conn_2.bind("<<ComboboxSelected>>",self.update_selected_connector_2)
        self.combobox_conn_2.set("None")
        self.combobox_conn_2.grid(row=self.row_index, column=self.col_index, padx=5, pady=1, sticky="WE")
        #self.combobox_conn_2.bind("<<ComboboxSelected>>", self.combobox_conn_2_update)
        self.row_index+=1
        self.grid_matrix_frame = tk.Frame(self.main_frame)
        self.grid_matrix = GridMatrix(self.grid_matrix_frame)
        self.row_index = 0
        self.col_index += 1
        self.left_1_frame.grid(row=0, column=0, sticky="n")
        self.left_2_frame.grid(row=0, column=1, sticky="n")
        self.grid_matrix_frame.grid(row=0, column=2, sticky="n")

    def __init__main_frame(self):
        self.main_frame.geometry("800x500")
        self.main_frame.title("Wiring Tester V"+ str(self.version))
        self.main_frame.resizable(height=False, width=False)

    def get_serial_ports(self):
        _port_list = serial.tools.list_ports.comports()
        _port_list_string = ["None"]
        for i in _port_list:
            _port_list_string.append(str(i.name))
        return _port_list_string
    
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
                self.label_conn_name["text"] = _c_name
                self.label_n_pin_con_1["text"] = "n pin conn: "+str(c.get_n_pin())
                if self.selected_connector_2 == self.selected_connector_1:
                    print("connettori selezionati uguali, connettore 2 viene settato a None")
                    self.selected_connector_2 == None
                    self.combobox_conn_2.set("None")
                    print("selected connector2 = None")
                return
        self.selected_connector_1 = None
        self.listbox_conn_list.activate(tk.END)
        self.label_conn_name["text"] = "--"
        self.label_n_pin_con_1["text"] = "n pin conn: -- "
        print("selected connector1 = None")

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
                    return
                elif _c_name == self.selected_connector_1.get_name():
                    print("connettore 2 selezionato uguale a connettore selezionato 1")
                else:
                    print("conn 2 != conn 1 - OK")
                    print("selected connector2 = "+ _c_name)
                    self.selected_connector_2 = c
                    return
            #else:
            #    print("selezionato connettore 2 None (nessun connettore nella lista connectors[] coincide con la combobox)")
        self.selected_connector_2 = None
        self.combobox_conn_2.set("None")
        #self.label_conn_name["text"] = "--"
        print("selected connector2 = None")
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
        self.upper_frame = tk.Frame(self.frame)
        self.lower_frame = tk.Frame(self.frame)
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
        self.ok_btn.grid(row=0,column=1, padx=5, pady=1, sticky="WE")
        # ok_btn.bind("<<Button-1>>", ok_btn_add_connector(self, msg_box))
        self.cancel_btn = tk.Button(self.lower_frame, text = "Cancel", command=self.cancel_btn_add_connector)
        #cancel_btn.bind("<<Button-1>>", cancel_btn_add_connector(self, msg_box))
        self.cancel_btn.grid(row=0,column=0, padx=5, pady=1, sticky="WE")
    
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
        _int_input = int(self.combobox_n_pin_new.get())
        print(_int_input)
        _new_conn = Connector(_int_input,_text_input,1)
        self.continuity[_new_conn.get_name()]=None
        self.connectors.append(_new_conn)
        self.listbox_conn_list.insert(0,_new_conn.get_name()) #volevo metterci END al posto di 0, ma non è definito
        #self.entry_name.destroy()
        #self.combobox_n_pin_new.destroy()
        self.frame.destroy()
        #self.combobox_conn_2_update()
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
            self.continuity[self.connectors[-_idx-1].get_name()]
            print("a")
            del self.connectors[-_idx-1]  #nella listbox gli ultimi inseriti sono gli indici verso lo zero, nella lista invece gli ultimi appesi sono quelli verso END
            print("a")
            self.listbox_conn_list.delete(_idx)
            #self.listbox_conn_list.ac##(TODO tk.END)
            self.update_selected_connector_1()
        except:
            print("errore: indice selezionato inesistente")
        print("end del")
        for c in self.connectors:
            print(c.get_name())
        
        #self.combobox_conn_2_update()
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

def total_check():
    ser.write([0b11111111])

def read_response():
    a = ser.readline()
    print(a)
    #print(ser.read())
    #aggiungere i controlli che non si stia leggendo quando la comunicazione è chiusa

def send_address():
    print(type(listbox_address.curselection())) ---> tupla
    print(type(listbox_address.curselection()[0])) ----> di interi

    #_addr_int = listbox_address.curselection()[0]
    _addr_int_1 = int(combobox_address_1.get())
    _addr_int_2 = int(combobox_address_2.get())

    #INVIA COMANDI
    ser.write([97]) #manda comando prova
    #sended_com_byte = ser.write([])
    #_addr_byte = ser.write([_addr_int]) #in realtà la reference di serial.write() dice che non ci vanno le graffe, ma se non le metto e ci metto 6 ad esempio mi manda 6 byte vuoti.
    _addr_byte_1 = ser.write([_addr_int_1])   #ECCERTO CHE MI INVIAVA UNA SERIE DI BYTE, è PERCHE NON è SERIAL.WRITE MA è PYSERIAL.WRITE CHE FUNZIONA DIVERSAMENTE
    _addr_byte_2 = ser.write([_addr_int_2])
    print("address 1 sended: "+str(_addr_int_1)+" in "+str(_addr_byte_1)+" byte")
    print("address 2 sended: "+str(_addr_int_2)+" in "+str(_addr_byte_2)+" byte")
    
    #sended_bytes = ser.write([_addr_int])
    #print("sended "+ str(sended_bytes) +" bytes")
    #QUI CI VANNO LE GRAFFE!!!! ALTRIMENTI CREA UN VETTORE IMMUTABILE DI X BYTES
    _addr_byte = bytes([_addr_int]) #bytes crea invece un vettore di byte di lunghezza pari all'argomento passato
    print("address: "+str(_addr_byte))
    sended_bytes = ser.write(_addr_byte)
    print("sended "+ str(sended_bytes) +" bytes")
     sended_bytes1 = ser.write(b'f60')
    print(sended_bytes1
    sended_bytes2 = ser.write(bytes([10]))
    print(sended_bytes2)
 
class popupWindows():
    self.top = ##da vedereeee
    self.l=Label(top,text="Hello World")
    self.l.pack()

def add_connector():
    msg_box = tk.Tk()
    upper_frame = tk.Frame(msg_box)
    lower_frame = tk.Frame(msg_box)
    upper_frame.grid(row=0, column=0, sticky="WE")
    lower_frame.grid(row=1, column=0, sticky="WE")
    ok_btn = tk.Button(lower_frame, text = "Ok", command=ok_btn_add_connector(msg_box))
    ok_btn.grid(row=0,column=1, padx=5, pady=1, sticky="WE")
   # ok_btn.bind("<<Button-1>>", ok_btn_add_connector(self, msg_box))
    cancel_btn = tk.Button(lower_frame, text = "Cancel", command=cancel_btn_add_connector(msg_box))
    #cancel_btn.bind("<<Button-1>>", cancel_btn_add_connector(self, msg_box))
    cancel_btn.grid(row=0,column=0, padx=5, pady=1, sticky="WE")
    entry_n_pin = tk.Entry(upper_frame, textvariable = "inserisci n_pin_conn")
    entry_n_pin.grid(row=1, column=0, padx=5, pady=1, sticky="WE")
    #crea nuovo connettore, lo appende alla lista di connettori e alla listobox
    _new_conn = Connector(10,"ConnettoreProva",1)
    connectors.append(_new_conn)
    listbox_conn_list.insert(0,_new_conn.get_name()) #volevo metterci END al posto di 0, ma non è definito
    combobox_conn_2_update()

def ok_btn_add_connector(_master):
    print("ok pressed")
    #o = tk.Entry(_master)
    #o.grid(row=2,column=2)
    _master.destroy()

def cancel_btn_add_connector(_master):
    print("cancel pressed")
    #_master.destroy()

def del_connector():
    print("start del")
    try:
        _idx = listbox_conn_list.curselection()[0]
    except:
        print("errore: elemento cancellato")
        print("end del")
        return
    try:
        del connectors[_idx]
        listbox_conn_list.delete(_idx)
    except:
        print("errore: indice selezionato inesistente")
    print("end del")
    combobox_conn_2_update()


def 1(eventObject):
    print("listbox selected")
    listbox_selected = listbox_conn_list.get(listbox_conn_list.curselection())#[0]
    label_conn_name["text"] = listbox_selected
    #trova il connettore selezionato nella lista dei connettori
    if listbox_selected == "None":
        label_n_pin_con_1["text"] = "n pin conn = -- "
    else:
        for _conn in connectors:
            _name = _conn.get_name()
            if _name == listbox_conn_list.get(listbox_conn_list.curselection()):
                label_n_pin_con_1["text"] = "n pin conn: "+str(_conn.get_n_pin())
                print("name: "+_name)
            else:
                print("connettore con nome diverso scartato")
    combobox_conn_2_update()


# GRAFICA
def enable_commands():
    button_address["state"] = "normal"
    button_single_check["state"] = "normal"
    button_total_check["state"] = "normal"
    combobox_address_1["state"] = "normal"
    combobox_address_2["state"] = "normal"
    label_address_1["state"] = "normal"
    label_address_2["state"] = "normal"
    #label_conn["state"] = "normal"
    #label_n_pin_con_1["state"] = "normal"
    #label_n_pin_con_2["state"] = "normal"
    combobox_n_pin_conn_1["state"] = "normal"
    combobox_n_pin_conn_2["state"] = "normal"
    button_read["state"] = "normal"
    #combobox_conn["state"] = "normal"
    
def disable_commands():
    button_address["state"] = "disabled"
    button_single_check["state"] = "disabled"
    button_total_check["state"] = "disabled"
    combobox_address_1["state"] = "disabled"
    combobox_address_2["state"] = "disabled"
    label_address_1["state"] = "disabled"
    label_address_2["state"] = "disabled"
    #label_conn["state"] = "disabled"
    #label_n_pin_con_1["state"] = "disabled"
    #label_n_pin_con_2["state"] = "disabled"
    combobox_n_pin_conn_1["state"] = "disabled"
    combobox_n_pin_conn_2["state"] = "disabled"
    button_read["state"] = "disabled"
    #combobox_conn["state"] = "disabled"
    



def combo_update():
    print("postcommand entered")
    ports = get_serial_ports()
    combobox_serial_port["values"]=ports

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
    '''
'''
def combobox_conn_2_update(_selected_name, _connectors):
    _conns = []
    for _conn in _connectors:
        _name = _conn.get_name
        if _name == _selected_name:
            print("connettore selezionato non riportato nella combobox")
        else:
            _conns.append(_name)
    combobox_conn_2["values"] = _conns
'''
'''
def combobox_conn_2_update():
    _conns = []
    for _conn in connectors:
        _name = _conn.get_name()
        if _name == listbox_conn_list.get(listbox_conn_list.curselection()):
            print("name: "+_name)
        else:
            _conns.append(_name)
            print("name: "+_name)
    combobox_conn_2["values"] = _conns

def combo_address_2_update(eventObject):
    print(eventObject)
    print("binded funcion entered")
    _readed_values = int(combobox_n_pin_conn_2.get())
    if(_readed_values>0):
        _pins = list(range(1,_readed_values+1,1))  #questi parametri quando vengono inseriti nella combobox diventano stringhe
        #_pins.insert("None",0)
    else:
        print("Non sono disponibili pin per questo connettore\n")
        combobox_address_2.set("None")
        _pins = ["None"]
    combobox_address_2["values"]=_pins

def connect_to_HW():
    _port = combobox_serial_port.get()
    print(_port)
    if _port == "None":
        print("seleziona una porta seriale valida")
    else:
        #va inserito un blocco try except con la gestione degli errori.
        if not(ser.is_open): # Establish the connection on a specific port
            if _port in get_serial_ports():
                print("connessione in corso")
                ser.baudrate = BAUDRATE 
                ser.port = _port
                ser.timeout = 1
                ser.open()
                print("connessione aperta")
                enable_commands()
            else:
                print("la porta è stata sconnessa, impossibile connettersi")
        else:
            print("comunicazione seriale già aperta")

def disconnect_from_HW():
    
    if ser.is_open:    # Establish the connection on a specific port
        print("disconnessione in corso")
        ser.close()
        print("connessione chiusa")
        disable_commands()
    else:
        print("nessuna comunicazione seriale aperta")


#RITORNA UNA LISTA DI STRING CON LE PORTE DISPONIBILI
def get_serial_ports():
    _port_list = serial.tools.list_ports.comports()
    _port_list_string = ["None"]
    for i in _port_list:
        _port_list_string.append(str(i.name))
    return _port_list_string





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