import tkinter as tk

class Gui():
    def __init__(self,_app,_state):
        self.app = _app
        self.state = _state

        self.main_frame = tk.Tk()
        self.main_frame.geometry("800x600")
        self.main_frame.minsize(800,600)
        self.main_frame.title("Wiring Tester V"+ str(self.state.version))
        self.main_frame.resizable(height=True, width=True)
        self.layer_left = tk.Frame(self.main_frame, relief="groove", borderwidth=2, padx=2, pady=2)
        self.layer_right = tk.Frame(self.main_frame, relief="groove", borderwidth=2)
        self.main_frame.grid_columnconfigure(1,weight=1)
        self.main_frame.grid_rowconfigure(0,weight=1)
        #self.layer_left.grid_columnconfigure(0,weight=1) # le commento perchè non voglio che queste colonne si espandano quando faccio un resize
        #self.layer_left.grid_columnconfigure(1,weight=1)
        #self.layer_left.grid_columnconfigure(2,weight=2)
        self.layer_left.grid_rowconfigure(1,weight=1)
        self.layer_right.grid_columnconfigure(0,weight=1)
        self.layer_right.grid_rowconfigure(0,weight=1)
        self.layer_left.grid(row=0,column=0,sticky="nswe")
        self.layer_right.grid(row=0,column=1,sticky="nswe")
        self.layer_left.grid_rowconfigure(1,weight=1)
        self.dashboard_frame = tk.Frame(self.layer_left,relief="groove", borderwidth=2)
        self.terminal_frame = tk.Frame(self.layer_left,relief="groove", borderwidth=2)
        self.dashboard_frame.grid(row=0,column=0,sticky="n")
        self.terminal_frame.grid(row=1,column=0,sticky="nwes")
        self.dashboard_frame.grid_columnconfigure(0,weight=1)
        self.terminal_frame.grid_columnconfigure(0,weight=1)
        self.dashboard_frame.grid_rowconfigure(0,weight=1)
        #elf.terminal_frame.grid_rowconfigure(0,weight=1)
        #tk.Button(self.layer_right).grid()
        #wid = self.layer_right.winfo_id()
        #os.system('xterm -into %d -geometry 40x20 -sb &' % wid)
        

        
        self.left_1_frame = tk.Frame(self.dashboard_frame)# relief = "raised", borderwidth=1,padx=2,pady=1) #bg = "pink")
        self.left_1_frame.grid_columnconfigure(0,weight=1)
        self.left_2_frame = tk.Frame(self.dashboard_frame)#, relief = "raised", borderwidth=1,padx=2,pady=1) # bg = "green")
        self.left_2_frame.grid_columnconfigure(0,weight=1)
        self.frame_serial_dash = tk.Frame(self.left_1_frame, relief = "ridge", borderwidth = 4, padx = 2, pady = 1)# bg = "black")
        self.frame_serial_command = tk.Frame(self.left_2_frame, pady = 5)#, relief = "flat", borderwidth = 4, padx = 2, pady = 1) #bg = "blue")
        self.frame_IO = tk.Frame(self.left_2_frame, relief = "flat", borderwidth = 4, padx = 2, pady = 1) #, bg="red", relief = "raised", borderwidth=1,
        self.frame_serial_dash.grid_columnconfigure(0,weight=1)
        self.frame_IO.grid(row=2, column=0, sticky="WE")
        #self.left_2_frame.grid_columnconfigure(0,weight=1)
        #self.left_1_frame.grid_propagate(False)
        #self.left_2_frame.grid_propagate(False)

        self.frame_serial_dash.grid(row=0, column=0, padx=0, pady=1, sticky="we")
        self.frame_serial_command.grid(row=1, column=0, padx=5, pady=1, sticky="we")
        
        #LISTA CONNETTORI
        self.list_frame = tk.Frame(self.left_1_frame, relief = "ridge", borderwidth = 4, padx = 2, pady = 2)
        self.list_frame.grid_columnconfigure(0,weight=1)
        self.list_frame.grid(sticky="we")

        #COL2
        self.conn_table_frame = tk.Frame(self.left_2_frame)
        self.conn_table_frame.grid(row=0,column=0,sticky="we")

        self.grid_matrix_frame = tk.Frame(self.layer_right, relief = "ridge", borderwidth=3)
        
        self.left_1_frame.grid(row=0, column=0, sticky="nswe")
        self.left_2_frame.grid(row=0, column=1, sticky="nswe")
        self.grid_matrix_frame.grid(row=0, column=0, sticky="nswe")

        if self.state.debug:
            self.btn_print_cont = tk.Button(self.left_2_frame, text="print state", command=self.app.print_state)
            self.btn_print_cont.grid()

            self.btn_render = tk.Button(self.left_2_frame, text="render", command=self.app.render_grid_matrix)
            self.btn_render.grid()