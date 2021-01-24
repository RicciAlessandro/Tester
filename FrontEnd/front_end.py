import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from connector import *
from grid_matrix import *
from data_file_stream import *
from serial_manager import *
import os
from menu import *
from gui import Gui
from state import State
#import connector
      
class Front_End():
    def __init__(self):
        #METODI PER LA CONFIGURAZIONE DELLA FINESTRA principale   
        self.state = State()
        self.gui = Gui(self,self.state)
        self.data_file_stream = DataFileStream(self, self.gui, self.state) # self.continuity
        self.connector_manager = ConnectorManager(self, self.gui, self.state)
        self.serial_manager = SerialManager(self, self.gui, self.state)
        self.grid_matrix = GridMatrix(self, self.gui, self.state, 0, 0, "--", "--")
        self.topMenu = TopMenu(self.gui.main_frame,self)
        self.gui.main_frame.config(menu=self.topMenu.menubar)
        
        
        
    def print_state(self):
        self.state.print_state()
        self.serial_manager.print_buffer()
        self.connector_manager.connector_table.update()

    def new_workspace(self):
        self.state.reset()
        self.connector_manager.update_all()
        self.grid_matrix.render_2()

    def render_grid_matrix(self):
        self.grid_matrix.render_2()

front_end = Front_End()
front_end.gui.main_frame.mainloop()
#INIZIO L'ESSECUZIONE E L'EVENT HANDLING
#main_frame.mainloop() 