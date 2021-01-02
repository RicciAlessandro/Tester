import tkinter as tk
from connector import *
from contextlib import contextmanager
from tkinter import filedialog, messagebox
import pandas as pd
import math

class DataFileStream():
    """
    docstring
    """
    def __init__(self, _main_frame, _app=None): #_continuity=None
        #self.continuity = _continuity
        self.main_frame = _main_frame
        self.app = _app
        self.directory = None # TODO IN REALTA' QUI CI DEVO METTERE IL PERCORSO BASE DOVE DOVREI TROVARE I DB
        self.save_button = SaveButton(self.main_frame, self)
        self.select_dir = SelectDir(self.main_frame, self)

        if self.app.debug:
            self.load_button = LoadButton(self.main_frame, self)
        #self.save_button.grid(row=0, sticky=tk.EW, padx=5, pady=1)#rowspan=3
        #self.load_button.grid(row=1, sticky=tk.EW, padx=5, pady=1)
        
        self.select_dir.pack(fill="x")#, padx=5, pady=1)
        self.save_button.pack(fill="x")#, padx=5, pady=1)
        if self.app.debug:
            self.load_button.pack(fill="x")#, padx=5, pady=1)

class SaveButton(tk.Button):
    def __init__(self, _master, _data_file_stream):
        super().__init__(_master, text="SALVA SU FILE", command=self.on_press)
        self.data_file_stream = _data_file_stream 

    def on_press(self):
        if self.data_file_stream.app.continuity:
            self.data_file_stream.directory = filedialog.askdirectory(initialdir=".\FrontEnd\DB\Default")
            if self.data_file_stream.directory:
                print(self.data_file_stream.directory)
                #SALVA LA CONFIG
                try:

                    print()
                    _path = self.data_file_stream.directory+"\config.xlsx"
                    writer = pd.ExcelWriter(_path, engine="openpyxl")
                    _conns = []
                    _pins = []
                    for k,v in self.data_file_stream.app.continuity.items():
                        #trova il numero di pin del connettore
                        
                        for _conn in self.data_file_stream.app.connectors:
                            if _conn.get_name() == k:
                                _conns.append(_conn.get_name())
                                _pins.append(_conn.get_n_pin())
                                #print("OOK", _conn.get_name())
                                #print("pin", _n_pin)
                        #_sheet_value = {" ":_col}
                    _sheet_value = {"conn":_conns, "n_pin":_pins} #prima colonna del excel
                    df = pd.DataFrame(_sheet_value)
                    df.to_excel(writer,index=False)
                    writer.save()
                except:
                    print("save config failed")
                    messagebox.showerror("Error", e)
                    return

                #SALVA I CONNETTORI NEI RELATIVI FILE
                try:
                    for k,v in self.data_file_stream.app.continuity.items():
                        #trova il numero di pin del connettore
                        for _conn in self.data_file_stream.app.connectors:
                            if _conn.get_name() == k:
                                _n_pin = _conn.get_n_pin()
                                print("OOK", _conn.get_name())
                                print("pin", _n_pin)
                        _col_pin = list(range(1,_n_pin+1,1))
                        #_sheet_value = {" ":_col}
                        _sheet_value = {" ":_col_pin} #prima colonna del excel
                        print("key", k)
                        _path = self.data_file_stream.directory+"\\"+k+".xlsx"
                        writer = pd.ExcelWriter(_path, engine="openpyxl")
                        for kk,vv in v.items(): 
                            print("key", kk)
                            for row in vv:
                                for pin1 in row:
                                    print(pin1)
                                print("\n")
                            print("\n")
                            vv_transp = list(map(list,zip(*vv)))
                            j=1
                            for _col in vv_transp:
                                _sheet_value[j] = _col #colonne successive dell'excell
                                j+=1
                            df = pd.DataFrame(_sheet_value)
                            df.to_excel(writer,sheet_name=kk,index=False)
                        writer.save()
                except Exception as e:
                    messagebox.showerror("Error", e)
                    return
        else:
            print("nessuna matrice di continuità da salvare")

