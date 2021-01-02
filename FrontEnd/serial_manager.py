import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk

class SerialManager(object):
    """
    docstring
    """
    def __init__(self, _frame_1, _frame_2):
        self.ser = serial.Serial()
        self.frame_1 = _frame_1
        self.frame_2 = _frame_2
        self.baudrate = 9600
        self.ports = self.get_serial_ports()
        self.frame = _frame_1
        #LABEL
        self.label_ports = tk.Label(self.frame, text="Seriali disponibili")
        
        #CONFIGURAZIONE DELLA COMBOBOX SERIALI DISPONIBILI
        self.combobox_serial_port = ttk.Combobox(self.frame, values=self.ports, postcommand=self.combobox_serial_update)
        self.combobox_serial_port.set("None")
        
        #CONFIGURAZIONE DEI PULSANTI CONNETTI/DISCONNETTI SERIALE
        self.button_connect = tk.Button(self.frame, text="CONNETTI", command=self.connect_to_HW)
        self.button_disconnect = tk.Button(self.frame, text="DISCONNETTI", command=self.disconnect_from_HW)
        
        self.label_ports.grid(row=0,column=0, padx=5, pady=1, sticky="WE")
        self.button_connect.grid(row=1, column=0, sticky="WE", padx=5, pady=1)
        self.button_disconnect.grid(row=2, column=0, sticky="WE", padx=5, pady=1)
        self.combobox_serial_port.grid(row=3,column=0, padx=5, pady=1, sticky="WE")
    

    def get_serial_ports(self):
        '''
        ritorna una lista di stringhe contenente tutte le seriali disponibili, compresa None
        '''
        _port_list = serial.tools.list_ports.comports()
        _port_list_string = ["None"]
        for i in _port_list:
            _port_list_string.append(str(i.name))
        return _port_list_string

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


if __name__ == "__main__":
    mainframe = tk.Tk()
    serial_manager = SerialManager(mainframe,None)
    mainframe.mainloop()