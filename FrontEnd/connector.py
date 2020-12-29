class Connector():
    '''
    Connettore 
    '''
    #costruttore
    def __init__(self, _nPin = 0, _name = "", _index = 0):
        self.__n_pin = _nPin
        self.__name = _name
        self.__index = _index

    def get_n_pin(self):
        return self.__n_pin
    def get_name(self):
        return self.__name
    def get_index(self):
        return self.__index
    '''
    __n_pin = 0 
    __name = ""
    __index = 0
    '''

class ConnectorManager():
    '''
    gestore di più istanze connettore e delle matrici di collegamento tra i connettori
    '''
    def __init__(self):
        self.__conns = []
        pass
    def load_connector(self):
        pass
    def save_connector(self):
        pass
    def add_connector(self):
        pass
    def del_connector(self):
        pass


    
