import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks

version = 0.01
BAUDRATE = 9600
main_frame = tk.Tk()
ser = serial.Serial()

#definizione funzioni
def send_address():
    '''
    print(type(listbox_address.curselection())) ---> tupla
    print(type(listbox_address.curselection()[0])) ----> di interi
    '''
    _addr_int = listbox_address.curselection()[0]
    sended_com_byte = ser.write([16])
    sended_addr_byte = ser.write([_addr_int])
    print("address sended: "+str(_addr_int))
    
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
    listbox_address["state"] = "normal"
    label_address["state"] = "normal"
    button_read["state"] = "normal"

def disable_commands():
    button_address["state"] = "disabled"
    button_check["state"] = "disabled"
    listbox_address["state"] = "disabled"
    label_address["state"] = "disabled"
    button_read["state"] = "disabled"



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

print("______________________________________________\nWiring Tester V"+ str(version)+"\n\n")
#METODI PER LA CONFIGURAZIONE DELLA FINESTRA
main_frame.geometry("800x500")
main_frame.title("Wiring Tester V"+ str(version))
main_frame.resizable(height=False, width=False)

label_ports = tk.Label(main_frame, text="Seriali disponibili")
label_ports.grid(row=0,column=0, padx=5, pady=1, sticky="WE")

ports = get_serial_ports()

combobox_serial_port = ttk.Combobox(main_frame, values=ports, postcommand=combo_update)
combobox_serial_port.set("None")
combobox_serial_port.grid(row=1,column=0, padx=5, pady=1, sticky="WE")

button_connect = tk.Button(main_frame, text="CONNETTI", command=connect_to_HW)
button_connect.grid(row=2, column=0, sticky="WE", padx=5, pady=1)
button_disconnect = tk.Button(main_frame, text="DISCONNETTI", command=disconnect_from_HW)
button_disconnect.grid(row=3, column=0, sticky="WE", padx=5, pady=1)

label_address = tk.Label(main_frame, text="Seleziona l'address da comandare")
label_address.grid(row=4, column=0, sticky="WE")
listbox_address = tk.Listbox(main_frame)
for i in(range(16)):
    print(i)
    listbox_address.insert(i,str(i))
listbox_address.grid(row=5, column=0, sticky="WE")

button_address = tk.Button(main_frame, text="SEND ADDRESS", command=send_address)
button_check = tk.Button(main_frame, text="CHECK CONTINUITY", command=check_continuity)
button_read = tk.Button(main_frame, text="READ RESPONSE", command=read_response)

button_address.grid(row=6, column=0, sticky="WE")
button_check.grid(row=7, column=0, sticky="WE")
button_read.grid(row=8, column=0, sticky="WE")

#text_console = tks.ScrolledText(main_frame)
#text_console.insert("console >>")
#text_console.grid(row=8, column=0, sticky="WE")

#comandi disabilitati fuìinchè non viene aperta una comunicazione
disable_commands()

#INIZIO L'ESSECUZIONE E L'EVENT HANDLING
main_frame.mainloop() 