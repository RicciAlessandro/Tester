class State():
    def __init__(self):
        self.version = 0.01
        self.debug = True
        self.continuity = {}
        self.selected_connector_1 = None
        self.selected_connector_2 = None
        self.connector_list = []

    def set_selected_connector_1(self, _conn):
        if _conn:
            self.selected_connector_1 = _conn
        else:
            self.selected_connector_1 = None

    def set_selected_connector_2(self, _conn):
        if _conn:
            self.selected_connector_2 = _conn
        else:
            self.selected_connector_2 = None
    
    def print_state(self):
        print("continuity 1: \n", self.continuity)
        print("connectors: \n" , self.connector_list)
        _conn_name = []
        if self.connector_list:
            for k in self.connector_list:
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
    
    def reset(self):
        self.__init__()
        
