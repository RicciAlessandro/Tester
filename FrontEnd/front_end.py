import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks

version = 0.01
BAUDRATE = 9600


#definizione funzioni
def send_address():
    '''
    print(type(listbox_address.curselection())) ---> tupla
    print(type(listbox_address.curselection()[0])) ----> di interi
    '''
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

    '''
    #QUI CI VANNO LE GRAFFE!!!! ALTRIMENTI CREA UN VETTORE IMMUTABILE DI X BYTES
    _addr_byte = bytes([_addr_int]) #bytes crea invece un vettore di byte di lunghezza pari all'argomento passato
    print("address: "+str(_addr_byte))
    sended_bytes = ser.write(_addr_byte)
    print("sended "+ str(sended_bytes) +" bytes")
    '''

    ''''
    sended_bytes1 = ser.write(b'f60')
    print(sended_bytes1'''
    '''
    sended_bytes2 = ser.write(bytes([10]))
    print(sended_bytes2)
    '''

    
    

def enable_commands():
    button_address["state"] = "normal"
    button_check["state"] = "normal"
    combobox_address_1["state"] = "normal"
    combobox_address_2["state"] = "normal"
    label_address_1["state"] = "normal"
    label_address_2["state"] = "normal"
    #label_conn["state"] = "normal"
    label_n_pin_con_1["state"] = "normal"
    label_n_pin_con_2["state"] = "normal"
    combobox_n_pin_conn_1["state"] = "normal"
    combobox_n_pin_conn_2["state"] = "normal"
    button_read["state"] = "normal"
    #combobox_conn["state"] = "normal"
    
def disable_commands():
    button_address["state"] = "disabled"
    button_check["state"] = "disabled"
    combobox_address_1["state"] = "disabled"
    combobox_address_2["state"] = "disabled"
    label_address_1["state"] = "disabled"
    label_address_2["state"] = "disabled"
    #label_conn["state"] = "disabled"
    label_n_pin_con_1["state"] = "disabled"
    label_n_pin_con_2["state"] = "disabled"
    combobox_n_pin_conn_1["state"] = "disabled"
    combobox_n_pin_conn_2["state"] = "disabled"
    button_read["state"] = "disabled"
    #combobox_conn["state"] = "disabled"
    



#definizione command
def send_check_request():
    pass

def check_continuity():
    pass

def read_response():
    a = str(ser.read())
    print(a)
    #print(ser.read())
    #aggiungere i controlli che non si stia leggendo quando la comunicazione è chiusa


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
#CONFIGURAZIONE DELLA COMBOBOX SCELTA CONNETTORE
'''
label_conn = tk.Label(main_frame, text="Scegli connettore:")
label_conn.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
combobox_conn = ttk.Combobox(main_frame, values=["CONN. 1","CONN. 2"])
combobox_conn.set("CONN. 1")
combobox_conn.grid(row=row_index,column=0, padx=5, pady=1, sticky="WE")
row_index+=1
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
button_check = tk.Button(main_frame, text="CHECK CONTINUITY", command=check_continuity)
button_read = tk.Button(main_frame, text="READ RESPONSE", command=read_response)

button_address.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_check.grid(row=row_index, column=0, sticky="WE")
row_index+=1
button_read.grid(row=row_index, column=0, sticky="WE")
row_index+=1

#text_console = tks.ScrolledText(main_frame)
#text_console.insert("console >>")
#text_console.grid(row=8, column=0, sticky="WE")

#comandi disabilitati fuìinchè non viene aperta una comunicazione
disable_commands()

#INIZIO L'ESSECUZIONE E L'EVENT HANDLING
main_frame.mainloop() 