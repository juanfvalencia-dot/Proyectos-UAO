class usuario:
    def __init__(self, nombre, cedula, telefono, puntos):
        self.__nombre = nombre
        self.__cedula = cedula
        self.__telefono = telefono
        self.__puntos = puntos
    
    def get_nombre(self):
        return self.__nombre
    
    def get_cedula(self):
        return self.__cedula
    
    def get_telefono(self):
        return self.__telefono
    
    def get_puntos(self):
        return self.__puntos
    
    def set_telefono(self, telefono):
        self.__telefono = telefono
    
    def set_cedula(self, cedula):
        self.__cedula = cedula

    def set_nombre(self, nombre):
        self.__nombre = nombre
    
    def fidelidad(self, tipo_sala):
        if tipo_sala.lower() == "2d":
            self.__puntos += 1000
        elif tipo_sala.lower() == "3d":
            self.__puntos += 2000
    
    def nivel(self):
        if self.__puntos >= 200000:
            return "DIAMANTE"
        elif self.__puntos >= 100000:
            return "ORO"
        elif self.__puntos >= 50000:
            return "PLATINO"
        else:
            return "BÁSICO"