class SelectDir(tk.Button):
    def __init__(self, _master, _data_file_stream):
        super().__init__(_master, text="APRI FILE", command=self.on_press)
        self.data_file_stream = _data_file_stream 

    def on_press(self):

        self.data_file_stream.directory = filedialog.askdirectory(initialdir=".\FrontEnd\DB\Default")
        if self.data_file_stream.directory:
            print(self.data_file_stream.directory)
            #LEGGI LE CONFIGURAZIONI --> OUTPUT N_PIN_CONN_DIST (dizonario contenente il nome dei connettori con il numero di pin)
            try:
                readed_data = pd.read_excel(self.data_file_stream.directory+'/config.xlsx')
                print("readed_data")
                print(readed_data)
            except Exception as e:
                messagebox.showerror("Error", e)
                return
            #print(type(readed_data["conn"]))
            #print(readed_data["conn"])

            _keys = []
            for c in readed_data["conn"]:
                print(type(c))
                print(c)
                if isinstance(c,float):
                    if math.isnan(c):
                        #print("nan intercettato")
                        pass
                else:
                    print("appeso",c)
                    _keys.append(c)
            _values = []
            #print(type(readed_data["n_pin"]))
            #print(readed_data["n_pin"])
            for c in readed_data["n_pin"]:
                print(type(c))
                print(c)
                if isinstance(c,float):
                    if math.isnan(c):
                        #print("nan intercettato")
                        pass
                    else:
                        #print("ok")
                        _values.append(int(c))
                elif isinstance(c,int):
                    if math.isnan(c):
                        #print("nan intercettato")
                        pass
                    else:
                        #print("ok")
                        _values.append(int(c))
            print(_keys)
            print(_values)
            _n_pin_dict = dict(zip(_keys,_values))
            print(_n_pin_dict)
            #n_pin_dict = {"conn1":n_pin_1, "conn2":n_pin_2, "conn3":n_pin_3}

            # todo controllo se continuity già esiste e richiesta a procedere

            #AGGIUNGE I CONNETTORI.
            self.data_file_stream.app.connectors = []
            for _conn in list(_n_pin_dict.keys()):
                _new_conn = Connector(_n_pin_dict[_conn],_conn,1)
                self.data_file_stream.app.connectors.append(_new_conn)
            self.data_file_stream.app.listbox_update()
            
            #costruisco il dizionario con le chiavi:
            self.data_file_stream.app.continuity = {}
            for _conn_1 in self.data_file_stream.app.connectors:
                self.data_file_stream.app.continuity[_conn_1.get_name()] = {}
                for _conn_2 in self.data_file_stream.app.connectors:
                    if _conn_2.get_name() != _conn_1.get_name():
                        self.data_file_stream.app.continuity[_conn_1.get_name()][_conn_2.get_name()]=[]
            print("result")
            print(self.data_file_stream.app.continuity)

            #CARICA DATI DAI FILE:
            print("POPOLA DIZIONARIO CONTINUITA'")
            for _conn_1 in list(self.data_file_stream.app.continuity.keys()):
                print(_conn_1)
                #LEGGI LE CONFIGURAZIONI --> OUTPUT N_PIN_CONN_DIST (dizonario contenente il nome dei connettori con il numero di pin)
                for _conn_2 in list(self.data_file_stream.app.continuity[_conn_1].keys()):
                    if _conn_1 != _conn_2:
                        _connection_matrix = []
                        try:
                            print("_conn_1")
                            print(_conn_1)
                            print("_conn_2")
                            print(_conn_2)
                            readed_data = pd.read_excel(self.data_file_stream.directory+'/'+_conn_1+'.xlsx',sheet_name=_conn_2)
                            print("readed_data")
                            print(readed_data)
                            for _col in range(1,_n_pin_dict[_conn_2]+1,1):

                                print("COL")
                                print(_col)
                                print(type(_col))
                                print(readed_data[_col])
                                _connection_matrix.append(readed_data[_col]) #_col-1

                        except Exception as e:
                            messagebox.showerror("Error", e)
                            #return
                        #print(type(readed_data["conn"]))
                        #print(readed_data["conn"])
                        _connection_matrix = list(map(list,zip(*_connection_matrix)))
                        print(_connection_matrix)
                        self.data_file_stream.app.continuity[_conn_1][_conn_2]=_connection_matrix
        
        
class LoadButton(tk.Button):
    def __init__(self, _master, _data_file_stream):
        super().__init__(_master,text="APRI config base", command=self.on_press)
        self.data_file_stream = _data_file_stream
    
    def on_press(self):
        #print(self.data_file_stream.continuity)
        #with self.data_file_stream.app as up:
            print(self.data_file_stream.app.continuity)
            if self.data_file_stream.app.continuity:
                print("Tutte le misure e le configurazioni non salvate andranno \
perse. Sei sicuro di voler caricare i dati?")
                    #return

            #SIMULO LA LETTURA DAI FILE CHE MI RESTITUISCE QUESTO
            continuity_conn_1 = {"conn2":[[1,0,0],[0,1,0]],"conn3":[[0,0,1,0],[0,0,0,1]]}
            continuity_conn_2 = {"conn1":[[1,0],[0,1],[0,0]],"conn3":[[1,0,0,0],[0,0,0,0],[0,0,0,0]]}
            continuity_conn_3 = {"conn1":[[0,0],[0,0],[1,0],[0,1]],"conn2":[[0,1,0],[0,0,0],[0,0,0],[0,0,0]]}
            _cont = {"conn1":continuity_conn_1,"conn2":continuity_conn_2,"conn3":continuity_conn_3}
            n_pin_1 = 2
            n_pin_2 = 3
            n_pin_3 = 4
            n_pin_list = [n_pin_1, n_pin_2, n_pin_3]
            n_pin_dict = {"conn1":n_pin_1, "conn2":n_pin_2, "conn3":n_pin_3}
            #-----------------------------
            #self.data_file_stream.continuity = _cont       # SE PASSO QUESTO NON MI AGGIORNA L'ATTRIBUTO DELLA CLASSE PADRE 
            self.data_file_stream.app.continuity = _cont   # SE PASSO QUESTO MI AGGIORNA ANCHE L'ATTRIBTO DELLA CLASSE PADRE
            #self.data_file_stream.app.continuity.clear()
            #self.data_file_stream.app.continuity.append(_cont)

            #print(self.data_file_stream.continuity)
            print(self.data_file_stream.app.continuity)
            self.data_file_stream.app.connectors = []  #CLEAR DELLA LISTA
            _conn_name = list(self.data_file_stream.app.continuity.keys())
            k=0
            for c in _conn_name:
                _new_conn = Connector(n_pin_list[k],c,1)
                self.data_file_stream.app.connectors.append(_new_conn)
                k+=1
            self.data_file_stream.app.listbox_update()
            # lettura file creati


        
        

if __name__ == "__main__":
    main_frame = tk.Tk()
    frame_IO = DataFileStream(main_frame)
    main_frame.mainloop()