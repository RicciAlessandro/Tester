import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import time

class SerialManager(object):
    """
    docstring
    """
    def __init__(self, _frame_1, _frame_2, _frame_3, _app, _connectors):
        self.connectors = _connectors
        self.ser = serial.Serial()
        self.frame_1 = _frame_1
        self.frame_2 = _frame_2
        self.frame_3 = _frame_3
        self.read_timeout = 0
        self.app = _app
        self.baudrate = 9600
        self.timeout = 0.1
        self.wait_timeout = 5
        self.ports = self.get_serial_ports()
        self.serial_terminal = SerialTerminal(self.ser, self.frame_3)
        self.serial_terminal.text.after(1000,self.serial_terminal.read_serial)

        self.frame_1.grid_columnconfigure(0,weight=1)
        self.frame_2.grid_columnconfigure(0,weight=1)
        
        #self.frame_3.grid(row=0,column=0)#,sticky="nswe")
        
        #LABEL
        self.label_ports = tk.Label(self.frame_1, text="Seriali disponibili")
        
        #CONFIGURAZIONE DELLA COMBOBOX SERIALI DISPONIBILI
        self.combobox_serial_port = ttk.Combobox(self.frame_1, values=self.ports, postcommand=self.combobox_serial_update)
        self.combobox_serial_port.set("None")
        
        #CONFIGURAZIONE DEI PULSANTI CONNETTI/DISCONNETTI SERIALE
        self.button_connect = tk.Button(self.frame_1, text="CONNETTI", command=self.connect_to_HW)
        self.button_disconnect = tk.Button(self.frame_1, text="DISCONNETTI", command=self.disconnect_from_HW)
        
        self.label_ports.grid(row=0,column=0, padx=5, pady=1, sticky="WE")
        self.button_connect.grid(row=2, column=0, sticky="WE", padx=5, pady=1)
        self.button_disconnect.grid(row=3, column=0, sticky="WE", padx=5, pady=1)
        self.combobox_serial_port.grid(row=1,column=0, padx=5, pady=1, sticky="WE")

        #secondo frame COMANDI SERIALE
        self.button_total_check = tk.Button(self.frame_2, text="TOTAL CHECK", command=self.total_check)
        self.button_address = tk.Button(self.frame_2, text="CHECK ADDRESS", command=self.send_address)
        self.button_read = tk.Button(self.frame_2, text="READ RESPONSE", command=self.read_response)

        self.button_total_check.grid(row=0,column=0, padx=2, pady=1, sticky="WE")
        self.button_address.grid(row=1,column=0, padx=2, pady=1, sticky="WE")
        self.button_read.grid(row=2,column=0, padx=2, pady=1, sticky="WE")

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
                    self.ser.timeout = self.read_timeout
                    self.ser.open()
                    print("connessione aperta")
                    self.enable_commands()
                else:
                    print("la porta è stata sconnessa, impossibile connettersi")
            else:
                print("comunicazione seriale già aperta")
        
    def disconnect_from_HW(self):
        if self.ser.is_open:    # Establish the connection on a specific port
            print("disconnessione in corso")
            self.ser.close()
            print("connessione chiusa")
            self.disable_commands()
        else:
            print("nessuna comunicazione seriale aperta")

    def combobox_serial_update(self):
        print("COMBOBOX SERIAL postcommand entered")
        ports = self.get_serial_ports()
        self.combobox_serial_port["values"] = ports

    def enable_commands(self):
        self.serial_terminal.enable = True
        self.button_address["state"] = "normal"
        self.button_total_check["state"] = "normal"
        self.button_read["state"] = "normal"   
        #button_single_check["state"] = "normal"
        #combobox_address_1["state"] = "normal"
        #combobox_address_2["state"] = "normal"
        #label_address_1["state"] = "normal"
        #label_address_2["state"] = "normal"
        #label_conn["state"] = "normal"
        #label_n_pin_con_1["state"] = "normal"
        #label_n_pin_con_2["state"] = "normal"
        #ombobox_n_pin_conn_1["state"] = "normal"
        #combobox_n_pin_conn_2["state"] = "normal"
        #combobox_conn["state"] = "normal"
    
    def disable_commands(self):
        self.serial_terminal.enable = False
        self.button_address["state"] = "disabled"
        self.button_total_check["state"] = "disabled"
        self.button_read["state"] = "disabled"
        #button_single_check["state"] = "disabled"
        #combobox_address_1["state"] = "disabled"
        #combobox_address_2["state"] = "disabled"
        #label_address_1["state"] = "disabled"
        #label_address_2["state"] = "disabled"
        #label_conn["state"] = "disabled"
        #label_n_pin_con_1["state"] = "disabled"
        #label_n_pin_con_2["state"] = "disabled"
        #combobox_n_pin_conn_1["state"] = "disabled"
        #combobox_n_pin_conn_2["state"] = "disabled"
        #combobox_conn["state"] = "disabled"
    
    def total_check(self):
        print(self.app.connectors)      #QUI SE METTO SELF.CONNECTORS NON SI AGGIORNA AL CAMBIARE DELLA LISTA DEI CONNETTORI DI APP
        if self.app.selected_connector_1:
            if self.app.selected_connector_2:
                #self.ser.flushInput()
                self.ser.write(bytes([0b11111111]))
                print(self.app.selected_connector_1.get_n_pin())
                print(self.app.selected_connector_2.get_n_pin())
                self.ser.write(self.app.selected_connector_1.get_name().encode())
                self.ser.write("\n".encode())
                self.ser.write(self.app.selected_connector_2.get_name().encode())
                self.ser.write("\n".encode())
                self.ser.write([self.app.selected_connector_1.get_n_pin()])
                self.ser.write([self.app.selected_connector_2.get_n_pin()])
                #time.sleep(0.8)
                self.frame_1.after(2000,self.read_total_check)
                '''
                for i in range(self.app.selected_connector_1.get_n_pin()):
                    for j in range(self.app.selected_connector_2.get_n_pin()):
                        time_base = time.time()
                        while(True):
                            if self.ser.in_waiting:
                                readed_line = self.ser.read() # b'\x03'
                                #print("prefisso: ",readed_line)
                                if readed_line==b'\xff':
                                    print("EOL find")
                                    break
                                elif(time.time()-time_base>self.wait_timeout):
                                    print("ERROR time elapsed")
                                    return
                        time_base = time.time()
                        while(True):
                            if self.ser.in_waiting:
                                readed_line = self.ser.read() # b'\x03'
                                print("byte letto", readed_line)
                                #print("prefisso: ",readed_line)
                                if(readed_line==b'\x0f'):
                                    print("OK 1 ", j)
                                    self.app.continuity[self.app.selected_connector_1.get_name()][self.app.selected_connector_2.get_name()][i][j] = 1
                                    self.app.continuity[self.app.selected_connector_2.get_name()][self.app.selected_connector_1.get_name()][j][i] = 1
                                    break
                                elif(readed_line==b'\01'):
                                    print("OK 2 ", j)
                                    self.app.continuity[self.app.selected_connector_1.get_name()][self.app.selected_connector_2.get_name()][i][j] = 0
                                    self.app.continuity[self.app.selected_connector_2.get_name()][self.app.selected_connector_1.get_name()][j][i] = 0
                                    break
                                else:
                                    self.app.continuity[self.app.selected_connector_1.get_name()][self.app.selected_connector_2.get_name()][i][j] = 5
                                    self.app.continuity[self.app.selected_connector_2.get_name()][self.app.selected_connector_1.get_name()][j][i] = 5
                                    print("reading ERROR")
                                    break
                            elif(time.time()-time_base>self.wait_timeout):
                                print("ERROR time elapsed with no response")
                                return
                print(self.app.continuity)      
                self.app.grid_matrix.render_2()
                '''
            else:
                print("nessun connettore 2 selezionato")
        else:
            print("nessun connettore 1 selezionato")

    def read_total_check(self):
        print("leggo dal buffer\n")
        print(self.serial_terminal.serial_buffer)
        _start_index = self.serial_terminal.serial_buffer.find("START TOTAL CHECK\n")
        _end_index = self.serial_terminal.serial_buffer.find("END TOTAL CHECK\n")
        if _end_index == -1:
            self.frame_1.after(1000,self.read_total_check)
            print("BUFFER NON PRONTO\n")
            return
        _command_response = self.serial_terminal.serial_buffer[_start_index:_end_index]
        print("COMMAND RESPONSE \n"+_command_response)
        _matrix_index = _command_response.find("Connection Matrix:\n")
        print("MARIX_INDEX"+str(_matrix_index)+"\n")
        _matrix = _command_response[_matrix_index+len("Connection Matrix:\n"):]
        print("MATRIX \n" + _matrix)
        #print("index = " + str(_start_index))
        #print(self.serial_terminal.serial_buffer[_start_index:])
        self.serial_terminal.serial_buffer=""
        _n_conn_1 = self.find_token(_command_response,"conn1:\t")
        _n_conn_2 = self.find_token(_command_response,"conn2:\t")
        _n_pin_conn_1 = int(self.find_token(_command_response,"nPin1\t"))
        _n_pin_conn_2 = int(self.find_token(_command_response,"nPin2\t"))
        print(_n_conn_1,"\n", _n_conn_2,"\n", _n_pin_conn_1,"\n", _n_pin_conn_2)

        k=0
        for i in range(_n_pin_conn_1):
            for j in range(_n_pin_conn_2):
                if(_matrix[k]=="1"):
                    print("OK 1 ", j)
                    self.app.continuity[_n_conn_1][_n_conn_2][i][j] = 1
                    self.app.continuity[_n_conn_2][_n_conn_1][j][i] = 1
                elif(_matrix[k]=="0"):
                    print("OK 2 ", j)
                    self.app.continuity[_n_conn_1][_n_conn_2][i][j] = 0
                    self.app.continuity[_n_conn_2][_n_conn_1][j][i] = 0
                else:
                    self.app.continuity[_n_conn_1][_n_conn_2][i][j] = 5
                    self.app.continuity[_n_conn_2][_n_conn_1][j][i] = 5
                    print("reading ERROR")
                k+=2
        print(self.app.continuity)      
        self.app.grid_matrix.render_2()

    def find_token(self,_string,_token):
        _start_index = _string.find(_token)
        _end_index = _string.find("\n",_start_index)
        return _string[_start_index+len(_token):_end_index]

    def read_response(self):
        a = self.ser.readline()
        print(a)
        #print(ser.read())
        #aggiungere i controlli che non si stia leggendo quando la comunicazione è chiusa

    def send_address(self):
        self.ser.flushInput()
        self.ser.write([0b11111111])
        time_base = time.time()
        while(True):
            read_line = self.ser.read()
            if read_line==b'\90':
                print("EOL finded")
                break
            elif(time.time()-time_base>5):
                print("ERROR time elapsed")
                return
        time.sleep(10)
        #print(type(listbox_address.curselection())) ---> tupla
        #print(type(listbox_address.curselection()[0])) ----> di interi

        #_addr_int = listbox_address.curselection()[0]
        #_addr_int_1 = int(combobox_address_1.get())
        #_addr_int_2 = int(combobox_address_2.get())

        #INVIA COMANDI
        #self.ser.write([97]) #manda comando prova
        #sended_com_byte = ser.write([])
        #_addr_byte = ser.write([_addr_int]) #in realtà la reference di serial.write() dice che non ci vanno le graffe, ma se non le metto e ci metto 6 ad esempio mi manda 6 byte vuoti.
        #_addr_byte_1 = ser.write([_addr_int_1])   #ECCERTO CHE MI INVIAVA UNA SERIE DI BYTE, è PERCHE NON è SERIAL.WRITE MA è PYSERIAL.WRITE CHE FUNZIONA DIVERSAMENTE
        #_addr_byte_2 = ser.write([_addr_int_2])
        #print("address 1 sended: "+str(_addr_int_1)+" in "+str(_addr_byte_1)+" byte")
        #print("address 2 sended: "+str(_addr_int_2)+" in "+str(_addr_byte_2)+" byte")
        
        #sended_bytes = ser.write([_addr_int])
        #print("sended "+ str(sended_bytes) +" bytes")
        #QUI CI VANNO LE GRAFFE!!!! ALTRIMENTI CREA UN VETTORE IMMUTABILE DI X BYTES
        #_addr_byte = bytes([_addr_int]) #bytes crea invece un vettore di byte di lunghezza pari all'argomento passato
        #print("address: "+str(_addr_byte))
        #sended_bytes = ser.write(_addr_byte)
        #print("sended "+ str(sended_bytes) +" bytes")
        #sended_bytes1 = ser.write(b'f60')
        #print(sended_bytes1
        #sended_bytes2 = ser.write(bytes([10]))
        #print(sended_bytes2)

class SerialTerminal():
    def __init__(self, _serial, _frame_1):
        self.parent_frame = _frame_1
        self.ser = _serial
        self.cmd_frame = tk.Frame(self.parent_frame)
        self.btn_frame = tk.Frame(self.cmd_frame)
        self.label = tk.Label(self.cmd_frame, text="SERIAL TERMINAL", relief="flat", borderwidth=2)
        self.btn_clc = tk.Button(self.btn_frame,text="CLEAR TERMINAL", command=self.on_clc_pressed)
        self.scrolled_frame = tk.Frame(self.parent_frame)
        self.text = tk.Text(self.scrolled_frame, exportselection=0)
        self.text.configure(state="disabled")
        self.text.configure(width=20)
        #self.text.pack(side="left", fill="y")
        self.scrollbar = tk.Scrollbar(self.scrolled_frame)
        #self.scrollbar.pack(side="right", fill="y")#, fill="y")
        self.enable = False
        #PARENT FRAME
        self.parent_frame.grid_columnconfigure(0,weight=1)
        self.parent_frame.grid_rowconfigure(1,weight=1)
        self.cmd_frame.grid(row=0,column=0,sticky="we")
        self.scrolled_frame.grid(row=1,column=0,sticky="nswe")
            #CMD TEXT
        self.cmd_frame.grid_columnconfigure(0,weight=1)
        self.label.grid(row=0,column=0, sticky="we")
        self.btn_frame.grid(row=1,column=0,sticky="we")
                #BTN FRAME
        self.btn_clc.grid(row=0,column=0)
            #SCOLLED FAME
        self.scrolled_frame.grid_columnconfigure(0,weight=1)
        self.scrolled_frame.grid_rowconfigure(0,weight=1)
        self.text.grid(row=0, column=0, sticky="nswe")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)
        self.serial_buffer = ""
        
    
    def read_serial(self):
        try:
            if self.enable:
                #print("trying to read from serial")
                _readed_bytes = ""    
                while(True):
                    if self.ser.in_waiting:
                        try:
                            _byte = self.ser.read().decode("ASCII")
                            _readed_bytes += _byte
                            print("readed " + str(_byte))
                        except:
                            print(_byte)
                        if self.ser.in_waiting==0:
                            self.text.configure(state="normal")
                            self.text.insert(tk.END, _readed_bytes)
                            self.text.see(tk.END)
                            self.text.configure(state="disabled")
                            self.serial_buffer += _readed_bytes
                            break
                    else:
                        #print("letto nulla")
                        break
            else:
                #print("serial disabled")
                pass
        except Exception as e:
            print("exception handlare \n ---------------- \n" + e)
        finally:
            self.text.after(1000,self.read_serial)
        

    def on_clc_pressed(self):
        self.text.configure(state="normal")
        self.text.delete('0.0',tk.END)
        self.text.configure(state="disabled")

if __name__ == "__main__":
    mainframe = tk.Tk()
    serial_manager = SerialManager(mainframe,None, None, None, None)
    mainframe.mainloop()